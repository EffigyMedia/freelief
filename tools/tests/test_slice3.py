"""Slice 3 in a real browser: the bubble field and the shape trace (REQ-012, REQ-013)."""

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
        assert toggle.get_attribute("aria-pressed") == "true"
        assert toggle.inner_text() == STRINGS["bubbles.resumeMotion"]
        assert page.locator("button.bubble.held").count() == CONFIG["bubbles"]["count"]


def test_bubbles_are_still_under_reduced_motion():
    with open_app(reduced_motion="reduce") as (page, _, _):
        go(page, "bubbles")
        assert page.locator("button.bubble.drifting").count() == 0
        assert page.locator(".motion-toggle").is_hidden()
        page.locator("button.bubble").first.click()
        assert page.locator("button.bubble").count() == CONFIG["bubbles"]["count"] - 1


def test_trace_moves_by_keyboard_and_notes_a_full_loop():
    with open_app() as (page, _, _):
        go(page, "trace")
        slider = page.locator("[role=slider]")
        slider.focus()
        assert slider.get_attribute("aria-valuenow") == "0"
        page.keyboard.press("ArrowRight", )
        assert int(slider.get_attribute("aria-valuenow")) > 0
        assert "percent around the loop" in slider.get_attribute("aria-valuetext")
        page.keyboard.press("ArrowLeft")
        assert slider.get_attribute("aria-valuenow") == "0"
        for _ in range(100):
            page.keyboard.press("ArrowRight")
        assert page.locator(".trace-loops").inner_text() == STRINGS["trace.oneLoop"]


def test_trace_follows_a_pointer_along_the_shape():
    with open_app() as (page, _, _):
        go(page, "trace")
        marker = page.locator(".trace-marker")
        start = marker.bounding_box()
        x, y = start["x"] + start["width"] / 2, start["y"] + start["height"] / 2
        page.mouse.move(x, y)
        page.mouse.down()
        # The loop starts at the right end of the eight and runs down and to the left first.
        for i in range(1, 13):
            page.mouse.move(x - i * 6, y + i * 3)
        page.mouse.up()
        assert int(page.locator("[role=slider]").get_attribute("aria-valuenow")) > 0


def test_new_shape_moves_through_every_shape_and_each_can_be_traced():
    shapes = CONFIG["trace"]["shapes"]
    assert len(shapes) >= 10, "many shapes (owner, 2026-10-07)"
    with open_app() as (page, errors, _):
        go(page, "trace")
        seen = []
        for shape in shapes:
            name = page.locator(".trace-name").inner_text()
            assert name == f"Shape: {STRINGS['trace.shape.' + shape['id']]}"
            d = page.locator(".trace-shape").get_attribute("d")
            assert d.startswith("M") and "NaN" not in d, shape["id"]
            seen.append(d)
            slider = page.locator("[role=slider]")
            slider.focus()
            for _ in range(10):
                page.keyboard.press("ArrowRight")
            assert int(slider.get_attribute("aria-valuenow")) >= 9, shape["id"]
            page.locator(".new-shape").click()
        assert len(set(seen)) == len(shapes), "every shape is different"
        assert page.locator(".trace-name").inner_text().endswith(STRINGS["trace.shape." + shapes[0]["id"]]), \
            "after the last shape comes the first again"
        assert not errors, errors