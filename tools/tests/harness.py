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


class _Server(socketserver.ThreadingTCPServer):
    # The service worker requests every file at once on install. Python's default listen queue of
    # 5 then refuses connections on Windows, which looks like an app that cannot start.
    request_queue_size = 128
    daemon_threads = True
    allow_reuse_address = True


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    # Keep connections open between requests. With HTTP/1.0 every file is a new socket, and the
    # suite's many service-worker installs exhaust Windows' socket buffers (ERR_NO_BUFFER_SPACE).
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass

    # Never let the test server's own caching hide a stale file, unless a test asks for the
    # caching GitHub Pages uses (max-age=600), to check that an update gets past it (AUD-013).
    cache_control = "no-store"

    def end_headers(self):
        self.send_header("Cache-Control", self.cache_control)
        super().end_headers()


def serve(directory: Path, cache_control: str = "no-store") -> str:
    """Serve a directory on a new free localhost port; return its URL."""
    handler_class = type("_Handler", (_QuietHandler,), {"cache_control": cache_control})
    handler = functools.partial(handler_class, directory=str(directory))
    server = _Server(("127.0.0.1", 0), handler)
    # A browser that closes a page mid-download aborts the socket; that is not a test failure.
    server.handle_error = lambda request, address: None
    threading.Thread(target=server.serve_forever, daemon=True).start()
    atexit.register(server.shutdown)
    return f"http://localhost:{server.server_address[1]}/"


def base_url() -> str:
    global _server
    if _server is None:
        _server = serve(ROOT)
    return _server


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
             viewport=None, service_workers="block", init_script=None, route="breathe"):
    """Open the app in a fresh context, on `route`. Yields (page, errors, requests).

    The app opens on the menu; most tests are about one screen, so they start there. Pass
    route=None to open the app as a person does."""
    context = browser().new_context(
        locale=locale, color_scheme=color_scheme, reduced_motion=reduced_motion,
        viewport=viewport or {"width": 390, "height": 844}, service_workers=service_workers)
    if init_script:
        context.add_init_script(init_script)
    page = context.new_page()
    errors: list[str] = []
    requests: list[str] = []
    # Tests block the service worker unless they need it: each install fetches every file, and over
    # a whole suite that exhausts Windows' sockets (ERR_NO_BUFFER_SPACE). Playwright's own notice
    # about the block is not an app error.
    page.on("console", lambda m: errors.append(m.text)
            if m.type in ("error", "warning") and "blocked by Playwright" not in m.text else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("request", lambda r: requests.append(r.url))
    page.goto(base_url() + (f"#{route}" if route else ""))
    try:
        page.wait_for_selector("html[data-ready='true']", timeout=5000)
    except Exception as error:
        ready = page.evaluate("document.documentElement.dataset.ready")
        context.close()
        raise AssertionError(f"the app did not start: ready={ready}; console: {errors}") from error
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
        try:
            if page.evaluate(expression):
                return
        except Exception as error:
            # The app reloads itself when a new version takes over; keep waiting across that.
            if "context was destroyed" not in str(error) and "navigat" not in str(error):
                raise
        time.sleep(0.05)
    raise AssertionError(f"timed out after {timeout_ms} ms waiting for: {expression}")