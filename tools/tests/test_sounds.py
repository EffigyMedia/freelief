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


def play_music(page):
    page.locator(".sound-choice[data-sound=music]").click()


def go(page, route):
    page.evaluate(f"location.hash = '{route}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 3000)


# Records every buffer source (the breath and the taps): when it starts, when it is told to stop,
# and whether it loops.
NOISE_PROBE = """
window.__src = [];
const createSource = AudioContext.prototype.createBufferSource;
AudioContext.prototype.createBufferSource = function () {
  const node = createSource.call(this);
  const record = { node, start: null, stops: [], ctx: this };
  window.__src.push(record);
  const start = node.start.bind(node), stop = node.stop.bind(node);
  node.start = (when, offset) => { record.start = when ?? this.currentTime; return start(when, offset); };
  node.stop = (when) => { record.stops.push(when ?? this.currentTime); return stop(when); };
  return node;
};
"""
BREATHS = "window.__src.filter(s => s.node.loop)"


def test_each_breath_is_soft_noise_that_lasts_its_whole_phase_and_no_tone():
    # RLG-050 (owner, 2026-10-09): breath noise, not a tone; in and out sound different.
    with open_app(init_script=NOISE_PROBE + PROBE) as (page, _, _):
        page.locator(".guide").click()  # unlock sound; the breath starts with the next phase
        wait_until(page, f"{BREATHS}.length >= 2", 14000)
        lengths = page.evaluate(f"{BREATHS}.slice(0, 2).map(s => s.stops[0] - s.start)")
        assert sorted(round(l) for l in lengths) == sorted([RHYTHM["in"], RHYTHM["out"]]), lengths
        assert page.evaluate("window.__osc.filter(o => o.freq() < 400).length") == 0, "no breathing tone"
        shape = CONFIG["sounds"]["breath"]
        assert shape["in"]["toCutoffHz"] > shape["in"]["fromCutoffHz"], "the in-breath brightens"
        assert shape["out"]["toCutoffHz"] < shape["out"]["fromCutoffHz"], "the out-breath darkens"


def test_pausing_stops_the_breath():
    with open_app(init_script=NOISE_PROBE) as (page, _, _):
        page.locator(".guide").click()
        wait_until(page, f"{BREATHS}.length >= 1", 14000)
        page.locator(".pause").click()
        left = page.evaluate(f"(() => {{ const s = {BREATHS}.at(-1); return s.stops.at(-1) - s.ctx.currentTime; }})()")
        assert left < 1.0, f"the breath keeps going after Pause: {left}"


def test_box_breathing_taps_once_for_each_second_of_a_hold():
    store = "localStorage.setItem('freelief.settings.v2', JSON.stringify({ rhythm: 'box' }));"
    hold = CONFIG["breathing"]["rhythms"]["box"]["holdIn"]
    with open_app(init_script=NOISE_PROBE + store) as (page, _, _):
        page.locator(".guide").click()
        wait_until(page, "window.__src.filter(s => !s.node.loop).length >= " + str(hold), 20000)
        starts = page.evaluate("window.__src.filter(s => !s.node.loop).slice(0, %d).map(s => s.start)" % hold)
        gaps = [round(b - a, 2) for a, b in zip(starts, starts[1:])]
        assert gaps == [1.0] * (hold - 1), f"one tap a second: {gaps}"
        lengths = page.evaluate("window.__src.filter(s => !s.node.loop).slice(0, 2).map(s => s.stops[0] - s.start)")
        assert all(l < 0.2 for l in lengths), f"a tap is short: {lengths}"


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
        page.locator("button.sound-toggle").click()  # the header's sound button, off
        go(page, "trace")
        page.locator("[role=slider]").focus()
        for _ in range(5):
            page.keyboard.press("ArrowRight")
        page.wait_for_timeout(300)
        assert page.evaluate("window.__osc.length") == 0


def test_the_header_sound_button_silences_at_once_and_brings_the_music_back():
    # Owner, 2026-10-08: the sound switch is a speaker in the header, crossed out when off.
    with open_app(init_script=PROBE) as (page, errors, _):
        sound = page.locator("header button.sound-toggle")
        assert sound.get_attribute("aria-label") == "Sound"
        assert sound.get_attribute("aria-pressed") == "true"
        assert sound.locator(".sound-waves").is_visible() and sound.locator(".sound-cross").is_hidden()
        page.locator(".guide").click()  # the first gesture unlocks sound
        play_music(page)
        wait_until(page, "window.__osc.length > 0", 3000)
        sound.click()
        assert sound.get_attribute("aria-pressed") == "false"
        assert sound.locator(".sound-cross").is_visible() and sound.locator(".sound-waves").is_hidden()
        wait_until(page, "window.__osc.at(-1).ctx.state === 'suspended'", 2000)
        before = page.evaluate("window.__osc.length")
        sound.click()
        wait_until(page, f"window.__osc.length > {before}", 3000)  # the music starts again
        wait_until(page, "window.__osc.at(-1).ctx.state === 'running'", 2000)
        assert not errors, errors


def test_the_sound_button_is_reached_by_keyboard_and_settings_has_no_sound_switch():
    with open_app(viewport={"width": 360, "height": 700}) as (page, _, _):
        for _ in range(4):  # music, rain, waves, then the speaker
            page.keyboard.press("Tab")
        assert page.evaluate("document.activeElement.classList.contains('sound-toggle')")
        page.keyboard.press("Enter")
        assert page.locator("button.sound-toggle").get_attribute("aria-pressed") == "false"
        page.keyboard.press("Space")
        assert page.locator("button.sound-toggle").get_attribute("aria-pressed") == "true"
        help_height = page.locator(".help-open").bounding_box()["height"]
        assert help_height < 60, "Need urgent help? stays on one line at 360 px"
        go(page, "settings")
        assert page.locator("input[name=sounds]").count() == 0


def test_the_sound_button_fades_out_and_in_rather_than_cutting():
    # Owner, 2026-10-08: a hard on/off was jarring. Off keeps playing while it fades, then pauses.
    fade = CONFIG["sounds"]["muteFadeSeconds"]
    with open_app(init_script=PROBE) as (page, _, _):
        page.locator(".guide").click()
        play_music(page)
        wait_until(page, "window.__osc.length > 0 && window.__osc.at(-1).ctx.state === 'running'", 3000)
        page.locator("button.sound-toggle").click()
        assert page.evaluate("window.__osc.at(-1).ctx.state") == "running", "no hard cut: it fades first"
        wait_until(page, "window.__osc.at(-1).ctx.state === 'suspended'", int(fade * 1000) + 2000)
        page.locator("button.sound-toggle").click()
        wait_until(page, "window.__osc.at(-1).ctx.state === 'running'", 2000)


def test_music_left_while_muted_does_not_come_back_when_sound_returns():
    # Owner report, 2026-10-08: mute in the Visualizer, leave it, unmute, and the music played and
    # then faded. A sound stopped while muted must be over at once.
    probe = """
window.__gain = [];
const createGain = AudioContext.prototype.createGain;
AudioContext.prototype.createGain = function () {
  const node = createGain.call(this);
  const record = { connected: true };
  window.__gain.push(record);
  const disconnect = node.disconnect.bind(node);
  node.disconnect = (...args) => { record.connected = false; return disconnect(...args); };
  return node;
};"""
    with open_app(init_script=PROBE + probe) as (page, _, _):
        page.locator(".guide").click()
        play_music(page)
        wait_until(page, "window.__osc.length > 0", 3000)
        page.locator("button.sound-toggle").click()
        wait_until(page, "window.__osc.at(-1).ctx.state === 'suspended'", 3000)
        assert page.evaluate("window.__gain.some(g => !g.connected)"),             "the music fading out when the audio paused was cut off, not frozen"
        play_music(page)  # stop it while muted
        go(page, "bubbles")
        stops = page.evaluate("window.__osc.filter(o => o.stop !== null).map(o => o.stop - o.ctx.currentTime)")
        assert stops and max(stops) <= 0.01, f"no stop left scheduled for later: {max(stops)}"



# RLG-046 (owner, 2026-10-09): every sound is diatonic to the music's key, C major (C D E F G A B).
C_MAJOR = {0, 2, 4, 5, 7, 9, 11}  # semitones above C
# Filter corners, a swell rate and a beat rate shape a sound; they are not notes.
# The breath's band moves over a wide, soft band of noise (Q under 1), so it has no pitch.
UNPITCHED = {"noiseHz", "cutoffHz", "lowpassHz", "highpassHz", "swellHz", "beatHz", "troughHz", "crestHz",
             "fromCutoffHz", "toCutoffHz"}
# The bubble pop and the ripple's water drop are natural sounds, so their pitch stays random
# (owner, 2026-10-09).
NATURAL = {"sounds.pop", "sounds.drop"}


def in_c_major(hz, cents=5):
    import math
    semitones = 12 * math.log2(hz / 261.63)
    nearest = round(semitones)
    return nearest % 12 in C_MAJOR and abs(semitones - nearest) * 100 <= cents


def pitches(node, path=""):
    # Every number under a key that names a pitch: *Hz, *note*, *Notes, frequenc*, chords.
    if any(path == n or path.startswith(n + ".") for n in NATURAL):
        return
    if isinstance(node, dict):
        for key, value in node.items():
            yield from pitches(value, f"{path}.{key}" if path else key)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from pitches(value, f"{path}[{i}]")
    elif isinstance(node, (int, float)) and not isinstance(node, bool):
        keys = [part.split("[")[0] for part in path.split(".")]
        if keys[-1] in UNPITCHED:
            return
        if any(k.endswith("Hz") or "note" in k.lower() or k.startswith("frequenc") or k == "chords" for k in keys):
            yield path, node


def test_every_configured_pitch_is_in_c_major():
    found = list(pitches(CONFIG))
    assert len(found) > 40, "the walk found the sound and mandala notes"
    assert any(path.startswith("sounds.rain.dropNotes") for path, _ in found)
    wrong = [(path, hz) for path, hz in found if not in_c_major(hz)]
    assert not wrong, f"not in C major: {wrong}"


def test_the_rain_drops_under_the_music_stay_in_c_major():
    # A test cannot listen, so it records the center of every band-pass filter: the rain's drops.
    probe = """
window.__bands = [];
const create = AudioContext.prototype.createBiquadFilter;
AudioContext.prototype.createBiquadFilter = function () {
  const node = create.call(this);
  setTimeout(() => { if (node.type === "bandpass") window.__bands.push(node.frequency.value); }, 0);
  return node;
};"""
    with open_app(init_script=probe) as (page, errors, _):
        page.locator(".guide").click()
        play_music(page)
        page.locator(".sound-choice[data-sound=rain]").click()
        wait_until(page, "window.__bands.length >= 8", 8000)
        heard = page.evaluate("window.__bands")
        wrong = [hz for hz in heard if not in_c_major(hz)]
        assert not wrong, f"rain drops out of key: {sorted(set(wrong))}"
        assert not errors, errors
