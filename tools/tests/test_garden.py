"""Zen Garden (RLG-055, owner 2026-10-10): rake the sand by touch and by keyboard; add, move and
remove stones and plants by touch, keyboard and screen reader; nothing scored, nothing timed."""

import json

from harness import ROOT, open_app, wait_until

CONFIG = json.loads((ROOT / "config.json").read_text("utf-8"))
STRINGS = json.loads((ROOT / "strings" / "en.json").read_text("utf-8"))
SETTINGS = CONFIG["garden"]


def go(page, route):
    page.evaluate(f"location.hash = '{route}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 3000)


def lines(page):
    return page.locator(".garden-lines line").count()


def test_a_finger_drawn_across_the_sand_rakes_parallel_lines():
    with open_app(viewport={"width": 360, "height": 800}) as (page, errors, _):
        go(page, "garden")
        assert page.locator(".garden-item.stone").count() == SETTINGS["startStones"]
        assert lines(page) == 0
        sand = page.locator(".garden-sand")
        sand.scroll_into_view_if_needed()
        box = sand.bounding_box()
        page.mouse.move(box["x"] + 10, box["y"] + 15)
        page.mouse.down()
        page.mouse.move(box["x"] + box["width"] - 10, box["y"] + 15, steps=12)
        page.mouse.up()
        made = lines(page)
        assert made > 0 and made % SETTINGS["tines"] == 0, f"each step rakes one line per tine: {made}"
        assert sand.evaluate("e => getComputedStyle(e).touchAction") == "none"
        page.locator(".garden-smooth").click()
        assert lines(page) == 0
        assert page.locator(".garden-status").inner_text() == STRINGS["garden.smoothed"]
        assert page.locator(".garden-item.stone").count() == SETTINGS["startStones"], "smoothing keeps the stones"
        assert not errors, errors


def test_the_sand_is_raked_by_keyboard_alone():
    with open_app() as (page, _, _):
        go(page, "garden")
        area = page.locator(".garden-rake-area")
        assert area.get_attribute("aria-label") == STRINGS["garden.sandLabel"]
        area.focus()
        assert page.locator(".garden-rake").get_attribute("visibility") == "visible"
        for key in ("ArrowRight", "ArrowRight", "ArrowDown", "ArrowLeft"):
            page.keyboard.press(key)
        assert lines(page) == 4 * SETTINGS["tines"]


def test_stones_and_plants_are_added_moved_and_removed_by_keyboard():
    with open_app() as (page, errors, _):
        go(page, "garden")
        page.locator(".garden-add-plant").click()
        plant = page.locator(".garden-item.plant")
        assert plant.count() == 1
        assert page.evaluate("document.activeElement.classList.contains('plant')"), "focus goes to the new plant"
        label = plant.get_attribute("aria-label")
        assert label.startswith(STRINGS["garden.plant"].format(number=1))
        assert plant.get_attribute("aria-pressed") == "true"
        page.keyboard.press("ArrowRight")
        assert plant.get_attribute("aria-label") != label, "the arrow keys move it"
        assert page.locator(".garden-status").get_attribute("aria-live") == "polite"
        page.keyboard.press("Delete")
        assert plant.count() == 0
        assert page.locator(".garden-status").inner_text() == STRINGS["garden.removed"]
        page.locator(".garden-item.stone").first.click()
        page.locator(".garden-remove").click()
        assert page.locator(".garden-item.stone").count() == SETTINGS["startStones"] - 1
        assert page.locator(".garden-remove").is_disabled(), "nothing is chosen after a removal"
        assert not errors, errors


def test_a_stone_is_dragged_and_the_garden_has_room_for_only_a_few():
    with open_app(viewport={"width": 360, "height": 800}) as (page, _, _):
        go(page, "garden")
        stone = page.locator(".garden-item.stone").first
        stone.scroll_into_view_if_needed()
        box = stone.bounding_box()
        assert min(box["width"], box["height"]) >= 44, f"a stone is a large target: {box}"
        label = stone.get_attribute("aria-label")
        x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
        page.mouse.move(x, y)
        page.mouse.down()
        page.mouse.move(x + 40, y + 20, steps=8)
        page.mouse.up()
        assert stone.get_attribute("aria-label") != label, "the drag moved it"
        assert stone.get_attribute("aria-pressed") == "false", "a drag does not choose"
        for _ in range(SETTINGS["maxItems"]):
            page.locator(".garden-add-stone").click()
        assert page.locator(".garden-item").count() == SETTINGS["maxItems"]
        assert page.locator(".garden-status").inner_text() == STRINGS["garden.full"]


def test_raking_makes_a_soft_sand_sound_and_nothing_is_counted():
    probe = """
window.__src = 0;
const create = AudioContext.prototype.createBufferSource;
AudioContext.prototype.createBufferSource = function () { window.__src += 1; return create.call(this); };"""
    with open_app(init_script=probe) as (page, _, _):
        page.locator(".guide").click()  # the first gesture unlocks sound
        page.wait_for_timeout(300)
        go(page, "garden")
        before = page.evaluate("window.__src")
        page.locator(".garden-rake-area").focus()
        page.keyboard.press("ArrowRight")
        wait_until(page, f"window.__src > {before}", 2000)
        text = page.locator("main").inner_text().lower()
        for word in ("score", "time", "level", "lose"):
            assert word not in text, word


def test_enter_and_space_choose_an_item_and_remove_takes_it_away():
    # AUD-152: an item is a toggle button, so Enter and Space choose it, as a click does; the Remove
    # button then takes it away, all by keyboard.
    with open_app() as (page, errors, _):
        go(page, "garden")
        stone = page.locator(".garden-item.stone").first
        stone.focus()
        page.keyboard.press("Enter")
        assert stone.get_attribute("aria-pressed") == "true"
        page.keyboard.press(" ")
        assert stone.get_attribute("aria-pressed") == "false", "Space chooses it no more"
        page.keyboard.press(" ")
        assert stone.get_attribute("aria-pressed") == "true"
        before = page.locator(".garden-item").count()
        page.locator(".garden-remove, button.remove").first.focus()
        page.keyboard.press("Enter")
        assert page.locator(".garden-item").count() == before - 1
        assert not errors, errors


def test_an_item_added_after_a_removal_gets_a_name_of_its_own():
    # AUD-155: remove Stone 1, add a stone, and no two items share a name.
    with open_app() as (page, errors, _):
        go(page, "garden")
        first = page.locator(".garden-item.stone").first
        first.focus()
        page.keyboard.press("Delete")
        page.locator(".garden-add-stone, button.add-stone").first.click()
        labels = page.locator(".garden-item").evaluate_all("items => items.map(i => i.getAttribute('aria-label'))")
        names = [label.split(",")[0] for label in labels]
        assert len(names) == len(set(names)), names
        assert not errors, errors


def test_raking_plays_one_continuous_sound_that_follows_the_speed():
    # RLG-060 (owner, 2026-10-10): one looping sound for the whole rake, not a repeated one-shot; its
    # level rises with a fast stroke and falls to silence when the rake stops.
    probe = """
window.__loops = []; window.__gains = [];
const createSource = AudioContext.prototype.createBufferSource;
AudioContext.prototype.createBufferSource = function () {
  const node = createSource.call(this); const record = { node, ctx: this };
  Object.defineProperty(record, 'loop', { get: () => node.loop }); window.__loops.push(record); return node; };
const setTarget = AudioParam.prototype.setTargetAtTime;
AudioParam.prototype.setTargetAtTime = function (value, when, constant) { window.__gains.push(value); return setTarget.call(this, value, when, constant); };"""
    with open_app(init_script=probe) as (page, _, _):
        page.locator(".guide").click()  # the first gesture unlocks sound
        wait_until(page, "window.__loops.length > 0", 8000)  # the breath shows that sound is unlocked
        go(page, "garden")
        before = page.evaluate("window.__loops.length")
        sand = page.locator(".garden-sand")
        sand.scroll_into_view_if_needed()
        box = sand.bounding_box()
        page.mouse.move(box["x"] + 20, box["y"] + box["height"] / 2)
        page.mouse.down()
        for i in range(1, 25):
            page.mouse.move(box["x"] + 20 + i * 10, box["y"] + box["height"] / 2)
        # Under full-suite load the first stroke can be slow to reach the audio (a flaky 2 s wait).
        wait_until(page, f"window.__loops.slice({before}).some(r => r.loop)", 8000)
        made = page.evaluate(f"window.__loops.slice({before}).filter(r => r.loop).length")
        assert made == 1, f"one looping sound for the stroke, not {made}"
        assert max(page.evaluate("window.__gains")) > 0, "the stroke is heard"
        page.mouse.up()
        page.wait_for_timeout(CONFIG["garden"]["rakeStillMs"] + 200)
        assert page.evaluate("window.__gains.at(-1)") == 0, "the sound settles to silence when the rake stops"
        assert page.evaluate(f"window.__loops.slice({before}).length") == 1, "no one-shot per move"



def test_no_rings_are_drawn_around_stones_and_plants():
    # RLG-061 (owner, 2026-10-10): stones and plants do not get rings around them by themselves.
    with open_app() as (page, _, _):
        go(page, "garden")
        page.locator(".garden-add-plant").click()
        assert page.locator(".garden-rings, .garden-rings circle").count() == 0
        sizes = page.evaluate("[...document.querySelectorAll('.garden-holes circle')].map(c => Number(c.getAttribute('r')))")
        biggest = max(CONFIG["garden"]["stoneSize"], CONFIG["garden"]["plantSize"])
        assert sizes and max(sizes) <= biggest, f"the lines are hidden only under an item: {sizes}"
