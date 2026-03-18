# Known Pitfalls

Cross-phase gotchas discovered during real-world usage. Each pitfall includes the symptom, root cause, and fix.

## 1. CSS filter: brightness() fails in Chrome print

**Symptom:** Images appear at full brightness in PDF despite having `filter: brightness(0.6)` in CSS.

**Root cause:** Chrome's print rendering engine (Skia) ignores CSS `filter` properties entirely — not just for `@media print`, but also for `Page.printToPDF` via CDP. This is documented in Chromium bug tracker but won't be fixed as it's considered a performance trade-off.

**Fix:** Pre-process images with Python Pillow during Phase 1:
```python
from PIL import Image, ImageEnhance
img = Image.open('photo.jpg')
dark = ImageEnhance.Brightness(img).enhance(0.6)
dark.save('output/img/photo-dark.jpg', quality=85)
```

Use the pre-processed image directly in HTML. No CSS filters.

## 2. CDP ignores --remote-debugging-port when Chrome is already open

**Symptom:** `export-pdf.py` launches Chrome but can't connect to CDP. `http://localhost:9222/json` returns connection refused.

**Root cause:** When Chrome is already running with a user profile, launching a new instance with the same profile just opens a new window in the existing process — which doesn't have CDP enabled. The `--remote-debugging-port` flag is silently ignored.

**Fix:** Always use a temporary `--user-data-dir`:
```python
import tempfile
user_data_dir = tempfile.mkdtemp(prefix='webview-cdp-')
chrome_args.append(f'--user-data-dir={user_data_dir}')
```

This creates an independent Chrome process with its own debug port.

## 3. JSON structure changes break the renderer

**Symptom:** Slides render correctly without filters, but crash with filters enabled. Console shows `Cannot read property 'length' of undefined`.

**Root cause:** The `generate.py` script omits sections when filters produce no data (e.g., removing the `timeline` key entirely when `--cutoff` filters out all timeline events).

**Fix:** Apply the fixed schema contract — ALL sections always present:
```python
data = {
    "timeline": [],        # empty array, not missing key
    "highlights": None,    # null, not missing key
}
```

## 4. Missing Python deps cause silent failures

**Symptom:** Extraction script runs without errors but produces empty or partial data.

**Root cause:** Python imports fail silently when wrapped in try/except blocks, or the script uses a built-in module that can't handle the file format (e.g., `csv` module for `.xlsx` files).

**Fix:** Run `check-deps.py` before any data extraction. It detects source file types and installs required packages. Phase 0 is non-optional.

## 5. Wrong date field used for filters

**Symptom:** Filtered presentation shows different totals than expected. Validation dataset reveals items that should be included are excluded (or vice versa).

**Root cause:** Using `end_date` instead of `start_date` for a cutoff filter (or the reverse). The field semantics depend on the business context — "active projects as of date X" requires `start_date <= X AND (end_date >= X OR end_date IS NULL)`, not just `start_date >= X`.

**Fix:**
1. Always clarify with the user which date field the filter should use
2. Generate validation.json with `excluded_items` showing the reason each item was excluded
3. Present validation summary before proceeding to rendering

## 6. white-space: nowrap missing on badges

**Symptom:** Status badges and tags break across two lines, looking broken.

**Root cause:** Default `white-space: normal` allows line breaks in small containers. Badge text like "Em andamento" wraps at the space.

**Fix:** Always add `white-space: nowrap` to badge/tag CSS:
```css
.detail-card-badge, .tag {
    white-space: nowrap;
}
```

## 7. Chrome --remote-allow-origins flag missing

**Symptom:** WebSocket connection to CDP fails with "403 Forbidden" or "Origin not allowed" after upgrading Chrome.

**Root cause:** Since Chrome 113, cross-origin connections to the DevTools WebSocket require explicit permission via `--remote-allow-origins=*`.

**Fix:** Always include the flag when launching Chrome:
```
--remote-allow-origins=*
```

The `export-pdf.py` script includes this by default.

## 8. Fonts not loading in PDF

**Symptom:** PDF shows fallback fonts (serif/sans-serif) instead of the specified Google Fonts.

**Root cause:** The PDF export happens before fonts finish downloading. Google Fonts load asynchronously.

**Fix:** Wait for `document.fonts.ready` before calling `Page.printToPDF`:
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

Also specify exact font weights in the Google Fonts URL to avoid missing weight variants.

## Quick Reference

| Pitfall | Phase | Impact | Prevention |
|---------|-------|--------|------------|
| CSS filters in print | 3→4 | Images wrong in PDF | Pre-process with Pillow |
| CDP port ignored | 4 | Export fails entirely | Temp user-data-dir |
| JSON schema changes | 2→3 | Renderer crashes | Fixed schema contract |
| Missing Python deps | 1 | Partial/empty data | check-deps.py in Phase 0 |
| Wrong date filter | 1→2 | Incorrect totals | Validation dataset + user confirmation |
| Badge text wrapping | 3 | Visual glitch | white-space: nowrap |
| Missing allow-origins | 4 | CDP 403 error | --remote-allow-origins=* |
| Fonts not loaded | 4 | Wrong fonts in PDF | document.fonts.ready |
