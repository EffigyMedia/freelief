"""Slice 2 in a real browser: grounding, calming words, settings, rhythm presets, tones, themes."""

import json

from harness import ROOT, open_app, wait_until

STRINGS = json.loads((ROOT / "strings" / "en.json").read_text("utf-8"))

# Counts AudioContext oscillators, so a test can see that a tone was asked for without hearing it.
TONE_PROBE = """
window.__tones = 0;
const original = AudioContext.prototype.createOscillator;
AudioContext.prototype.createOscillator = function () {
  window.__tones += 1;
  return original.call(this);
};
"""

BLOCKED_STORAGE = """
Object.defineProperty(window, 'localStorage', {
  get() { throw new DOMException('blocked', 'SecurityError'); }
});
"""


def go(page, route):
    page.evaluate(f"location.hash = '{route}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 2000)


def test_the_menu_is_home_and_reaches_every_screen_by_keyboard():
    # REQ-018 as changed 2026-10-07: Freelief opens on the menu, and every screen goes back to it.
    with open_app(route=None) as (page, errors, _):
        assert page.evaluate("document.querySelector('main').dataset.shown") == "menu"
        hrefs = page.locator(".menu-item").evaluate_all("els => els.map(e => e.getAttribute('href'))")
        assert hrefs == ["#breathe", "#ground", "#statements", "#bubbles", "#trace", "#sort", "#calm"]
        page.locator(".menu-item").first.focus()
        page.keyboard.press("Enter")
        wait_until(page, "document.querySelector('main').dataset.shown === 'breathe'", 2000)
        assert page.evaluate("document.activeElement.tagName") == "H1", "focus moves to the new screen"
        page.locator(".nav-back").click()
        wait_until(page, "document.querySelector('main').dataset.shown === 'menu'", 2000)
        assert not errors, errors


def test_the_settings_gear_is_at_the_top_right_on_every_screen():
    with open_app(route=None, viewport={"width": 360, "height": 640}) as (page, _, _):
        for screen in ("menu", "breathe", "calm", "about"):
            go(page, screen)
            gear = page.locator("a.gear")
            assert gear.get_attribute("aria-label") == "Settings", screen
            box = gear.bounding_box()
            assert box["x"] + box["width"] > 360 - 40 and box["y"] < 60, f"{screen}: gear at {box}"
        page.locator("a.gear").click()
        wait_until(page, "document.querySelector('main').dataset.shown === 'settings'", 2000)


def test_grounding_walks_five_steps_and_back():
    with open_app() as (page, _, _):
        go(page, "ground")
        prompt = page.locator(".prompt")
        assert prompt.inner_text() == STRINGS["ground.5"]
        assert page.locator(".previous").is_hidden()
        next_button = page.locator(".next")
        next_button.focus()
        for step in ("4", "3", "2", "1"):
            page.keyboard.press("Enter")
            assert prompt.inner_text() == STRINGS[f"ground.{step}"]
        page.keyboard.press("Enter")
        assert prompt.inner_text() == STRINGS["ground.done"]
        assert next_button.inner_text() == STRINGS["ground.again"]
        page.locator(".previous").click()
        assert prompt.inner_text() == STRINGS["ground.1"]
        assert prompt.get_attribute("aria-live") == "polite"


def test_calming_words_advance_and_wrap():
    with open_app() as (page, _, _):
        go(page, "statements")
        statements = STRINGS["statements.list"]
        text = page.locator(".statement")
        assert text.inner_text() == statements[0]
        page.locator(".next").click()
        assert text.inner_text() == statements[1]
        page.locator(".previous").click()
        page.locator(".previous").click()
        assert text.inner_text() == statements[-1], "the list wraps; there is no end"


def test_settings_round_trip_through_a_reload():
    # AGENTS.md: settings round-trip in a test. Save, reload, read, assert the same values.
    with open_app() as (page, _, _):
        go(page, "settings")
        page.locator("input[name=rhythm][value=box]").check()
        page.locator("input[name=theme][value=light]").check()
        page.locator("input[name=sounds]").uncheck()
        page.reload()
        wait_until(page, "document.documentElement.dataset.ready === 'true'")
        go(page, "settings")
        assert page.locator("input[name=rhythm][value=box]").is_checked()
        assert page.locator("input[name=theme][value=light]").is_checked()
        assert not page.locator("input[name=sounds]").is_checked()
        assert page.evaluate("document.documentElement.dataset.theme") == "light"
        stored = json.loads(page.evaluate("localStorage.getItem('freelief.settings.v1')"))
        assert stored == {"rhythm": "box", "sounds": False, "theme": "light", "calmMode": "music"}


def test_blocked_storage_falls_back_to_defaults():
    with open_app(init_script=BLOCKED_STORAGE) as (page, errors, _):
        assert page.locator(".guide").is_visible()
        go(page, "settings")
        assert page.locator("input[name=rhythm][value=calm]").is_checked()
        page.locator("input[name=rhythm][value=slow]").check()
        go(page, "breathe")
        assert not [e for e in errors if "blocked" not in e], errors


def test_box_rhythm_holds_after_the_in_breath():
    with open_app() as (page, _, _):
        go(page, "settings")
        page.locator("input[name=rhythm][value=box]").check()
        go(page, "breathe")
        wait_until(page, "document.querySelector('.phase').textContent === 'Hold'", 6000)


def test_sounds_are_on_by_default_after_a_tap_and_silent_when_off():
    # REQ-007 as changed 2026-10-07: sounds are on by default; one switch turns them all off.
    # Browsers allow sound only after a gesture, so nothing plays before the first tap.
    with open_app(init_script=TONE_PROBE) as (page, errors, _):
        page.wait_for_timeout(1200)
        assert page.evaluate("window.__tones") == 0, "nothing plays before the first tap"
        page.locator(".guide").click()
        wait_until(page, "window.__tones >= 1", 7000)
        go(page, "settings")
        assert page.locator("input[name=sounds]").is_checked()
        page.locator("input[name=sounds]").uncheck()
        go(page, "bubbles")
        before = page.evaluate("window.__tones")
        page.locator("button.bubble").first.click(force=True)
        page.wait_for_timeout(300)
        assert page.evaluate("window.__tones") == before, "no sound once the switch is off"
        assert not [e for e in errors if "AudioContext" in e], errors


def test_each_activity_plays_its_cue():
    with open_app(init_script=TONE_PROBE) as (page, _, _):
        page.locator(".guide").click()  # the first gesture unlocks sound
        for route, action in (("bubbles", lambda: page.locator("button.bubble").first.click(force=True)),
                              ("ground", lambda: page.locator(".next").click()),
                              ("statements", lambda: page.locator(".next").click())):
            go(page, route)
            before = page.evaluate("window.__tones")
            action()
            wait_until(page, f"window.__tones > {before}", 2000)

def test_dark_override_beats_a_light_device():
    with open_app(color_scheme="light") as (page, _, _):
        light = page.evaluate("getComputedStyle(document.body).backgroundColor")
        go(page, "settings")
        page.locator("input[name=theme][value=dark]").check()
        dark = page.evaluate("getComputedStyle(document.body).backgroundColor")
        assert light != dark
        assert dark == "rgb(15, 22, 38)"
