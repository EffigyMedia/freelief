"""Shared browser harness: one static server and one Chrome for every browser test.

The server serves the repository root on a free localhost port; localhost is a secure context,
so the service worker runs as it does on GitHub Pages.
"""

from __future__ import annotations

import atexit
import functools
import http.server
import socketserver
import threading
import time
from contextlib import contextmanager
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent.parent

_server = None
_playwright = None
_browser = None


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def end_headers(self):
        # Never let the test server's own caching hide a stale file.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def base_url() -> str:
    global _server
    if _server is None:
        handler = functools.partial(_QuietHandler, directory=str(ROOT))
        _server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
        _server.daemon_threads = True
        # A browser that closes a page mid-download aborts the socket; that is not a test failure.
        _server.handle_error = lambda request, address: None
        threading.Thread(target=_server.serve_forever, daemon=True).start()
        atexit.register(_server.shutdown)
    return f"http://localhost:{_server.server_address[1]}/"


def browser():
    global _playwright, _browser
    if _browser is None:
        _playwright = sync_playwright().start()
        try:
            _browser = _playwright.chromium.launch(channel="chrome")
        except Exception:
            _browser = _playwright.chromium.launch()
        atexit.register(_playwright.stop)
        atexit.register(_browser.close)
    return _browser


@contextmanager
def open_app(locale="en-US", color_scheme="dark", reduced_motion="no-preference",
             viewport=None, service_workers="allow", init_script=None):
    """Open the app in a fresh context. Yields (page, errors, requests)."""
    context = browser().new_context(
        locale=locale, color_scheme=color_scheme, reduced_motion=reduced_motion,
        viewport=viewport or {"width": 390, "height": 844}, service_workers=service_workers)
    if init_script:
        context.add_init_script(init_script)
    page = context.new_page()
    errors: list[str] = []
    requests: list[str] = []
    page.on("console", lambda m: errors.append(m.text) if m.type in ("error", "warning") else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("request", lambda r: requests.append(r.url))
    page.goto(base_url())
    page.wait_for_selector("html[data-ready='true']", timeout=5000)
    try:
        yield page, errors, requests
    finally:
        context.close()


def wait_until(page, expression: str, timeout_ms: int = 5000) -> None:
    """Poll a JS expression until it is truthy.

    Playwright's wait_for_function evaluates a string, which the app's Content Security Policy
    (no 'unsafe-eval') correctly refuses; page.evaluate is not affected.
    """
    deadline = time.monotonic() + timeout_ms / 1000
    while time.monotonic() < deadline:
        if page.evaluate(expression):
            return
        time.sleep(0.05)
    raise AssertionError(f"timed out after {timeout_ms} ms waiting for: {expression}")