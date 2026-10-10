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
        # The rings are drawn by the water's grid of dots (RLG-041): dots near the ring light up.
        wave = SETTINGS["wave"]
        lit = f"[...document.querySelectorAll('.pond-field circle')].filter(c => +c.getAttribute('opacity') > {wave['restLevel'] + 0.3}).length"
        wait_until(page, f"{lit} > 10", 2000)
        assert page.locator(".pond-field").get_attribute("aria-hidden") == "true"
        life = SETTINGS["lifeSeconds"] + SETTINGS["rings"] * SETTINGS["ringGapSeconds"]
        wait_until(page, "document.querySelectorAll('.pond .ripple-set').length === 0", int(life * 1000) + 1500)
        wait_until(page, f"{lit} === 0", 1500)  # the water is still again
        assert not errors, errors


def test_the_waves_add_where_crests_meet_and_cancel_where_a_crest_meets_a_trough():
    # RLG-041: the water's height is the sum of the ripples' waves, so the rings interfere.
    with open_app() as (page, _, _):
        go(page, "ripple")
        result = page.evaluate("""(async () => {
            const { waveHeight } = await import('./activities/ripple.js');
            const config = await (await fetch('config.json')).json();
            const wave = config.ripple.wave;
            const age = 1.5, front = wave.speed * age;  // the crest of each packet is here
            const a = { x: 0, y: 0, born: 0 }, b = { x: 2 * front, y: 0, born: 0 };
            const one = (s, x, y) => waveHeight([s], x, y, age, wave);
            const both = (x, y) => waveHeight([a, b], x, y, age, wave);
            // Midway between the sources, both crests arrive together.
            const mid = [front, 0];
            const half = wave.wavelength / 2;
            const sum = [[13, 7], [front, 20], [40, -30]].every(([x, y]) =>
                Math.abs(both(x, y) - (one(a, x, y) + one(b, x, y))) < 1e-9);
            const single = one(a, ...mid), together = both(...mid);
            // A crest of a meets a trough of b: the point at distance front from a and
            // front + half from b, where the two circles cross.
            const D = 2 * front, rA = front, rB = front + half;
            const x = (rA * rA - rB * rB + D * D) / (2 * D), y = Math.sqrt(rA * rA - x * x);
            const ra = Math.hypot(x, y), rb = Math.hypot(x - 2 * front, y);
            const cancel = both(x, y), alone = Math.max(Math.abs(one(a, x, y)), Math.abs(one(b, x, y)));
            return { sum, single, together, ra, rb, cancel, alone, front, half };
        })()""")
        assert result["sum"], "the height is exactly the sum of each ripple's wave"
        assert result["together"] > 1.9 * result["single"] > 0, f"crests meeting are brighter: {result}"
        assert abs(result["ra"] - result["front"]) < 1e-6 and abs(result["rb"] - result["front"] - result["half"]) < 1e-6
        assert abs(result["cancel"]) < 0.35 * result["alone"], f"a crest and a trough cancel: {result}"


def test_still_water_draws_nothing():
    # The grid is redrawn only while a ripple moves, so the pond uses no power when it is still.
    probe = """
window.__frames = 0;
const raf = window.requestAnimationFrame.bind(window);
window.requestAnimationFrame = (f) => { window.__frames += 1; return raf(f); };"""
    with open_app(init_script=probe) as (page, _, _):
        go(page, "ripple")
        page.locator(".pond").click(position={"x": 100, "y": 100})
        life = SETTINGS["lifeSeconds"] + SETTINGS["rings"] * SETTINGS["ringGapSeconds"]
        page.wait_for_timeout(int(life * 1000) + 500)
        before = page.evaluate("window.__frames")
        page.wait_for_timeout(1000)
        assert page.evaluate("window.__frames") == before, "no frames are drawn on still water"


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
        # Count every ripple made and the most on the water at once. Ripples also clear themselves
        # after a few seconds, so a count taken at the end would depend on how fast the drag ran.
        page.evaluate("""(() => { const pond = document.querySelector('.pond');
            window.__made = 0; window.__most = pond.querySelectorAll('.ripple-set').length;
            new MutationObserver((records) => {
              for (const r of records) window.__made += [...r.addedNodes].filter(n => n.classList?.contains('ripple-set')).length;
              window.__most = Math.max(window.__most, pond.querySelectorAll('.ripple-set').length);
            }).observe(pond, { childList: true }); })()""")
        page.mouse.move(pond["x"] + 10, pond["y"] + 20)
        page.mouse.down()
        page.mouse.move(pond["x"] + pond["width"] - 10, pond["y"] + pond["height"] - 20, steps=40)
        page.mouse.up()
        made = page.evaluate("window.__made")
        assert made > SETTINGS["maxRipples"], f"the long drag left a trail ({made} ripples)"
        # The cap, checked with quick key presses, so the drag's speed on this machine cannot matter.
        page.locator(".pond").focus()
        for _ in range(SETTINGS["maxRipples"] + 4):
            page.keyboard.press("Enter")
        most = page.evaluate("window.__most")
        assert most == SETTINGS["maxRipples"], f"never more than maxRipples at once ({most})"
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


def test_the_drop_is_muted_by_a_low_pass_filter():
    # Owner, 2026-10-07: "a bit more muted".
    probe = """
window.__filters = [];
const createFilter = AudioContext.prototype.createBiquadFilter;
AudioContext.prototype.createBiquadFilter = function () {
  const node = createFilter.call(this); window.__filters.push(node); return node; };
"""
    with open_app(init_script=probe) as (page, _, _):
        page.locator(".guide").click()
        go(page, "ripple")
        page.locator(".pond").click(position={"x": 100, "y": 100})
        wait_until(page, "window.__filters.length > 0", 2000)
        last = page.evaluate("(() => { const f = window.__filters.at(-1); return [f.type, f.frequency.value]; })()")
        assert last == ["lowpass", CONFIG["sounds"]["drop"]["lowpassHz"]]
        assert CONFIG["sounds"]["drop"]["lowpassHz"] < CONFIG["sounds"]["drop"]["endHz"]


def test_a_slow_drag_is_never_followed_by_a_stray_random_ripple():
    # The click after a long drag once counted as a key press and added a random ripple.
    with open_app() as (page, _, _):
        go(page, "ripple")
        pond = page.locator(".pond").bounding_box()
        y = pond["y"] + pond["height"] / 2
        page.mouse.move(pond["x"] + 20, y)
        page.mouse.down()
        page.wait_for_timeout(900)  # longer than any time window could allow
        page.mouse.move(pond["x"] + 20 + SETTINGS["trailSpacing"] * 1.5, y, steps=4)
        page.mouse.up()
        lefts = page.locator(".ripple-set").evaluate_all("els => els.map(e => parseFloat(e.style.left))")
        assert len(lefts) == 2 and all(left <= 20 + SETTINGS["trailSpacing"] * 1.5 + 1 for left in lefts), lefts
        page.locator(".pond").focus()
        page.keyboard.press("Enter")
        assert page.locator(".ripple-set").count() == 3, "a key press after a drag still makes a ripple"


def test_a_ripple_fades_out_smoothly_at_the_end_of_its_life():
    # RLG-054 (owner, 2026-10-10): ripples vanished abruptly. Near its end a ripple is almost flat.
    with open_app() as (page, _, _):
        go(page, "ripple")
        result = page.evaluate("""(async () => {
            const { waveHeight } = await import('./activities/ripple.js');
            const wave = (await (await fetch('config.json')).json()).ripple.wave;
            const life = 4.75, source = { x: 0, y: 0, born: 0, life };
            // The largest height along the ring at a given age.
            const peak = (age) => Math.max(...[...Array(200).keys()].map((i) =>
                Math.abs(waveHeight([source], wave.speed * age + (i - 100) * 0.5, 0, age, wave))));
            return { before: peak(life - wave.endFadeSeconds), late: peak(life - 0.1), end: peak(life) };
        })()""")
        assert result["end"] == 0, result
        assert result["late"] < 0.05 * result["before"], f"it fades to almost nothing first: {result}"


def test_no_sound_stop_can_jump_its_volume():
    # RLG-053: cancelScheduledValues alone dropped a running ramp, and the volume jumped back up.
    source = (ROOT / "audio.js").read_text("utf-8")
    body = source.split("function hold(param, now) {", 1)
    assert len(body) == 2, "audio.js has a hold() helper"
    outside = body[0] + body[1].split("\n}\n", 1)[1]
    code = " ".join(line for line in outside.splitlines() if not line.strip().startswith("//"))
    assert "cancelScheduledValues" not in code, "every stop goes through hold()"
