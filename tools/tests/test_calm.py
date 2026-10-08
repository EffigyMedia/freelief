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
  const record = { stop: null, ctx: this };
  window.__osc.push(record);
  const stop = node.stop.bind(node);
  node.stop = (when) => { record.stop = when ?? this.currentTime; return stop(when); };
  return node;
};
"""


def go(page, route):
    page.evaluate(f"location.hash = '{route}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 3000)


def test_calm_plays_pads_and_stops_them_on_leaving():
    with open_app(init_script=OSC_PROBE) as (page, _, _):
        page.locator(".guide").click()  # the first gesture unlocks sound
        go(page, "calm")
        voices = len(CONFIG["sounds"]["pads"]["chords"][0]) * 2
        wait_until(page, f"window.__osc.length >= {voices}", 3000)
        go(page, "breathe")
        later = page.evaluate("window.__osc.every(o => o.stop !== null && o.stop - o.ctx.currentTime < 3)")
        assert later, "leaving Calm stops the music"


def test_calm_is_silent_with_sounds_off_and_says_so():
    with open_app(init_script=OSC_PROBE) as (page, _, _):
        go(page, "settings")
        page.locator("input[name=sounds]").uncheck()
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


def test_rain_mode_plays_looping_noise_and_is_remembered():
    with open_app(init_script=OSC_PROBE + NOISE_PROBE) as (page, _, _):
        page.locator(".guide").click()
        go(page, "calm")
        assert page.locator("input[name=calm-mode][value=music]").is_checked()
        wait_until(page, "window.__osc.length > 0", 3000)
        music = page.evaluate("window.__osc.length")
        page.locator("input[name=calm-mode][value=rain]").check()
        wait_until(page, "window.__noise.some(n => n.loop)", 3000)
        assert page.evaluate(f"window.__osc.slice(0, {music}).every(o => o.stop !== null)"), "the music stops for the rain"
        go(page, "breathe")
        go(page, "calm")
        assert page.locator("input[name=calm-mode][value=rain]").is_checked(), "the choice is remembered"


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
        for route in ["trace", "sort", "about", "feedback"]:
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
        for route in ["bubbles", "trace", "sort", "calm"]:
            go(page, route)
            hidden = page.locator(f"main p.visually-hidden:text-is({json.dumps(STRINGS[route + '.intro'])})")
            assert hidden.count() == 1, route
            box = hidden.bounding_box()
            assert box["width"] <= 1 and box["height"] <= 1, f"{route}: the intro is not shown"
            assert page.locator("main .exercise-intro").count() == 0, route
        go(page, "sort")
        assert page.locator(".sort-tiles").get_attribute("aria-describedby") == "sort-intro"
