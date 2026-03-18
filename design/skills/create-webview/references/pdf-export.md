# PDF Export Reference

Step-by-step guide for Phase 4 — exporting HTML presentations to PDF via Chrome DevTools Protocol (CDP).

## Overview

The export pipeline: HTML (served locally) → Chrome (headed, with CDP) → PDF via `Page.printToPDF`. The `scripts/export-pdf.py` script handles all complexity, but understanding the internals helps debug edge cases.

## Chrome Setup

### Why headed, not headless?

Chrome headless mode (`--headless=new`) has subtle rendering differences from headed mode, especially with:
- Custom fonts (may not load in headless)
- CSS animations (may not complete)
- Complex flexbox layouts (occasional pixel differences)

Headed mode shows the user exactly what's being exported. Transparency builds trust.

### Required flags

```
--remote-debugging-port=9222     # Enable CDP
--remote-allow-origins=*         # Required since Chrome 113+
--user-data-dir=<temp-dir>       # CRITICAL: use temp dir
--no-first-run                   # Skip Chrome welcome screens
--no-default-browser-check       # Skip default browser prompt
--disable-extensions             # Faster startup
```

### The user-data-dir trap

If Chrome is already running (user's normal browsing), launching a new instance with `--remote-debugging-port` **silently fails** — it just opens a new window in the existing instance, without CDP enabled.

The fix: always use a temporary `--user-data-dir`. This forces Chrome to create a completely independent instance with its own debug port. The `export-pdf.py` script creates this via `tempfile.mkdtemp()` and cleans it up after export.

```python
import tempfile
user_data_dir = tempfile.mkdtemp(prefix='webview-cdp-')
# ... use in Chrome args ...
# cleanup:
shutil.rmtree(user_data_dir, ignore_errors=True)
```

## WebSocket Connection

### Discovery

Chrome exposes CDP targets at `http://localhost:9222/json`. Each target has a `webSocketDebuggerUrl`:

```json
[
  {
    "type": "page",
    "url": "http://localhost:5500/output/index.html",
    "webSocketDebuggerUrl": "ws://localhost:9222/devtools/page/ABC123"
  }
]
```

### Connection with retry

Chrome needs a moment to start and register targets. The script retries for 30 seconds:

```python
import websocket
import urllib.request
import json
import time

start = time.time()
while time.time() - start < 30:
    try:
        resp = urllib.request.urlopen('http://localhost:9222/json')
        tabs = json.loads(resp.read())
        for tab in tabs:
            if tab.get('type') == 'page':
                ws = websocket.create_connection(tab['webSocketDebuggerUrl'])
                break
    except:
        time.sleep(0.5)
```

## Page Size Injection

Chrome's `Page.printToPDF` uses `@page` CSS rules for dimensions. Inject the exact slide size:

```javascript
// Injected via Runtime.evaluate:
(function() {
    var style = document.createElement('style');
    style.textContent = '@page { size: 1440px 810px; margin: 0; }';
    document.head.appendChild(style);
})()
```

```python
ws.send(json.dumps({
    'id': 1,
    'method': 'Runtime.evaluate',
    'params': {
        'expression': '(function(){var s=document.createElement("style");s.textContent="@page{size:1440px 810px;margin:0}";document.head.appendChild(s)})()'
    }
}))
```

## Font Loading

Wait for all fonts (especially Google Fonts) to load before exporting:

```python
ws.send(json.dumps({
    'id': 2,
    'method': 'Runtime.evaluate',
    'params': {
        'expression': 'document.fonts.ready.then(() => "ready")',
        'awaitPromise': True
    }
}))
```

Add a short delay (1-2s) after font loading for any remaining async rendering.

## PDF Generation

```python
ws.send(json.dumps({
    'id': 3,
    'method': 'Page.printToPDF',
    'params': {
        'preferCSSPageSize': True,
        'printBackground': True,
        'marginTop': 0,
        'marginBottom': 0,
        'marginLeft': 0,
        'marginRight': 0
    }
}))

result = json.loads(ws.recv())
pdf_bytes = base64.b64decode(result['result']['data'])
```

Key params:
- `preferCSSPageSize: true` — uses the injected `@page` dimensions
- `printBackground: true` — renders background colors and images (essential for dark themes)
- All margins `0` — the slide CSS handles all spacing internally

## Known Issues and Workarounds

### CSS filters don't print

`filter: brightness()`, `filter: grayscale()`, `filter: drop-shadow()` — all are ignored in Chrome's print rendering. This includes both `@media print` and `Page.printToPDF`.

**Workaround:** Pre-process images with Python (Pillow) during Phase 1. Create darkened/filtered versions as actual image files.

### Page breaks

Each `.slide` div must start on a new page. Use:

```css
@media print {
    .slide {
        break-after: page;
        break-inside: avoid;
    }
}
```

The `break-inside: avoid` prevents Chrome from splitting a slide across two pages.

### Background gradients

Complex CSS gradients sometimes render incorrectly in print. Use simple linear gradients (2 stops max) for reliable results. For complex backgrounds, use pre-rendered images.

### Web fonts in PDF

Google Fonts usually work if `document.fonts.ready` is awaited. However, some font weights may not load if the CSS `@import` or `<link>` doesn't explicitly request them.

**Tip:** Always specify exact weights in the Google Fonts URL:
```html
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

## Cleanup Procedure

After export (success or failure):

1. Close WebSocket connection
2. Send SIGTERM to Chrome process
3. Wait up to 5 seconds for graceful shutdown
4. Force kill if still running
5. Remove temp `user-data-dir`
6. Verify PDF file was written and has non-zero size

```python
import signal, shutil

def cleanup(proc, user_data_dir):
    try:
        if proc.poll() is None:
            proc.send_signal(signal.SIGTERM)
            proc.wait(timeout=5)
    except:
        try:
            proc.kill()
        except:
            pass
    shutil.rmtree(user_data_dir, ignore_errors=True)
```
