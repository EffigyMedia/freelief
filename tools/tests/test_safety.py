"""Safety fixes from the design review and round UNT-051 (owner, 2026-10-08): a tappable emergency
number, silence over urgent help and in the background, the screen kept awake, a way to help from
the Visualizer's full screen, and nothing drawn under its black screen."""

import json

from harness import ROOT, open_app, wait_until

CONFIG = json.loads((ROOT / "config.json").read_text("utf-8"))

# Records each audio context that makes a sound: a tone (oscillator) or noise (the breath, a tap).
OSC_PROBE = """
window.__ctx = [];
for (const name of ["createOscillator", "createBufferSource"]) {
  const create = AudioContext.prototype[name];
  AudioContext.prototype[name] = function () {
    if (!window.__ctx.includes(this)) window.__ctx.push(this);
    return create.call(this);
  };
}
"""

WAKE_PROBE = """
window.__wake = { requests: 0, held: 0 };
Object.defineProperty(navigator, 'wakeLock', { configurable: true, value: {
  request: async () => {
    window.__wake.requests += 1; window.__wake.held += 1;
    const sentinel = new EventTarget();
    sentinel.release = async () => { window.__wake.held -= 1; sentinel.dispatchEvent(new Event('release')); };
    return sentinel;
  } } });
"""


def go(page, route):
    page.evaluate(f"location.hash = '{route}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 3000)


def test_the_emergency_number_is_the_first_thing_to_tap():
    with open_app(locale="en-GB") as (page, _, _):
        page.locator(".help-open").click()
        calls = page.locator(".emergency-calls a")
        assert calls.count() == 1 and calls.first.get_attribute("href") == "tel:999"
        assert calls.first.inner_text() == "Call 999"
        first_tel = page.locator("dialog.help a[href^='tel:']").first
        assert first_tel.get_attribute("class").split().count("emergency-call") == 1, "it comes before the lines"
        page.locator("#help-country").select_option("IE")
        assert page.locator(".emergency-calls a").evaluate_all("as => as.map(a => a.getAttribute('href'))") == \
            ["tel:112", "tel:999"], "'112 or 999' gives a button for each"
        page.locator("#help-country").select_option("")
        assert page.locator(".emergency-calls a").count() == 0, "no number is guessed for another country"
        assert page.locator(".directory a").count() == 1


def test_sound_waits_while_urgent_help_is_open_and_while_the_app_is_hidden():
    with open_app(init_script=OSC_PROBE) as (page, errors, _):
        page.locator(".guide").click()  # the first gesture unlocks sound
        page.locator(".sound-choice[data-sound=music]").click()
        wait_until(page, "window.__ctx.length > 0 && window.__ctx[0].state === 'running'", 3000)
        page.locator(".help-open").click()
        wait_until(page, "window.__ctx[0].state === 'suspended'", 2000)
        page.locator("dialog.help .help-back").click()
        wait_until(page, "window.__ctx[0].state === 'running'", 2000)
        hide = """Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => '%s' });
                  document.dispatchEvent(new Event('visibilitychange'));"""
        page.evaluate(hide % "hidden")
        wait_until(page, "window.__ctx[0].state === 'suspended'", 2000)
        page.evaluate(hide % "visible")
        wait_until(page, "window.__ctx[0].state === 'running'", 2000)
        # With sound off, closing help does not bring sound back.
        page.locator("button.sound-toggle").click()
        page.locator(".help-open").click()
        page.locator("dialog.help .help-back").click()
        wait_until(page, "window.__ctx[0].state === 'suspended'", 2000)
        page.wait_for_timeout(300)
        assert page.evaluate("window.__ctx[0].state") == "suspended", "closing help does not bring sound back"
        assert not errors, errors


def test_breathing_and_the_visualizer_keep_the_screen_awake_and_let_it_sleep_after():
    with open_app(init_script=WAKE_PROBE, route="menu") as (page, _, _):
        assert page.evaluate("window.__wake.held") == 0, "the menu lets the screen sleep"
        go(page, "breathe")
        wait_until(page, "window.__wake.held === 1", 2000)
        go(page, "calm")
        wait_until(page, "window.__wake.held === 1 && window.__wake.requests >= 2", 2000)
        go(page, "bubbles")
        wait_until(page, "window.__wake.held === 0", 2000)


def test_full_screen_keeps_a_way_to_urgent_help():
    with open_app() as (page, _, _):
        go(page, "calm")
        assert page.locator(".calm-help").is_hidden()
        page.locator(".full-screen").click()
        helper = page.locator(".calm-help")
        assert helper.is_visible() and helper.inner_text() == "Need urgent help?"
        helper.click()
        assert page.locator("dialog.help").evaluate("d => d.open")
        assert "full" not in page.locator(".calm-stage").get_attribute("class")


def test_nothing_is_drawn_under_the_black_screen_and_one_tap_brings_help_back():
    fast = 300  # the probe shortens the time between patterns to this
    probe = """
const realTimeout = window.setTimeout.bind(window);
window.setTimeout = (callback, ms, ...rest) => realTimeout(callback, ms >= 15000 ? 300 : ms, ...rest);
"""
    with open_app(init_script=probe) as (page, _, _):
        go(page, "calm")
        page.locator(".black-screen").click()
        assert "asleep" in page.locator(".calm-stage").get_attribute("class")
        assert page.locator(".calm-field").evaluate("e => getComputedStyle(e).visibility") == "hidden"
        page.wait_for_timeout(500)
        before = page.evaluate("document.querySelectorAll('.kaleido-layer').length")
        page.wait_for_timeout(int(fast * 4))
        after = page.evaluate("document.querySelectorAll('.kaleido-layer').length")
        assert after <= before, "no new pattern is drawn while the screen is black"
        page.locator(".black-cover").click()
        assert "asleep" not in page.locator(".calm-stage").get_attribute("class")
        assert page.locator(".help-open").is_visible(), "one tap from black, help is in reach again"


# AUD-103 (owner, 2026-10-09): the screen may sleep after a time with no touch, chosen in Settings.
# The probe shortens any wait of ten minutes or more to a moment, so the test does not wait.
SHORT_WAITS = """
const realTimeout = window.setTimeout.bind(window);
window.setTimeout = (callback, ms, ...rest) => realTimeout(callback, ms >= 600000 ? 400 : ms, ...rest);
"""


def test_the_screen_may_sleep_after_the_idle_time_and_a_touch_keeps_it_on_again():
    with open_app(init_script=WAKE_PROBE + SHORT_WAITS, route="menu") as (page, _, _):
        go(page, "calm")
        wait_until(page, "window.__wake.held === 1", 2000)
        wait_until(page, "window.__wake.held === 0", 3000)  # no touch for the idle time
        page.locator("h1").click()
        wait_until(page, "window.__wake.held === 1", 2000)


def test_pausing_breathing_lets_the_screen_sleep_and_resuming_keeps_it_on():
    with open_app(init_script=WAKE_PROBE) as (page, _, _):
        wait_until(page, "window.__wake.held === 1", 2000)
        page.locator(".pause").click()
        wait_until(page, "window.__wake.held === 0", 2000)
        page.locator(".pause").click()
        wait_until(page, "window.__wake.held === 1", 2000)


def test_the_screen_on_time_is_a_setting_that_is_kept():
    with open_app(route="settings") as (page, _, _):
        assert page.locator("input[name=awakeMinutes][value='30']").is_checked()
        page.locator("input[name=awakeMinutes][value='60']").check()
        page.reload()
        wait_until(page, "document.documentElement.dataset.ready === 'true'", 5000)
        assert page.locator("input[name=awakeMinutes][value='60']").is_checked(), "saved, reloaded, read"


def test_a_wake_lock_granted_after_leaving_is_let_go_at_once():
    # AUD-081: a lock granted late, after the screen left breathing, must not keep the screen on.
    slow = """
window.__wake = { held: 0 };
Object.defineProperty(navigator, 'wakeLock', { configurable: true, value: {
  request: () => new Promise((resolve) => setTimeout(() => {
    window.__wake.held += 1;
    const sentinel = new EventTarget();
    sentinel.release = async () => { window.__wake.held -= 1; };
    resolve(sentinel);
  }, 500)) } });
"""
    with open_app(init_script=slow, route="menu") as (page, _, _):
        go(page, "breathe")
        go(page, "menu")  # leave before the lock is granted
        page.wait_for_timeout(900)
        assert page.evaluate("window.__wake.held") == 0


def test_a_breathing_tone_does_not_wake_the_audio_while_urgent_help_is_open():
    # AUD-082: a cue must not resume the paused audio behind the crisis lines.
    with open_app(init_script=OSC_PROBE) as (page, _, _):
        page.locator(".guide").click()
        wait_until(page, "window.__ctx.length > 0 && window.__ctx[0].state === 'running'", 9000)
        page.locator(".help-open").click()
        wait_until(page, "window.__ctx[0].state === 'suspended'", 2000)
        page.wait_for_timeout(7000)  # more than one breathing phase
        assert page.evaluate("window.__ctx[0].state") == "suspended"


def test_always_keeps_the_screen_on_with_no_idle_end():
    # RLG-048 (owner, 2026-10-09): "Always, while it runs" sets no idle time.
    store = "localStorage.setItem('freelief.settings.v2', JSON.stringify({ awakeMinutes: 0 }));"
    with open_app(init_script=WAKE_PROBE + SHORT_WAITS + store, route="menu") as (page, _, _):
        go(page, "calm")
        wait_until(page, "window.__wake.held === 1", 2000)
        page.wait_for_timeout(1500)  # past the shortened idle time of the other choices
        assert page.evaluate("window.__wake.held") == 1
        go(page, "settings")
        assert page.locator("input[name=awakeMinutes][value='0']").is_checked()
