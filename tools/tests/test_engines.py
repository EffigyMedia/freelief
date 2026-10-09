"""The supported browsers (AUD-028, owner 2026-10-08): Chrome, Safari and Firefox. The rest of the
suite runs in Chrome; these never-break paths also run in WebKit, Safari's engine. Firefox joins when
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


def test_the_never_break_paths_work_in_webkit():
    never_break(engine("webkit"))
