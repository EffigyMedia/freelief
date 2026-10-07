"""Owner feedback from the phone, 2026-10-07: a way out of urgent help at the top, the phone's back
gesture closes it, and every exercise and activity offers "More ways to calm"."""

from harness import open_app, wait_until

EXERCISES = ["ground", "statements", "bubbles", "trace", "sort"]


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
        page.locator("details.others summary").click()
        page.locator("dialog.help").evaluate("d => d.scrollTo(0, d.scrollHeight)")
        assert back.is_visible() and back.bounding_box()["y"] < 120, "Back stays visible after scrolling"
        back.click()
        assert not page.locator("dialog.help").evaluate("d => d.open")


def test_the_phone_back_gesture_closes_urgent_help_and_stays_in_the_app():
    with open_app() as (page, _, _):
        go(page, "ground")
        page.locator(".help-open").click()
        assert page.locator("dialog.help").evaluate("d => d.open")
        page.go_back()
        wait_until(page, "!document.querySelector('dialog.help').open", 2000)
        assert page.evaluate("document.querySelector('main').dataset.shown") == "ground"
        # Closing by the Back button must not leave an extra history step behind.
        page.locator(".help-open").click()
        page.locator("dialog.help .help-back").click()
        wait_until(page, "!(history.state && history.state.freeliefHelp)", 2000)
        page.go_back()
        wait_until(page, "document.querySelector('main').dataset.shown === 'breathe'", 3000)


def test_every_exercise_offers_more_ways_and_back_to_breathing():
    with open_app() as (page, _, _):
        for screen in EXERCISES:
            go(page, screen)
            assert page.locator(".nav-more").is_visible(), screen
            assert page.locator(".nav-back").is_visible(), screen
        go(page, "breathe")
        assert page.locator(".nav-more").is_visible() and page.locator(".nav-back").is_hidden()
        go(page, "menu")
        assert page.locator(".nav-more").is_hidden() and page.locator(".nav-back").is_visible()