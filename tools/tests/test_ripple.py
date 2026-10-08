"""The ripple pond (REQ-032): by touch, by a drag, by keyboard, under reduced motion, with a sound."""

import json

from harness import ROOT, open_app, wait_until

CONFIG = json.loads((ROOT / "config.json").read_text("utf-8"))
STRINGS = json.loads((ROOT / "strings" / "en.json").read_text("utf-8"))
SETTINGS = CONFIG["ripple"]

OSC_PROBE = """
window.__osc = 0;
const create = AudioContext.prototype.createOscillator;
AudioContext.prototype.createOscillator = function () { window.__osc += 1; return create.call(this); };
"""


def go(page, route):
    page.evaluate(f"location.hash = '{route}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 3000)


def sets(page):
    return page.locator(".pond .ripple-set")


def test_a_tap_makes_rings_spread_from_that_point_and_they_clear_away():
    with open_app() as (page, errors, _):
        go(page, "ripple")
        pond = page.locator(".pond").bounding_box()
        page.mouse.click(pond["x"] + 80, pond["y"] + 60)
        assert sets(page).count() == 1
        ripple = sets(page).first
        assert ripple.evaluate("e => [e.style.left, e.style.top]") == ["80px", "60px"]
        assert ripple.locator(".ripple-ring").count() == SETTINGS["rings"]
        ring = ripple.locator(".ripple-ring").first
        assert ring.evaluate("e => getComputedStyle(e).animationName") == "ripple-spread"
        life = SETTINGS["lifeSeconds"] + SETTINGS["rings"] * SETTINGS["ringGapSeconds"]
        wait_until(page, "document.querySelectorAll('.pond .ripple-set').length === 0", int(life * 1000) + 1500)
        assert not errors, errors


def test_a_finger_drawn_across_the_water_leaves_a_trail_but_never_too_many():
    with open_app() as (page, _, _):
        go(page, "ripple")
        pond = page.locator(".pond").bounding_box()
        y = pond["y"] + pond["height"] / 2
        page.mouse.move(pond["x"] + 20, y)
        page.mouse.down()
        page.mouse.move(pond["x"] + 20 + SETTINGS["trailSpacing"] * 3.5, y, steps=12)
        page.mouse.up()
        assert sets(page).count() == 4, "one ripple at the touch, then one every trailSpacing pixels"
        page.mouse.move(pond["x"] + 10, pond["y"] + 20)
        page.mouse.down()
        page.mouse.move(pond["x"] + pond["width"] - 10, pond["y"] + pond["height"] - 20, steps=40)
        page.mouse.up()
        assert sets(page).count() == SETTINGS["maxRipples"]
        assert page.locator(".pond").evaluate("e => getComputedStyle(e).touchAction") == "none"


def test_the_pond_works_by_keyboard_and_has_a_name():
    with open_app() as (page, errors, _):
        go(page, "ripple")
        pond = page.locator("button.pond")
        assert pond.get_attribute("aria-label") == STRINGS["ripple.pondLabel"]
        assert page.locator("#ripple-intro").inner_text() == STRINGS["ripple.intro"]
        page.locator(".nav-back").focus()
        page.keyboard.press("Tab")
        assert page.evaluate("document.activeElement.classList.contains('pond')")
        page.keyboard.press("Enter")
        page.keyboard.press("Space")
        assert sets(page).count() == 2
        box = pond.bounding_box()
        for i in range(2):
            x, y = sets(page).nth(i).evaluate("e => [parseFloat(e.style.left), parseFloat(e.style.top)]")
            margin = SETTINGS["keyboardMargin"]
            assert margin <= x <= box["width"] - margin and margin <= y <= box["height"] - margin
        assert not errors, errors


def test_a_tap_is_one_ripple_not_two():
    # The click that follows a pointer down must not add a second, random ripple.
    with open_app() as (page, _, _):
        go(page, "ripple")
        page.locator(".pond").click(position={"x": 100, "y": 100})
        page.wait_for_timeout(100)
        assert sets(page).count() == 1


def test_under_reduced_motion_the_rings_fade_and_do_not_spread():
    with open_app(reduced_motion="reduce") as (page, _, _):
        go(page, "ripple")
        page.locator(".pond").click(position={"x": 120, "y": 90})
        ring = page.locator(".ripple-ring").first
        assert "still" in ring.get_attribute("class")
        assert ring.evaluate("e => getComputedStyle(e).animationName") == "ripple-fade"
        assert ring.evaluate("e => getComputedStyle(e).animationDuration") == f"{SETTINGS['lifeSeconds']}s"


def test_each_ripple_plays_a_drop():
    with open_app(init_script=OSC_PROBE) as (page, _, _):
        page.locator(".guide").click()  # the first gesture unlocks sound
        go(page, "ripple")
        page.wait_for_timeout(300)
        before = page.evaluate("window.__osc")
        page.locator(".pond").click(position={"x": 100, "y": 100})
        wait_until(page, f"window.__osc > {before}", 2000)
