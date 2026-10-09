"""Start-up fails soft (AUD-002): whatever fails to load, the person still sees how to breathe and
how to reach emergency help. Design section 8: "Any failure leaves the breath guide and the crisis
lines usable." """

from harness import base_url, browser, wait_until

EMERGENCY = "call your local emergency number"


def _open_with_failure(path, javascript=True):
    context = browser().new_context(service_workers="block", java_script_enabled=javascript)
    page = context.new_page()
    page.console_errors = []
    page.on("console", lambda m: page.console_errors.append(m.text) if m.type == "error" else None)
    if path:
        page.route(f"**/{path}", lambda route: route.abort("internetdisconnected"))
    page.goto(base_url())
    return context, page


def _wait_settled(page):
    wait_until(page, "['true', 'fallback'].includes(document.documentElement.dataset.ready)", 5000)


def test_a_failed_crisis_file_keeps_the_guide_and_the_emergency_route():
    context, page = _open_with_failure("data/crisis-lines.json")
    try:
        _wait_settled(page)
        assert page.evaluate("document.documentElement.dataset.ready") == "true"
        assert page.locator(".menu-item").first.is_visible()
        page.locator(".help-open").click()
        dialog = page.locator("dialog.help")
        assert EMERGENCY in dialog.locator(".emergency").inner_text()
        assert dialog.locator(".directory a").get_attribute("href") == "https://findahelpline.com/"
        # The reason is logged, so a field report of "no lines" can be debugged (AUD-084).
        assert any("could not load the crisis lines" in e for e in page.console_errors), page.console_errors
    finally:
        context.close()


def test_a_failed_core_file_leaves_the_static_fallback():
    for path in ("config.json", "strings/en.json", "app.js", "screens/menu.js"):
        context, page = _open_with_failure(path)
        try:
            fallback = page.locator("#fallback")
            # A failed boot shows it at once; a module that never loads shows it after fallback.js's wait.
            fallback.wait_for(state="visible", timeout=4000)
            assert fallback.is_visible(), f"{path}: the fallback must stay on screen"
            assert EMERGENCY in fallback.inner_text(), path
            assert fallback.locator("a[href='https://findahelpline.com/']").count() == 1, path
            assert page.locator("h1").count() == 1, f"{path}: one heading, no half-built shell"
        finally:
            context.close()


def test_with_javascript_off_the_fallback_shows():
    context, page = _open_with_failure(None, javascript=False)
    try:
        assert EMERGENCY in page.locator("#fallback").inner_text()
        assert "Breathe in" in page.locator("#fallback").inner_text()
    finally:
        context.close()


def test_a_normal_start_replaces_the_fallback():
    context, page = _open_with_failure(None)
    try:
        _wait_settled(page)
        assert page.locator("#fallback").count() == 0
        assert page.locator(".menu-item").first.is_visible(), "the app opens on the menu"
    finally:
        context.close()


def test_a_failed_screen_start_falls_back_to_the_menu_and_links_still_work():
    # AUD-008: a deep link to Standards whose data cannot load must not stop the router or leave a
    # frozen screen; the person lands on the menu, and every link works.
    context = browser().new_context(viewport={"width": 390, "height": 844}, service_workers="block")
    try:
        context.route("**/data/standards.json", lambda route: route.abort())
        page = context.new_page()
        page.goto(base_url() + "#standards")
        page.wait_for_selector("html[data-ready='true']", timeout=5000)
        wait_until(page, "document.querySelector('main').dataset.shown === 'menu'", 5000)
        assert page.evaluate("location.hash") == "#menu"
        assert page.locator("main .page.standards").count() == 0, "no half-drawn Standards screen"
        page.locator(".menu-item[href='#bubbles']").click()
        wait_until(page, "document.querySelector('main').dataset.shown === 'bubbles'", 3000)
        page.locator(".nav-back").click()
        wait_until(page, "document.querySelector('main').dataset.shown === 'menu'", 3000)
    finally:
        context.close()


def test_a_menu_that_cannot_start_brings_back_the_static_fallback():
    # AUD-002: a failure after the shell is built still leaves the breathing line and the emergency
    # route on screen.
    context = browser().new_context(viewport={"width": 390, "height": 844}, service_workers="block")
    try:
        context.route("**/screens/menu.js", lambda route: route.fulfill(
            status=200, content_type="text/javascript",
            body="export function start() { throw new Error('broken'); } export function stop() {}"))
        page = context.new_page()
        page.goto(base_url())
        wait_until(page, "document.documentElement.dataset.ready === 'fallback'", 6000)
        assert page.locator("#fallback").is_visible()
        assert "emergency" in page.locator("#fallback").inner_text().lower()
    finally:
        context.close()
