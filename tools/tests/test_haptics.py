"""Haptic feedback (REQ-034): one short vibration per triggered event, never for anything
continuous, on by default, off from Settings."""

import json

from harness import ROOT, open_app, wait_until

CONFIG = json.loads((ROOT / "config.json").read_text("utf-8"))
PATTERNS = CONFIG["haptics"]["patterns"]

VIBRATE_PROBE = """
window.__buzz = [];
Object.defineProperty(navigator, 'vibrate', { configurable: true,
  value: (pattern) => { window.__buzz.push(pattern); return true; } });
"""


def go(page, route):
    page.evaluate(f"location.hash = '{route}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 3000)


def buzz(page):
    return page.evaluate("window.__buzz")


def test_each_activity_event_gives_one_short_pulse():
    with open_app(init_script=VIBRATE_PROBE) as (page, errors, _):
        go(page, "bubbles")
        page.locator("button.bubble").first.click(force=True)
        assert buzz(page) == [PATTERNS["pop"]]
        go(page, "sort")
        page.locator(".sort-tile").nth(0).click()
        page.locator(".sort-tile").nth(1).click()
        assert buzz(page)[1:] == [PATTERNS["choose"], PATTERNS["swap"]]
        go(page, "ripple")
        page.locator(".pond").click(position={"x": 100, "y": 100})
        assert buzz(page)[-1] == PATTERNS["ripple"]
        go(page, "mandala")
        page.locator(".mandala-part").first.click()
        assert buzz(page)[-1] == PATTERNS["fill"]
        assert all(p in PATTERNS.values() for p in buzz(page))
        assert not errors, errors


def test_nothing_continuous_vibrates():
    with open_app(init_script=VIBRATE_PROBE) as (page, _, _):
        page.wait_for_timeout(9000)  # a full box-breathing cycle and more: in, hold, out
        assert buzz(page) == [], "the breathing guide never vibrates"
        go(page, "ripple")
        pond = page.locator(".pond").bounding_box()
        y = pond["y"] + pond["height"] / 2
        page.mouse.move(pond["x"] + 20, y)
        page.mouse.down()
        page.mouse.move(pond["x"] + pond["width"] - 20, y, steps=20)
        page.mouse.up()
        assert page.locator(".ripple-set").count() > 2, "the drag left a trail"
        assert buzz(page) == [PATTERNS["ripple"]], "only the touch pulses, not the trail"


def test_the_switch_turns_it_off_and_the_choice_is_saved():
    with open_app(init_script=VIBRATE_PROBE) as (page, _, _):
        go(page, "settings")
        switch = page.locator("input[name=haptics]")
        assert switch.is_checked(), "on by default"
        # Owner, 2026-10-07: say plainly where it does not work.
        hint = page.locator("#haptics-hint").inner_text()
        assert "does not work on iPhone or in Safari" in hint
        assert switch.get_attribute("aria-describedby") == "haptics-hint"
        page.locator("input[name=haptics]").focus()
        page.keyboard.press("Space")
        assert not switch.is_checked()
        page.reload()
        wait_until(page, "document.documentElement.dataset.ready === 'true'")
        go(page, "bubbles")
        page.locator("button.bubble").first.click(force=True)
        assert buzz(page) == [], "no vibration once the switch is off"
        go(page, "settings")
        assert not page.locator("input[name=haptics]").is_checked()
        stored = json.loads(page.evaluate("localStorage.getItem('freelief.settings.v1')"))
        assert stored["haptics"] is False


def test_a_device_without_vibration_works_the_same():
    no_vibrate = "Object.defineProperty(navigator, 'vibrate', { configurable: true, value: undefined });"
    with open_app(init_script=no_vibrate) as (page, errors, _):
        go(page, "bubbles")
        page.locator("button.bubble").first.click(force=True)
        go(page, "mandala")
        page.locator(".mandala-part").first.click()
        assert not errors, errors
