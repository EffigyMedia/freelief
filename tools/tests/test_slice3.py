"""Slice 3 in a real browser: the bubble field (REQ-012). The shape trace was replaced by Zen Garden
(RLG-055); its tests are in test_garden.py."""

import json

from harness import ROOT, open_app, wait_until

CONFIG = json.loads((ROOT / "config.json").read_text("utf-8"))
STRINGS = json.loads((ROOT / "strings" / "en.json").read_text("utf-8"))


def go(page, route):
    page.evaluate(f"location.hash = '{route}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 2000)


def test_a_popped_bubble_is_replaced_and_nothing_is_scored():
    with open_app() as (page, errors, _):
        go(page, "bubbles")
        bubbles = page.locator("button.bubble")
        assert bubbles.count() == CONFIG["bubbles"]["count"]
        # A drifting bubble is never "stable", so Playwright's normal click would wait forever.
        bubbles.first.click(force=True)
        wait_until(page, f"document.querySelectorAll('button.bubble').length === {CONFIG['bubbles']['count']}"
                   " && !document.querySelector('.popping')", 4000)
        text = page.locator("main").inner_text().lower()
        assert "score" not in text and "points" not in text
        assert not errors, errors


def test_bubbles_pop_by_keyboard_and_focus_stays_in_the_field():
    with open_app() as (page, _, _):
        go(page, "bubbles")
        page.locator("button.bubble").first.focus()
        page.keyboard.press("Enter")
        wait_until(page, "!document.querySelector('.popping')", 2000)
        assert page.evaluate("document.activeElement.classList.contains('bubble')"), \
            "focus moves to another bubble after a pop"
        page.keyboard.press("Space")
        wait_until(page, "!document.querySelector('.popping')", 2000)
        assert page.evaluate("document.activeElement.classList.contains('bubble')")


def test_bubble_drift_can_be_stopped():
    # WCAG 2.2.2: movement that lasts over 5 seconds can be paused.
    with open_app() as (page, _, _):
        go(page, "bubbles")
        toggle = page.locator(".motion-toggle")
        assert page.locator("button.bubble.drifting").count() == CONFIG["bubbles"]["count"]
        toggle.click()
        assert toggle.get_attribute("aria-pressed") is None, "RLG-047: the label alone says the state"
        assert toggle.inner_text() == STRINGS["bubbles.resumeMotion"]
        assert page.locator("button.bubble.held").count() == CONFIG["bubbles"]["count"]


def test_bubbles_are_still_under_reduced_motion():
    with open_app(reduced_motion="reduce") as (page, _, _):
        go(page, "bubbles")
        assert page.locator("button.bubble.drifting").count() == 0
        assert page.locator(".motion-toggle").is_hidden()
        page.locator("button.bubble").first.click()
        assert page.locator("button.bubble").count() == CONFIG["bubbles"]["count"] - 1


def test_tab_reaches_the_bubbles_in_reading_order():
    # RLG-047: the page order of the bubbles is their slot order, so Tab follows what a person sees.
    with open_app(reduced_motion="reduce") as (page, _, _):  # still bubbles, so a click lands
        go(page, "bubbles")
        for _ in range(4):
            page.locator("button.bubble").first.click()
            page.wait_for_timeout(CONFIG["bubbles"]["popMs"] + CONFIG["bubbles"]["respawnMs"] + 200)
        slots = page.evaluate("[...document.querySelectorAll('.bubble-field li')].map(li => Number(li.dataset.slot))")
        assert slots == sorted(slots), f"the bubbles are out of reading order: {slots}"
