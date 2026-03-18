#!/usr/bin/env python3
"""
export-pdf.py — Export an HTML presentation to PDF via Chrome DevTools Protocol.

Handles:
- Temp user-data-dir (works even with Chrome already open)
- --remote-allow-origins=* (required since Chrome 113+)
- @page CSS injection for exact slide dimensions
- Retry loop with configurable timeout
- Automatic cleanup

Usage:
  python3 export-pdf.py --url http://localhost:5500 --output presentation.pdf
  python3 export-pdf.py --url file:///path/to/index.html --output out.pdf --width 1920 --height 1080
"""

import argparse
import base64
import json
import os
import platform
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import urllib.request


def find_chrome():
    """Find Chrome executable path."""
    candidates = []
    system = platform.system()

    if system == 'Darwin':
        candidates = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Chromium.app/Contents/MacOS/Chromium',
        ]
    elif system == 'Linux':
        candidates = [
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
            '/usr/bin/chromium-browser',
            '/usr/bin/chromium',
        ]
    elif system == 'Windows':
        candidates = [
            os.path.expandvars(r'%ProgramFiles%\Google\Chrome\Application\chrome.exe'),
            os.path.expandvars(r'%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe'),
            os.path.expandvars(r'%LocalAppData%\Google\Chrome\Application\chrome.exe'),
        ]

    for path in candidates:
        if os.path.isfile(path):
            return path

    # Try PATH
    import shutil as sh
    chrome = sh.which('google-chrome') or sh.which('chromium') or sh.which('chrome')
    if chrome:
        return chrome

    return None


def launch_chrome(chrome_path, url, port=9222):
    """Launch Chrome with CDP enabled and temp user-data-dir."""
    user_data_dir = tempfile.mkdtemp(prefix='webview-cdp-')

    args = [
        chrome_path,
        f'--remote-debugging-port={port}',
        '--remote-allow-origins=*',
        f'--user-data-dir={user_data_dir}',
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-extensions',
        url,
    ]

    proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return proc, user_data_dir


def connect_cdp(port=9222, timeout=30):
    """Connect to Chrome CDP via WebSocket with retry loop."""
    try:
        import websocket
    except ImportError:
        print('ERROR: websocket-client not installed. Run: pip3 install websocket-client')
        sys.exit(1)

    start = time.time()
    last_error = None

    while time.time() - start < timeout:
        try:
            resp = urllib.request.urlopen(f'http://localhost:{port}/json')
            tabs = json.loads(resp.read())

            # Find a page target (not devtools or service worker)
            ws_url = None
            for tab in tabs:
                if tab.get('type') == 'page':
                    ws_url = tab.get('webSocketDebuggerUrl')
                    break

            if not ws_url and tabs:
                ws_url = tabs[0].get('webSocketDebuggerUrl')

            if ws_url:
                ws = websocket.create_connection(ws_url)
                return ws
        except Exception as e:
            last_error = e
            time.sleep(0.5)

    raise TimeoutError(
        f'Could not connect to Chrome CDP on port {port} after {timeout}s. '
        f'Last error: {last_error}'
    )


def inject_page_size(ws, width, height, msg_id=1):
    """Inject @page CSS rule for exact dimensions."""
    js = f"""
    (function() {{
        var style = document.createElement('style');
        style.textContent = '@page {{ size: {width}px {height}px; margin: 0; }}';
        document.head.appendChild(style);
    }})()
    """
    ws.send(json.dumps({
        'id': msg_id,
        'method': 'Runtime.evaluate',
        'params': {'expression': js}
    }))
    return json.loads(ws.recv())


def wait_for_fonts(ws, msg_id=2):
    """Wait for all fonts to be loaded."""
    ws.send(json.dumps({
        'id': msg_id,
        'method': 'Runtime.evaluate',
        'params': {
            'expression': 'document.fonts.ready.then(() => "ready")',
            'awaitPromise': True
        }
    }))
    return json.loads(ws.recv())


def print_to_pdf(ws, msg_id=3):
    """Generate PDF via CDP."""
    ws.send(json.dumps({
        'id': msg_id,
        'method': 'Page.printToPDF',
        'params': {
            'preferCSSPageSize': True,
            'printBackground': True,
            'marginTop': 0,
            'marginBottom': 0,
            'marginLeft': 0,
            'marginRight': 0,
        }
    }))
    result = json.loads(ws.recv())

    if 'error' in result:
        raise RuntimeError(f'printToPDF failed: {result["error"]}')

    return base64.b64decode(result['result']['data'])


def cleanup(proc, user_data_dir):
    """Terminate Chrome and remove temp directory."""
    try:
        if proc.poll() is None:
            proc.send_signal(signal.SIGTERM)
            proc.wait(timeout=5)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass

    try:
        shutil.rmtree(user_data_dir, ignore_errors=True)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description='Export HTML presentation to PDF via Chrome CDP')
    parser.add_argument('--url', default='http://localhost:5500', help='URL to export (default: http://localhost:5500)')
    parser.add_argument('--output', '-o', default='presentation.pdf', help='Output PDF path (default: presentation.pdf)')
    parser.add_argument('--width', type=int, default=1440, help='Slide width in px (default: 1440)')
    parser.add_argument('--height', type=int, default=810, help='Slide height in px (default: 810)')
    parser.add_argument('--port', type=int, default=9222, help='Chrome debug port (default: 9222)')
    parser.add_argument('--timeout', type=int, default=30, help='CDP connection timeout in seconds (default: 30)')
    parser.add_argument('--delay', type=float, default=2.0, help='Delay before PDF export in seconds (default: 2.0)')
    args = parser.parse_args()

    # Find Chrome
    chrome_path = find_chrome()
    if not chrome_path:
        print('ERROR: Chrome not found. Please install Google Chrome.')
        sys.exit(1)
    print(f'Chrome: {chrome_path}')

    # Launch
    print(f'Opening {args.url}...')
    proc, user_data_dir = launch_chrome(chrome_path, args.url, args.port)

    try:
        # Connect
        print(f'Connecting to CDP (port {args.port}, timeout {args.timeout}s)...')
        ws = connect_cdp(port=args.port, timeout=args.timeout)
        print('Connected.')

        # Inject page size
        print(f'Setting page size: {args.width}x{args.height}px')
        inject_page_size(ws, args.width, args.height)

        # Wait for fonts
        print('Waiting for fonts...')
        wait_for_fonts(ws)

        # Delay for rendering
        print(f'Waiting {args.delay}s for full render...')
        time.sleep(args.delay)

        # Export
        print('Exporting PDF...')
        pdf_data = print_to_pdf(ws)

        # Write
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, 'wb') as f:
            f.write(pdf_data)

        size_mb = len(pdf_data) / (1024 * 1024)
        print(f'PDF saved: {args.output} ({size_mb:.1f} MB)')

        ws.close()

    finally:
        print('Cleaning up...')
        cleanup(proc, user_data_dir)

    print('Done.')


if __name__ == '__main__':
    main()
