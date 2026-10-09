"""Owner feedback from the phone, 2026-10-07: a way out of urgent help at the top, the phone's back
gesture closes it, and every exercise and activity offers a way back to the menu ("Back to menu",
which replaced "More ways to calm" the same day)."""

from harness import open_app, wait_until

EXERCISES = ["bubbles", "trace", "unblock", "ripple", "mandala", "calm"]


def go(page, route):
    page.evaluate(f"location.hash = '{route}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 3000)


def test_the_way_out_of_urgent_help_is_at_the_top_and_stays_visible():
    with open_app(viewport={"width": 360, "height": 640}) as (page, _, _):
        page.locator(".help-open").click()
        back = page.locator("dialog.help .help-back")
        assert back.inner_text() == "Back"
        box = back.bounding_box()
        assert box["y"] < 120, f"Back must be at the top of the window, found at y={box['y']}"
        page.locator("dialog.help").evaluate("d => d.scrollTo(0, d.scrollHeight)")
        assert back.is_visible() and back.bounding_box()["y"] < 120, "Back stays visible after scrolling"
        back.click()
        assert not page.locator("dialog.help").evaluate("d => d.open")


def test_the_phone_back_gesture_closes_urgent_help_and_stays_in_the_app():
    with open_app() as (page, _, _):
        go(page, "trace")
        page.locator(".help-open").click()
        assert page.locator("dialog.help").evaluate("d => d.open")
        page.go_back()
        wait_until(page, "!document.querySelector('dialog.help').open", 2000)
        assert page.evaluate("document.querySelector('main').dataset.shown") == "trace"
        # Closing by the Back button must not leave an extra history step behind.
        page.locator(".help-open").click()
        page.locator("dialog.help .help-back").click()
        wait_until(page, "!(history.state && history.state.freeliefHelp)", 2000)
        page.go_back()
        wait_until(page, "document.querySelector('main').dataset.shown === 'breathe'", 3000)


def test_every_screen_goes_back_to_the_menu():
    # Owner, 2026-10-07: "each goes back to menu".
    with open_app() as (page, _, _):
        for screen in ["breathe", *EXERCISES, "settings", "about"]:
            go(page, screen)
            back = page.locator(".nav-back")
            assert back.is_visible() and back.inner_text() == "Back to menu", screen
            assert back.get_attribute("href") == "#menu", screen
        go(page, "menu")
        assert page.locator(".nav-back").is_hidden()

def test_the_page_under_urgent_help_takes_no_touch():
    # Owner report, 2026-10-07: with help open, a swipe on the backdrop scrolled the app under it.
    with open_app(route="menu", viewport={"width": 390, "height": 460}) as (page, _, _):
        cdp = page.context.new_cdp_session(page)

        def swipe(x, y0, y1):
            cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x, "y": y0}]})
            for i in range(1, 11):
                cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [
                    {"x": x, "y": y0 + (y1 - y0) * i / 10}]})
            cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
            page.wait_for_timeout(500)

        assert page.evaluate("document.documentElement.scrollHeight > innerHeight"), "the page can scroll"
        page.locator(".help-open").click()
        swipe(5, 440, 100)  # on the backdrop, outside the dialog
        assert page.evaluate("scrollY") == 0, "the page under the dialog did not move"
        for _ in range(4):
            swipe(200, 400, 100)  # inside the dialog, past the end of its list
        assert page.evaluate("document.querySelector('dialog.help').scrollTop") > 0, "the help list scrolls"
        assert page.evaluate("scrollY") == 0, "a scroll at the end of the list does not move the page"
        cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": 5, "y": 440}]})
        cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
        assert page.evaluate("location.hash") == "#menu" and page.evaluate("document.querySelector('dialog.help').open")
        page.locator("dialog.help .help-back").click()
        swipe(200, 440, 100)
        assert page.evaluate("scrollY") > 0, "the page scrolls again once help is closed"
