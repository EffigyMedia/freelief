"""The Calm screen (owner, 2026-10-07): musical pads, shapes that come and go, and a black screen
that one tap or key brings back."""

import json

from harness import ROOT, open_app, wait_until

CONFIG = json.loads((ROOT / "config.json").read_text("utf-8"))
STRINGS = json.loads((ROOT / "strings" / "en.json").read_text("utf-8"))

OSC_PROBE = """
window.__osc = [];
const create = AudioContext.prototype.createOscillator;
AudioContext.prototype.createOscillator = function () {
  const node = create.call(this);
  const record = { stop: null, ctx: this, node };
  window.__osc.push(record);
  const stop = node.stop.bind(node);
  node.stop = (when) => { record.stop = when ?? this.currentTime; return stop(when); };
  return node;
};
"""


def go(page, route):
    page.evaluate(f"location.hash = '{route}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 3000)


LIVE_PADS = ("window.__osc.filter(o => o.node.type === 'triangle' && "
             "(o.stop === null || o.stop > o.ctx.currentTime + 3)).length")


def test_the_music_keeps_playing_after_leaving_and_the_sound_bar_stops_it():
    # RLG-045 (owner, 2026-10-09): the sound plays on every screen until it is turned off.
    with open_app(init_script=OSC_PROBE) as (page, errors, _):
        page.locator(".guide").click()  # the first gesture unlocks sound
        go(page, "calm")
        voices = len(CONFIG["sounds"]["pads"]["chords"][0]) * 2
        wait_until(page, f"window.__osc.length >= {voices}", 3000)
        assert page.locator(".sound-bar").is_hidden(), "the Visualizer has its own choice, so no bar"
        go(page, "bubbles")
        assert page.evaluate(LIVE_PADS) >= voices, "leaving the Visualizer does not stop the music"
        bar = page.locator(".sound-bar")
        assert bar.is_visible() and bar.locator(".sound-bar-text").inner_text() == STRINGS["soundBar.music"]
        stop = bar.locator(".sound-bar-stop")
        assert stop.inner_text() == STRINGS["soundBar.stop"]
        assert stop.get_attribute("aria-describedby") == "sound-bar-text"
        stop.click()
        assert bar.is_hidden()
        assert page.evaluate("document.activeElement.tagName") == "H1", "focus moves to the heading, not lost"
        wait_until(page, f"{LIVE_PADS} === 0", 3000)
        go(page, "calm")
        assert page.locator("input[name=calm-mode][value=off]").is_checked(), "Stop is the same as Off"
        before = page.evaluate("window.__osc.length")
        page.wait_for_timeout(500)
        assert page.evaluate("window.__osc.length") == before, "Off stays off on coming back"
        assert not errors, errors


def test_the_sound_bar_is_reached_and_used_by_keyboard():
    with open_app(init_script=OSC_PROBE, viewport={"width": 360, "height": 740}) as (page, _, _):
        page.locator(".guide").click()
        go(page, "calm")
        go(page, "menu")
        page.locator(".brand").click()
        for _ in range(6):
            page.keyboard.press("Tab")
            if page.evaluate("document.activeElement.classList.contains('sound-bar-stop')"):
                break
        assert page.evaluate("document.activeElement.classList.contains('sound-bar-stop')")
        box = page.locator(".sound-bar-stop").bounding_box()
        assert box["height"] >= 44 and box["width"] >= 44
        page.keyboard.press("Enter")
        assert page.locator(".sound-bar").is_hidden()


def test_breathing_lowers_the_background_sound_and_leaving_brings_it_back():
    probe = """
window.__gains = [];
const createGain = AudioContext.prototype.createGain;
AudioContext.prototype.createGain = function () { const n = createGain.call(this); window.__gains.push(n); return n; };"""
    duck = CONFIG["sounds"]["background"]
    with open_app(init_script=probe) as (page, _, _):
        page.locator(".guide").click()
        go(page, "calm")
        wait_until(page, "window.__gains.length >= 2", 3000)
        bed = "window.__gains[1].gain.value"  # the master volume first, then the background's own
        # The app opened on breathing, so the background starts low and rises on the Visualizer.
        wait_until(page, f"Math.abs({bed} - 1) < 0.01", int(duck["duckSeconds"] * 1000) + 2000)
        go(page, "breathe")
        wait_until(page, f"Math.abs({bed} - {duck['duckLevel']}) < 0.01", int(duck["duckSeconds"] * 1000) + 2000)
        go(page, "bubbles")
        wait_until(page, f"Math.abs({bed} - 1) < 0.01", int(duck["duckSeconds"] * 1000) + 2000)


def test_calm_is_silent_with_sounds_off_and_says_so():
    with open_app(init_script=OSC_PROBE) as (page, _, _):
        page.locator("button.sound-toggle").click()  # the header's sound button, off
        go(page, "calm")
        page.wait_for_timeout(500)
        assert page.evaluate("window.__osc.length") == 0
        assert page.locator(".calm-sound-note").is_visible()


def test_shapes_come_and_go():
    with open_app() as (page, errors, _):
        go(page, "calm")
        wait_until(page, "document.querySelectorAll('.calm-field > g').length >= 2", 6000)
        count = page.evaluate("document.querySelectorAll('.calm-field > g').length")
        assert count <= CONFIG["calm"]["maxShapes"]
        assert page.evaluate("getComputedStyle(document.querySelector('.calm-shape')).animationName") \
            == "calm-come-and-go"
        assert not errors, errors


def test_shapes_only_fade_under_reduced_motion():
    with open_app(reduced_motion="reduce") as (page, _, _):
        go(page, "calm")
        wait_until(page, "document.querySelectorAll('.calm-shape').length >= 1", 4000)
        style = page.evaluate("""(() => { const s = getComputedStyle(document.querySelector('.calm-shape'));
            return [s.animationName, s.animationDuration]; })()""")
        assert style[0] == "calm-fade" and style[1] != "0s", style


def test_black_screen_covers_everything_and_one_tap_brings_it_back():
    with open_app() as (page, _, _):
        go(page, "calm")
        page.locator(".black-screen").click()
        cover = page.locator(".black-cover")
        assert cover.is_visible()
        assert page.evaluate("getComputedStyle(document.querySelector('.black-cover')).backgroundColor") \
            == "rgb(0, 0, 0)"
        assert page.evaluate("document.elementFromPoint(innerWidth / 2, 20).classList.contains('black-cover')"), \
            "the cover sits over the header too"
        assert cover.get_attribute("aria-label") == STRINGS["calm.blackLabel"]
        page.mouse.click(100, 400)
        assert page.locator(".black-cover").count() == 0
        assert page.evaluate("document.activeElement.classList.contains('black-screen')")


def test_black_screen_works_by_keyboard():
    with open_app() as (page, _, _):
        go(page, "calm")
        page.locator(".black-screen").focus()
        page.keyboard.press("Enter")
        assert page.evaluate("document.activeElement.classList.contains('black-cover')")
        page.keyboard.press("Escape")
        assert page.locator(".black-cover").count() == 0
        page.keyboard.press("Enter")
        page.keyboard.press("Space")
        assert page.locator(".black-cover").count() == 0


def test_leaving_calm_removes_the_black_screen():
    with open_app() as (page, _, _):
        go(page, "calm")
        page.locator(".black-screen").click()
        page.evaluate("location.hash = 'breathe'")
        wait_until(page, "document.querySelector('main').dataset.shown === 'breathe'", 3000)
        assert page.locator(".black-cover").count() == 0


NOISE_PROBE = """
window.__noise = [];
const createSource = AudioContext.prototype.createBufferSource;
AudioContext.prototype.createBufferSource = function () {
  const node = createSource.call(this);
  window.__noise.push(node);
  return node;
};
"""


def test_nature_mode_plays_looping_noise_and_is_remembered():
    with open_app(init_script=OSC_PROBE + NOISE_PROBE) as (page, _, _):
        page.locator(".guide").click()
        go(page, "calm")
        assert page.locator("input[name=calm-mode][value=music]").is_checked()
        wait_until(page, "window.__osc.length > 0", 3000)
        music = page.evaluate("window.__osc.length")
        page.locator("input[name=calm-mode][value=nature]").check()
        wait_until(page, "window.__noise.some(n => n.loop)", 3000)
        assert page.evaluate(f"window.__osc.slice(0, {music}).every(o => o.stop !== null)"), "the music stops for nature"
        go(page, "breathe")
        assert page.locator(".sound-bar-text").inner_text() == \
            STRINGS["soundBar.nature"].format(nature=STRINGS["soundBar.nature.rain"])
        go(page, "calm")
        assert page.locator("input[name=calm-mode][value=nature]").is_checked(), "the choice is remembered"


def test_waves_replace_rain_when_chosen_in_settings_and_the_choice_is_kept():
    # RLG-043: Nature plays rain or waves. Waves have no rain drops (no band-pass filters).
    probe = NOISE_PROBE + """
window.__bands = 0;
const createFilter = AudioContext.prototype.createBiquadFilter;
AudioContext.prototype.createBiquadFilter = function () {
  const n = createFilter.call(this); setTimeout(() => { if (n.type === 'bandpass') window.__bands += 1; }, 0); return n; };"""
    with open_app(init_script=probe) as (page, errors, _):
        page.locator(".guide").click()
        go(page, "settings")
        assert page.locator("input[name=natureSound][value=rain]").is_checked()
        page.locator("input[name=natureSound][value=waves]").check()
        page.reload()
        wait_until(page, "document.documentElement.dataset.ready === 'true'", 5000)
        go(page, "settings")
        assert page.locator("input[name=natureSound][value=waves]").is_checked(), "saved, reloaded, read"
        page.locator(".brand").click()
        go(page, "calm")
        page.locator("input[name=calm-mode][value=nature]").check()
        wait_until(page, "window.__noise.some(n => n.loop)", 3000)
        page.wait_for_timeout(800)
        assert page.evaluate("window.__bands") == 0, "waves, not rain: no drops"
        go(page, "menu")
        assert page.locator(".sound-bar-text").inner_text() == \
            STRINGS["soundBar.nature"].format(nature=STRINGS["soundBar.nature.waves"])
        assert not errors, errors


def test_a_saved_rain_choice_from_before_becomes_nature():
    store = "localStorage.setItem('freelief.settings.v2', JSON.stringify({ calmMode: 'rain' }));"
    with open_app(init_script=f"if (!sessionStorage.seeded) {{ {store} sessionStorage.seeded = 1; }}") as (page, _, _):
        go(page, "calm")
        assert page.locator("input[name=calm-mode][value=nature]").is_checked()


NOISE_STOP_PROBE = """
window.__noise = [];
const createSource = AudioContext.prototype.createBufferSource;
AudioContext.prototype.createBufferSource = function () {
  const node = createSource.call(this);
  const record = { node, stopped: false };
  window.__noise.push(record);
  const stop = node.stop.bind(node);
  node.stop = (when) => { record.stopped = true; return stop(when); };
  return node;
};
"""


def test_both_mode_plays_music_and_rain_together_and_stops_both():
    live_pads = ("window.__osc.filter(o => o.node.type === 'triangle' && "
                 "(o.stop === null || o.stop > o.ctx.currentTime)).length")
    live_rain = "window.__noise.filter(n => n.node.loop && !n.stopped).length"
    with open_app(init_script=OSC_PROBE + NOISE_STOP_PROBE) as (page, errors, _):
        page.locator(".guide").click()
        go(page, "calm")
        page.locator("input[name=calm-mode][value=both]").check()
        # Both plays the pads (triangle waves) and the looping rain together, and leaving keeps them.
        pads = len(CONFIG["sounds"]["pads"]["chords"][0]) * 2
        wait_until(page, f"{live_pads} >= {pads} && {live_rain} >= 1", 3000)
        go(page, "breathe")
        assert page.evaluate(f"{live_pads} >= {pads} && {live_rain} >= 1"), "leaving keeps both"
        go(page, "calm")
        assert page.locator("input[name=calm-mode][value=both]").is_checked(), "the choice is remembered"
        # Off stops everything: the music fades within 2 s, the rain stops at once.
        page.locator("input[name=calm-mode][value=off]").check()
        wait_until(page, f"{live_pads} === 0 && {live_rain} === 0", 4000)
        assert not errors, errors
        mix = CONFIG["calm"]["bothMix"]
        assert 0 < mix["nature"] < mix["music"] <= 1, "the nature sound sits under the music"


def test_the_bubble_pop_is_percussive_noise_not_a_tone():
    with open_app(init_script=OSC_PROBE + NOISE_PROBE) as (page, _, _):
        page.locator(".guide").click()
        go(page, "bubbles")
        before = page.evaluate("window.__noise.length")
        page.locator("button.bubble").first.click(force=True)
        wait_until(page, f"window.__noise.length > {before}", 2000)
        last = page.evaluate("window.__osc[window.__osc.length - 1].stop - window.__osc[window.__osc.length - 1].ctx.currentTime")
        assert last < 0.15, "the thump under the pop is short"


def test_full_screen_fills_the_screen_and_leaves_by_button_or_escape():
    with open_app(viewport={"width": 390, "height": 844}) as (page, _, _):
        go(page, "calm")
        page.locator(".full-screen").click()
        box = page.locator(".calm-stage").bounding_box()
        assert box["width"] >= 389 and box["height"] >= 843, box
        assert page.evaluate("document.activeElement.classList.contains('calm-exit')")
        page.keyboard.press("Escape")
        assert not page.evaluate("document.querySelector('.calm-stage').classList.contains('full')")
        page.locator(".full-screen").click()
        page.locator(".calm-exit").click()
        assert page.locator(".calm-exit").is_hidden()


def test_back_to_menu_is_at_the_top_of_every_screen_and_the_footer_does_not_mention_breathing():
    with open_app(route="settings") as (page, _, _):
        above = page.evaluate("""(() => { const nav = document.querySelector('.screen-nav');
            return nav.compareDocumentPosition(document.querySelector('main')) & Node.DOCUMENT_POSITION_FOLLOWING; })()""")
        assert above, "Back to menu comes before the Settings screen"
        assert "circle" not in page.locator(".tagline").inner_text().lower()
        for route in ["trace", "unblock", "about", "feedback"]:
            go(page, route)
            nav = page.locator(".screen-nav").bounding_box()
            screen = page.locator("main").bounding_box()
            header = page.locator("header.top").bounding_box()
            assert header["y"] + header["height"] <= nav["y"] < screen["y"], f"Back to menu is at the top of {route}"
        go(page, "menu")
        assert page.locator(".screen-nav").is_hidden()

def test_lines_divide_the_header_and_the_footer_and_the_about_version_is_centred():
    with open_app(route="about") as (page, _, _):
        top = page.locator("header.top").evaluate("e => getComputedStyle(e).borderBottomWidth")
        bottom = page.locator("footer.bottom").evaluate("e => getComputedStyle(e).borderTopWidth")
        assert top == "2px" and bottom == "2px"
        version = page.locator(".about-version")
        assert version.evaluate("e => getComputedStyle(e).textAlign") == "center"
        box, section = version.bounding_box(), page.locator("section.page").bounding_box()
        assert abs((box["x"] + box["width"] / 2) - (section["x"] + section["width"] / 2)) < 2


def test_activities_show_no_text_above_them_but_a_screen_reader_still_hears_how_to_use_them():
    with open_app() as (page, _, _):
        for route in ["bubbles", "trace", "unblock", "calm"]:
            go(page, route)
            hidden = page.locator(f"main p.visually-hidden:text-is({json.dumps(STRINGS[route + '.intro'])})")
            assert hidden.count() == 1, route
            box = hidden.bounding_box()
            assert box["width"] <= 1 and box["height"] <= 1, f"{route}: the intro is not shown"
            assert page.locator("main .exercise-intro").count() == 0, route
        go(page, "unblock")
        assert page.locator(".unblock-board").get_attribute("aria-describedby") == "unblock-intro"


def test_the_header_stays_at_the_top_while_the_page_scrolls():
    # Owner, 2026-10-08: the header is frozen; the rest scrolls under it.
    with open_app(viewport={"width": 390, "height": 700}) as (page, _, _):
        go(page, "about")
        page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
        page.wait_for_timeout(200)
        assert page.evaluate("scrollY") > 300, "the About page is long enough to scroll"
        header = page.locator("header.top").bounding_box()
        assert abs(header["y"]) < 1, header
        assert page.locator(".help-open").is_visible()
        page.locator(".help-open").click()
        assert page.locator("dialog.help").evaluate("d => d.open"), "help is one tap away mid-page"


def test_a_visualizer_opened_before_any_tap_starts_its_sound_at_the_first_tap():
    # A browser allows sound only after a gesture. The bar must never name a sound that is silent.
    with open_app(init_script=OSC_PROBE, route="calm") as (page, _, _):
        page.wait_for_timeout(500)
        assert page.evaluate("window.__osc.length") == 0, "nothing plays before a gesture"
        page.locator("h1").click()
        wait_until(page, "window.__osc.length > 0", 3000)


def test_any_key_ends_the_black_screen_and_the_page_under_a_cover_cannot_be_reached():
    # web-interface-review, 2026-10-09: the label says any key; Tab must not reach hidden controls.
    with open_app() as (page, _, _):
        go(page, "calm")
        page.locator(".black-screen").click()
        assert page.evaluate("document.querySelector('main').inert"), "the page under the cover is inert"
        page.keyboard.press("a")
        assert page.locator(".black-cover").count() == 0, "any key brings the screen back"
        assert not page.evaluate("document.querySelector('main').inert")
        page.locator(".full-screen").click()
        assert page.evaluate("document.querySelector('header').inert"), "full screen makes the rest inert"
        page.keyboard.press("Escape")
        assert not page.evaluate("document.querySelector('header').inert")
