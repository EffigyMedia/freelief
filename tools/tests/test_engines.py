"""The supported browsers (AUD-028, owner 2026-10-08): Chrome, Safari and Firefox. The rest of the
suite runs in Chrome; the never-break paths (by pointer, by keyboard, and offline) also run in
WebKit, Safari's engine. Firefox joins when
its engine can start on this machine (see RLG-033)."""

from harness import engine, open_app, wait_until


def go(page, route):
    page.evaluate(f"location.hash = '{route}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 5000)


def never_break(browser):
    with open_app(route=None, on=browser) as (page, errors, _):
        assert page.evaluate("document.querySelector('main').dataset.shown") == "menu"
        page.locator(".menu-item[href='#breathe']").click()
        wait_until(page, "document.querySelector('main').dataset.shown === 'breathe'", 5000)
        wait_until(page, "document.querySelector('.phase').textContent.trim().length > 0", 3000)
        page.locator(".help-open").click()
        assert page.locator("dialog.help").evaluate("d => d.open")
        assert page.locator(".directory a").count() == 1
        page.locator("dialog.help .help-back").click()
        go(page, "bubbles")
        page.locator("button.bubble").first.click(force=True)
        go(page, "unblock")
        page.locator(".unblock-block").nth(0).click()
        page.locator(".unblock-slide button").nth(1).click()
        go(page, "mandala")
        page.locator(".mandala-part").first.click()
        go(page, "settings")
        page.locator("button.sound-toggle").click()
        assert page.locator("button.sound-toggle").get_attribute("aria-pressed") == "false"
        assert not errors, errors


def by_keyboard(browser):
    # The never-break paths without a pointer (AUD-028): help opens and closes, breathing pauses.
    with open_app(route="breathe", on=browser) as (page, errors, _):
        page.locator(".help-open").focus()
        page.keyboard.press("Enter")
        assert page.locator("dialog.help").evaluate("d => d.open")
        page.keyboard.press("Escape")
        assert not page.locator("dialog.help").evaluate("d => d.open")
        page.locator(".pause").focus()
        page.keyboard.press("Enter")
        assert page.locator(".pause").inner_text() == "Resume"
        assert not errors, errors


def offline(browser):
    # The app opens with no network once it has been installed (REQ-008), in this engine too. WebKit
    # in Playwright cannot navigate while a context is set offline, so the server is stopped instead.
    import functools
    import http.server
    import threading
    from harness import ROOT
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    handler.log_message = lambda *args: None
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://localhost:{server.server_address[1]}/"
    context = browser.new_context(service_workers="allow")
    try:
        page = context.new_page()
        page.goto(url)
        page.evaluate("navigator.serviceWorker.ready.then(() => 1)")
        page.goto(url)
        wait_until(page, "navigator.serviceWorker.controller !== null", 8000)
        server.shutdown()
        server.server_close()
        page.goto(url)
        page.wait_for_selector("html[data-ready='true']", timeout=10000)
        page.locator(".help-open").click()
        assert page.locator("dialog.help").evaluate("d => d.open")
    finally:
        context.close()


def test_the_never_break_paths_work_in_webkit():
    never_break(engine("webkit"))


def test_the_never_break_paths_work_by_keyboard_in_webkit():
    by_keyboard(engine("webkit"))


def test_the_app_opens_offline_in_webkit():
    offline(engine("webkit"))
