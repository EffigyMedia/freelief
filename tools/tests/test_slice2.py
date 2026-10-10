"""Slice 2 in a real browser: the menu, settings, rhythm presets, tones, themes."""

import json

from harness import ROOT, open_app, wait_until

CONFIG = json.loads((ROOT / "config.json").read_text("utf-8"))

STRINGS = json.loads((ROOT / "strings" / "en.json").read_text("utf-8"))

# Counts AudioContext oscillators, so a test can see that a tone was asked for without hearing it.
# Counts every sound made: a tone (oscillator) or noise (the breath since RLG-050, a pop, a tap).
TONE_PROBE = """
window.__tones = 0;
for (const name of ["createOscillator", "createBufferSource"]) {
  const original = AudioContext.prototype[name];
  AudioContext.prototype[name] = function () {
    window.__tones += 1;
    return original.call(this);
  };
}
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
        assert hrefs == ["#breathe", "#bubbles", "#garden", "#ripple", "#mandala", "#unblock", "#calm"]
        page.locator(".menu-item").first.focus()
        page.keyboard.press("Enter")
        wait_until(page, "document.querySelector('main').dataset.shown === 'breathe'", 2000)
        assert page.evaluate("document.activeElement.tagName") == "H1", "focus moves to the new screen"
        page.locator(".nav-back").click()
        wait_until(page, "document.querySelector('main').dataset.shown === 'menu'", 2000)
        assert not errors, errors


def test_the_header_is_three_centered_rows_on_every_screen():
    # Owner, 2026-10-09 (RLG-049): the name; music, rain, waves, sound and Settings; then urgent help.
    with open_app(route=None, viewport={"width": 360, "height": 640}) as (page, _, _):
        for screen in ("menu", "breathe", "calm", "about"):
            go(page, screen)
            gear = page.locator("a.gear")
            assert gear.get_attribute("aria-label") == "Settings", screen
            rows = [page.locator(sel).bounding_box() for sel in (".brand", ".top-actions", ".help-open")]
            assert rows[0]["y"] + rows[0]["height"] <= rows[1]["y"] + 1, f"{screen}: the name is above the buttons"
            assert rows[1]["y"] + rows[1]["height"] <= rows[2]["y"] + 1, f"{screen}: urgent help is the third line"
            for box in rows:
                middle = box["x"] + box["width"] / 2
                assert abs(middle - 180) <= 2, f"{screen}: a row is not centered: {box}"
        page.locator("a.gear").click()
        wait_until(page, "document.querySelector('main').dataset.shown === 'settings'", 2000)



def test_a_save_keeps_the_settings_this_version_cannot_read():
    # AUD-121: after a rollback, an older version must not erase a newer version's choices at its
    # next save. A stored name it does not know, or a value it does not know, is written back.
    key = CONFIG["settings"]["storageKey"]
    seed = json.dumps({"fromNewerVersion": "kept", "awakeMinutes": 999, "rhythm": "slow"})
    store = f"if (!localStorage.getItem('{key}')) localStorage.setItem('{key}', JSON.stringify({seed}));"
    stored = f"JSON.parse(localStorage.getItem('{key}'))"
    with open_app(init_script=store) as (page, _, _):
        go(page, "settings")
        assert page.locator("input[name=rhythm][value=slow]").is_checked(), "a known value is read"
        page.locator("input[name=theme][value=light]").check()
        saved = page.evaluate(stored)
        assert saved["fromNewerVersion"] == "kept" and saved["awakeMinutes"] == 999, saved
        assert saved["theme"] == "light" and saved["rhythm"] == "slow", saved
        default = CONFIG["wakeLock"]["idleMinutesDefault"]
        other = next(m for m in CONFIG["wakeLock"]["idleMinutesChoices"] if m != default)
        page.locator(f"input[name=awakeMinutes][value='{other}']").check()
        page.locator(f"input[name=awakeMinutes][value='{default}']").check()
        saved = page.evaluate(stored)
        assert "awakeMinutes" not in saved, f"a new choice replaces the unknown value: {saved}"
        assert saved["fromNewerVersion"] == "kept", saved

def test_settings_round_trip_through_a_reload():
    # AGENTS.md: settings round-trip in a test. Save, reload, read, assert the same values.
    with open_app() as (page, _, _):
        go(page, "settings")
        page.locator("input[name=rhythm][value=slow]").check()  # not the default, so the save shows
        page.locator("input[name=theme][value=light]").check()
        page.locator("button.sound-toggle").click()
        page.locator("#help-region").select_option("IE")
        page.locator("input[name=haptics]").uncheck()
        page.reload()
        wait_until(page, "document.documentElement.dataset.ready === 'true'")
        go(page, "settings")
        assert page.locator("input[name=rhythm][value=slow]").is_checked()
        assert page.locator("input[name=theme][value=light]").is_checked()
        assert page.locator("#help-region").input_value() == "IE"
        assert not page.locator("input[name=haptics]").is_checked()
        assert page.locator("button.sound-toggle").get_attribute("aria-pressed") == "false"
        assert page.evaluate("document.documentElement.dataset.theme") == "light"
        stored = json.loads(page.evaluate("localStorage.getItem('freelief.settings.v2')"))
        # Only the five changed settings are stored; the Visualizer's sound was never touched.
        assert stored == {"rhythm": "slow", "sounds": False, "theme": "light",
                          "helpRegion": "IE", "haptics": False}


def test_blocked_storage_falls_back_to_defaults():
    with open_app(init_script=BLOCKED_STORAGE) as (page, errors, _):
        assert page.locator(".guide").is_visible()
        go(page, "settings")
        default = CONFIG["breathing"]["defaultRhythm"]
        assert default == "calm", "owner, 2026-10-08: the long breath out the research favors"
        assert page.locator(f"input[name=rhythm][value={default}]").is_checked()
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
        sound = page.locator("button.sound-toggle")
        assert sound.get_attribute("aria-pressed") == "true"
        sound.click()
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
                              ("unblock", lambda: page.locator(".unblock-block").first.click())):
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


def test_only_a_changed_setting_is_stored_so_a_new_default_still_arrives():
    # AUD-062: a setting the person never touched follows the default of the running version.
    with open_app() as (page, _, _):
        go(page, "settings")
        page.locator("input[name=theme][value=light]").check()
        stored = json.loads(page.evaluate("localStorage.getItem('freelief.settings.v2')"))
        assert stored == {"theme": "light"}


V1_STORE = """
localStorage.setItem('freelief.settings.v1', JSON.stringify(
  { rhythm: 'box', sounds: true, theme: 'dark', helpRegion: 'auto', haptics: false }));
"""


def test_an_old_store_keeps_only_real_choices_and_drops_the_box_era_rhythm():
    with open_app(init_script="if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1');"
                  + V1_STORE + "}") as (page, _, _):
        stored = json.loads(page.evaluate("localStorage.getItem('freelief.settings.v2')"))
        assert stored == {"theme": "dark", "haptics": False}, "only values that differ from today's defaults"
        assert page.evaluate("localStorage.getItem('freelief.settings.v1')") is None, "the old store is removed"
        go(page, "settings")
        assert page.locator(f"input[name=rhythm][value={CONFIG['breathing']['defaultRhythm']}]").is_checked()
        assert page.locator("input[name=theme][value=dark]").is_checked()


def test_breathe_stands_out_and_freelief_can_open_on_breathing():
    # Owner, 2026-10-08 (design review): Breathe is the first help; Settings can make it the start.
    with open_app(route=None) as (page, _, _):
        first = page.locator(".menu-item").first
        assert first.get_attribute("href") == "#breathe" and "menu-item-first" in first.get_attribute("class")
        size = lambda i: page.locator(".menu-label").nth(i).evaluate("e => parseFloat(getComputedStyle(e).fontSize)")
        assert size(0) > size(1), "the Breathe card is larger"
        assert page.evaluate("document.querySelector('main').dataset.shown") == "menu"
        go(page, "settings")
        assert page.locator("input[name=openOn][value=menu]").is_checked()
        page.locator("input[name=openOn][value=breathe]").focus()
        page.keyboard.press("Space")
        page.goto(page.url.split("#")[0])
        page.wait_for_selector("html[data-ready='true']")
        wait_until(page, "document.querySelector('main').dataset.shown === 'breathe'", 3000)
        page.evaluate("location.hash = 'nothing-here'")
        wait_until(page, "document.querySelector('main').dataset.shown === 'menu'", 3000)


def test_the_rhythm_shows_under_the_breathing_circle():
    # Design review, 2026-10-08: the person sees how long each phase lasts.
    with open_app() as (page, _, _):
        go(page, "breathe")
        assert page.locator(".rhythm-line").inner_text() == "In 4 · Out 6"
        go(page, "settings")
        page.locator("input[name=rhythm][value=box]").check()
        go(page, "breathe")
        assert page.locator(".rhythm-line").inner_text() == "In 4 · Hold 4 · Out 4 · Rest 4"


def test_an_inherited_name_in_storage_is_ignored():
    # AUD-030: a stored "constructor" rhythm once broke the guide.
    seed = ("localStorage.setItem('freelief.settings.v2', JSON.stringify("
            "{ rhythm: 'constructor', theme: '__proto__', openOn: 'hasOwnProperty' }));")
    with open_app(init_script=seed, route=None) as (page, errors, _):
        assert page.evaluate("document.querySelector('main').dataset.shown") == "menu"
        go(page, "breathe")
        wait_until(page, "document.querySelector('.phase').textContent.trim().length > 0", 3000)
        assert page.locator(".rhythm-line").inner_text() == "In 4 · Out 6", "the default rhythm runs"
        assert not errors, errors


def test_reset_settings_brings_back_every_default_and_a_default_choice_is_not_stored():
    # AUD-110: the person can reset Settings, and choosing a default again does not pin it.
    with open_app(route="settings") as (page, _, _):
        page.locator("input[name=rhythm][value=slow]").check()
        page.locator("input[name=theme][value=light]").check()
        stored = page.evaluate("JSON.parse(localStorage.getItem('freelief.settings.v2'))")
        assert stored == {"rhythm": "slow", "theme": "light"}
        page.locator("input[name=theme][value=system]").check()
        stored = page.evaluate("JSON.parse(localStorage.getItem('freelief.settings.v2'))")
        assert stored == {"rhythm": "slow"}, "choosing the default again stores nothing"
        page.locator(".reset-settings").click()
        assert page.locator(".reset-confirm").is_visible(), "one tap asks first"
        page.locator(".reset-no").click()
        assert page.locator(".reset-confirm").is_hidden()
        assert page.evaluate("JSON.parse(localStorage.getItem('freelief.settings.v2'))") == {"rhythm": "slow"}
        page.locator(".reset-settings").click()
        page.locator(".reset-yes").click()
        wait_until(page, f"document.querySelector('.reset-status').textContent === {STRINGS['settings.resetDone']!r}", 2000)
        assert page.evaluate("localStorage.getItem('freelief.settings.v2')") == "{}"
        page.reload()
        wait_until(page, "document.documentElement.dataset.ready === 'true'", 5000)
        assert page.locator("input[name=rhythm][value=calm]").is_checked(), "saved, reloaded, read"


def test_settings_says_whether_this_version_is_ready_offline():
    # AUD-112: a person who installs Freelief for a future crisis can see that it works offline.
    with open_app(route="settings", service_workers="allow") as (page, _, _):
        page.evaluate("navigator.serviceWorker.ready")
        wait_until(page, "caches.has('freelief-' + self.FREELIEF_VERSION)", 8000)
        page.reload()
        wait_until(page, "document.documentElement.dataset.ready === 'true'", 5000)
        wait_until(page, f"document.querySelector('.offline-state').textContent === {STRINGS['settings.offlineReady']!r}", 3000)
    with open_app(route="settings") as (page, _, _):
        wait_until(page, f"document.querySelector('.offline-state').textContent === {STRINGS['settings.offlineNotReady']!r}", 3000)
