"""Mandala coloring (REQ-033): by touch, by keyboard alone, without sight, at a usable size."""

import json
import time

from harness import ROOT, open_app, wait_until

CONFIG = json.loads((ROOT / "config.json").read_text("utf-8"))
STRINGS = json.loads((ROOT / "strings" / "en.json").read_text("utf-8"))
SETTINGS = CONFIG["mandala"]

OSC_PROBE = """
window.__osc = 0;
const create = AudioContext.prototype.createOscillator;
AudioContext.prototype.createOscillator = function () { window.__osc += 1; return create.call(this); };
"""


def go(page, route):
    page.evaluate(f"location.hash = '{route}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 3000)


def parts_in(design):
    return sum(ring["count"] for ring in SETTINGS["designs"][design])


def fill(locator):
    return locator.evaluate("e => getComputedStyle(e).fill")


def filled(page, locator, name, timeout_ms=2000):
    # The fill fades in over a short transition; wait for the final color.
    want = expected(page, name)
    handle = locator.element_handle()
    deadline = time.monotonic() + timeout_ms / 1000
    while time.monotonic() < deadline:
        if handle.evaluate("e => getComputedStyle(e).fill") == want:
            return True
        time.sleep(0.05)
    return False


def expected(page, name):
    color = next(s["color"] for s in SETTINGS["palette"] if s["name"] == name)
    return page.evaluate(f"(() => {{ const d = document.createElement('div'); d.style.color = '{color}';"
                         "document.body.append(d); const c = getComputedStyle(d).color; d.remove(); return c; })()")


def test_a_tap_fills_a_shape_with_the_chosen_color():
    with open_app() as (page, errors, _):
        go(page, "mandala")
        parts = page.locator(".mandala-part")
        assert parts.count() == parts_in(0)
        assert all(fill(parts.nth(i)) in ("transparent", "rgba(0, 0, 0, 0)") for i in range(parts.count()))
        parts.nth(3).click()
        assert filled(page, parts.nth(3), SETTINGS["palette"][0]["name"])
        page.locator("input[name=mandala-color][value=rose]").check()
        parts.nth(3).click()
        assert filled(page, parts.nth(3), "rose"), "a filled shape takes the new color"
        assert parts.nth(3).get_attribute("aria-label").endswith(STRINGS["mandala.color.rose"])
        assert page.locator(".mandala-status").inner_text() == parts.nth(3).get_attribute("aria-label")
        assert page.locator(".mandala-status").get_attribute("aria-live") == "polite"
        assert not errors, errors


def test_every_shape_has_a_name_and_the_mandala_is_one_tab_stop():
    with open_app() as (page, _, _):
        go(page, "mandala")
        parts = page.locator(".mandala-part")
        labels = parts.evaluate_all("els => els.map(e => e.getAttribute('aria-label'))")
        assert labels[0] == STRINGS["mandala.center"].format(color=STRINGS["mandala.blank"])
        ring1 = SETTINGS["designs"][0][1]["count"]
        assert labels[1] == STRINGS["mandala.part"].format(ring=1, index=1, total=ring1, color=STRINGS["mandala.blank"])
        assert len(set(labels)) == len(labels), "no two shapes share a name"
        assert parts.evaluate_all("els => els.every(e => e.getAttribute('role') === 'button')")
        assert page.locator(".mandala-part[tabindex='0']").count() == 1


def test_the_mandala_can_be_colored_by_keyboard_alone():
    with open_app() as (page, errors, _):
        go(page, "mandala")
        # The color first: arrow keys move through the radio group and choose.
        page.locator("input[name=mandala-color]:checked").focus()
        page.keyboard.press("ArrowRight")
        second = SETTINGS["palette"][1]["name"]
        assert page.locator(f"input[name=mandala-color][value={second}]").is_checked()
        page.keyboard.press("Tab")
        assert page.evaluate("document.activeElement.classList.contains('mandala-part')")
        assert page.evaluate("document.activeElement.dataset.ring") == "0"
        page.keyboard.press("ArrowUp")  # out to ring 1
        page.keyboard.press("ArrowRight")  # around to its second shape
        focused = page.evaluate("[document.activeElement.dataset.ring, document.activeElement.dataset.index]")
        assert focused == ["1", "1"]
        page.keyboard.press("Enter")
        part = page.locator(".mandala-part[data-ring='1'][data-index='1']")
        assert filled(page, part, second)
        page.keyboard.press("ArrowLeft")
        page.keyboard.press("ArrowLeft")
        last = SETTINGS["designs"][0][1]["count"] - 1
        assert page.evaluate("document.activeElement.dataset.index") == str(last), "the ring wraps around"
        page.keyboard.press(" ")
        assert filled(page, page.locator(f".mandala-part[data-ring='1'][data-index='{last}']"), second)
        page.keyboard.press("End")
        assert page.evaluate("document.activeElement.dataset.ring") == str(len(SETTINGS["designs"][0]) - 1)
        page.keyboard.press("Home")
        assert page.evaluate("document.activeElement.dataset.ring") == "0"
        assert not errors, errors


def test_new_mandala_starts_a_blank_new_design():
    with open_app() as (page, _, _):
        go(page, "mandala")
        page.locator(".mandala-part").first.click()
        page.locator(".new-mandala").click()
        parts = page.locator(".mandala-part")
        assert parts.count() == parts_in(1)
        assert all(fill(parts.nth(i)) in ("transparent", "rgba(0, 0, 0, 0)") for i in range(parts.count()))
        assert page.locator(".mandala-status").inner_text() == ""


def test_every_shape_in_every_design_is_a_large_target_on_a_phone():
    with open_app(viewport={"width": 360, "height": 740}) as (page, _, _):
        go(page, "mandala")
        for design in range(len(SETTINGS["designs"])):
            sizes = page.locator(".mandala-part").evaluate_all(
                "els => els.map(e => { const b = e.getBoundingClientRect(); return Math.min(b.width, b.height); })")
            assert min(sizes) >= 24, f"design {design}: smallest shape {min(sizes):.1f}px (WCAG 2.5.8)"
            swatch = page.locator("input[name=mandala-color]").first.bounding_box()
            assert swatch["width"] >= 44 and swatch["height"] >= 44
            page.locator(".new-mandala").click()


def test_each_color_has_its_own_chime_note():
    # Owner, 2026-10-08: each color plays a different note, as a rain chime, when chosen and when filled.
    probe = """
window.__freq = [];
const create = AudioContext.prototype.createOscillator;
AudioContext.prototype.createOscillator = function () {
  const node = create.call(this);
  setTimeout(() => window.__freq.push(node.frequency.value), 0);
  return node;
};"""
    notes = [s["note"] for s in SETTINGS["palette"]]
    assert len(set(notes)) == len(notes), "no two colors share a note"
    with open_app(init_script=probe) as (page, _, _):
        page.locator(".guide").click()
        go(page, "mandala")
        page.wait_for_timeout(300)
        for swatch in SETTINGS["palette"][1:3]:
            page.evaluate("window.__freq = []")
            page.locator(f"input[name=mandala-color][value={swatch['name']}]").check()
            wait_until(page, f"window.__freq.some(f => Math.abs(f - {swatch['note']}) < 0.5)", 2000)
            page.evaluate("window.__freq = []")
            page.locator(".mandala-part").first.click()
            wait_until(page, f"window.__freq.some(f => Math.abs(f - {swatch['note']}) < 0.5)", 2000)


def test_filling_a_shape_plays_the_step_cue():
    with open_app(init_script=OSC_PROBE) as (page, _, _):
        page.locator(".guide").click()  # the first gesture unlocks sound
        go(page, "mandala")
        page.wait_for_timeout(300)
        before = page.evaluate("window.__osc")
        page.locator(".mandala-part").first.click()
        wait_until(page, f"window.__osc > {before}", 2000)
