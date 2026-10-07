"""Sounds (REQ-007 as changed 2026-10-07). A test cannot listen, so it reads the Web Audio graph:
when each oscillator starts, when it is told to stop, and how many are live."""

import json

from harness import ROOT, open_app, wait_until

CONFIG = json.loads((ROOT / "config.json").read_text("utf-8"))

# Records every oscillator's planned start and stop, relative to the audio clock.
PROBE = """
window.__osc = [];
const create = AudioContext.prototype.createOscillator;
AudioContext.prototype.createOscillator = function () {
  const node = create.call(this);
  const record = { freq: () => node.frequency.value, start: null, stop: null, ctx: this };
  window.__osc.push(record);
  const start = node.start.bind(node), stop = node.stop.bind(node);
  node.start = (when) => { record.start = (when ?? this.currentTime); return start(when); };
  node.stop = (when) => { record.stop = (when ?? this.currentTime); return stop(when); };
  return node;
};
"""

RHYTHM = CONFIG["breathing"]["rhythms"][CONFIG["breathing"]["defaultRhythm"]]


def go(page, route):
    page.evaluate(f"location.hash = '{route}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 3000)


def test_a_breathing_tone_lasts_its_whole_phase():
    with open_app(init_script=PROBE) as (page, _, _):
        page.locator(".guide").click()  # unlock sound; the tone starts with the next phase
        wait_until(page, "window.__osc.length >= 2", 12000)
        lengths = page.evaluate("window.__osc.slice(0, 2).map(o => o.stop - o.start)")
        phase = page.evaluate("document.querySelector('.phase').textContent")
        expected = RHYTHM["out"] if phase == "Breathe out" else RHYTHM["in"]
        for length in lengths:
            assert abs(length - expected) < 0.2, f"tone lasts {length:.2f} s, phase lasts {expected} s"


def test_pausing_stops_the_breathing_tone():
    with open_app(init_script=PROBE) as (page, _, _):
        page.locator(".guide").click()
        wait_until(page, "window.__osc.length >= 2", 12000)
        page.locator(".pause").click()
        early = page.evaluate("""window.__osc.slice(0, 2)
            .map(o => o.stop - o.ctx.currentTime)""")
        assert all(left < 1.0 for left in early), f"tone keeps going after Pause: {early}"


def test_the_glass_sings_while_tracing_and_stops_on_leaving():
    with open_app(init_script=PROBE) as (page, _, _):
        go(page, "trace")
        slider = page.locator("[role=slider]")
        slider.focus()
        for _ in range(5):
            page.keyboard.press("ArrowRight")
        glass = CONFIG["sounds"]["glass"]
        partials = len(glass["partials"]) * 2
        wait_until(page, f"window.__osc.length >= {partials}", 2000)
        assert page.evaluate("window.__osc.every(o => o.stop === null)"), "the glass sustains while moving"
        go(page, "breathe")
        assert page.evaluate(f"window.__osc.slice(0, {partials}).every(o => o.stop !== null)"), \
            "leaving the screen stops the glass"


def test_sounds_off_means_no_glass():
    with open_app(init_script=PROBE) as (page, _, _):
        go(page, "settings")
        page.locator("input[name=sounds]").uncheck()
        go(page, "trace")
        page.locator("[role=slider]").focus()
        for _ in range(5):
            page.keyboard.press("ArrowRight")
        page.wait_for_timeout(300)
        assert page.evaluate("window.__osc.length") == 0
