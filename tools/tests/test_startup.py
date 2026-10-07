"""Start-up fails soft (AUD-002): whatever fails to load, the person still sees how to breathe and
how to reach emergency help. Design section 8: "Any failure leaves the breath guide and the crisis
lines usable." """

from harness import base_url, browser, wait_until

EMERGENCY = "call your local emergency number"


def _open_with_failure(path, javascript=True):
    context = browser().new_context(service_workers="block", java_script_enabled=javascript)
    page = context.new_page()
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
        assert page.locator(".guide").is_visible()
        page.locator(".help-open").click()
        dialog = page.locator("dialog.help")
        assert EMERGENCY in dialog.locator(".emergency").inner_text()
        assert dialog.locator(".directory a").get_attribute("href") == "https://findahelpline.com/"
    finally:
        context.close()


def test_a_failed_core_file_leaves_the_static_fallback():
    for path in ("config.json", "strings/en.json", "app.js", "exercises/breathe.js"):
        context, page = _open_with_failure(path)
        try:
            page.wait_for_timeout(800)
            fallback = page.locator("#fallback")
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
        assert page.locator(".guide").is_visible()
    finally:
        context.close()
