"""Slice 5 in a real browser: the colour sort (REQ-014), by keyboard, by touch, without sight."""

import json

from harness import ROOT, open_app, wait_until

STRINGS = json.loads((ROOT / "strings" / "en.json").read_text("utf-8"))
CONFIG = json.loads((ROOT / "config.json").read_text("utf-8"))
COUNT = len(CONFIG["sort"]["lightness"])


def go(page, route):
    page.evaluate(f"location.hash = '{route}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 2000)


def order(page):
    return page.locator(".sort-tile").evaluate_all("els => els.map(e => Number(e.dataset.shade))")


def test_tiles_start_out_of_order_with_spoken_names():
    with open_app() as (page, _, _):
        go(page, "sort")
        shades = order(page)
        assert sorted(shades) == list(range(COUNT)) and shades != list(range(COUNT))
        label = page.locator(".sort-tile").first.get_attribute("aria-label")
        assert label.startswith("Blue, ") and label.endswith(f"place 1 of {COUNT}")
        tab_stops = page.locator(".sort-tile[tabindex='0']").count()
        assert tab_stops == 1, "the row is one tab stop; arrows move inside it"


def test_the_sort_can_be_solved_by_keyboard_alone():
    with open_app() as (page, errors, _):
        go(page, "sort")
        page.locator(".sort-tile[tabindex='0']").focus()
        position = 0
        # A selection sort, done the way a keyboard user would: arrows to move, Enter to choose.
        for target in range(COUNT):
            shades = order(page)
            if shades[target] == target:
                continue
            source = shades.index(target)
            for _ in range(abs(source - position)):
                page.keyboard.press("ArrowRight" if source > position else "ArrowLeft")
            position = source
            page.keyboard.press("Enter")
            assert page.locator(".sort-tile[aria-pressed='true']").count() == 1
            for _ in range(abs(target - position)):
                page.keyboard.press("ArrowRight" if target > position else "ArrowLeft")
            position = target
            page.keyboard.press("Enter")
        assert order(page) == list(range(COUNT))
        assert page.locator(".sort-status").inner_text() == STRINGS["sort.done"]
        assert page.locator(".sort-status").get_attribute("aria-live") == "polite"
        assert not errors, errors


def test_two_taps_swap_and_a_second_tap_on_the_same_tile_cancels():
    with open_app() as (page, _, _):
        go(page, "sort")
        before = order(page)
        tiles = page.locator(".sort-tile")
        tiles.nth(0).click()
        tiles.nth(0).click()
        assert page.locator(".sort-status").inner_text() == STRINGS["sort.unchosen"]
        assert order(page) == before
        tiles.nth(0).click()
        tiles.nth(1).click()
        assert order(page) == [before[1], before[0], *before[2:]]
        assert page.locator(".sort-tile[aria-pressed='true']").count() == 0


def test_new_colours_changes_the_palette_and_reshuffles():
    with open_app() as (page, _, _):
        go(page, "sort")
        page.locator(".new-colours").click()
        label = page.locator(".sort-tile").first.get_attribute("aria-label")
        assert label.startswith("Green, ")
        assert order(page) != list(range(COUNT))


def test_tiles_are_large_targets():
    with open_app() as (page, _, _):
        go(page, "sort")
        sizes = page.locator(".sort-tile").evaluate_all(
            "els => els.map(e => Math.min(e.getBoundingClientRect().width, e.getBoundingClientRect().height))")
        assert min(sizes) >= 44


def centre(page, index):
    box = page.locator(".sort-tile").nth(index).bounding_box()
    return box["x"] + box["width"] / 2, box["y"] + box["height"] / 2


def mouse_drag(page, start, end, steps=8):
    page.mouse.move(*centre(page, start))
    page.mouse.down()
    page.mouse.move(*centre(page, end), steps=steps)
    page.mouse.up()


def test_a_drag_onto_another_tile_swaps_the_two():
    with open_app() as (page, errors, _):
        go(page, "sort")
        before = order(page)
        mouse_drag(page, 0, 3)
        assert order(page) == [before[3], before[1], before[2], before[0], *before[4:]]
        name = page.locator(".sort-tile").nth(3).get_attribute("aria-label").split(", place")[0]
        assert page.locator(".sort-status").inner_text() == STRINGS["sort.swapped"].format(
            name=name, position=4)
        assert page.locator(".sort-tile[aria-pressed='true']").count() == 0, "a drag chooses nothing"
        assert page.locator(".sort-tile.dragging, .sort-tile.drop-target").count() == 0
        assert not errors, errors


def test_the_sort_can_be_solved_by_drag_alone():
    with open_app() as (page, errors, _):
        go(page, "sort")
        for target in range(COUNT):
            shades = order(page)
            if shades[target] != target:
                mouse_drag(page, shades.index(target), target)
        assert order(page) == list(range(COUNT))
        assert page.locator(".sort-status").inner_text() == STRINGS["sort.done"]
        assert not errors, errors


def test_a_drag_dropped_off_the_tiles_changes_nothing():
    with open_app() as (page, _, _):
        go(page, "sort")
        before = order(page)
        x, y = centre(page, 1)
        page.mouse.move(x, y)
        page.mouse.down()
        page.mouse.move(x, y + 200, steps=8)
        page.mouse.up()
        assert order(page) == before
        assert page.locator(".sort-tile[aria-pressed='true']").count() == 0
        assert page.locator(".sort-tile.dragging, .sort-tile.drop-target").count() == 0


def test_a_small_slip_is_still_a_tap_and_chooses():
    threshold = CONFIG["sort"]["dragThreshold"]
    with open_app() as (page, _, _):
        go(page, "sort")
        before = order(page)
        x, y = centre(page, 2)
        page.mouse.move(x, y)
        page.mouse.down()
        page.mouse.move(x + threshold / 2, y, steps=2)
        page.mouse.up()
        assert page.locator(".sort-tile[aria-pressed='true']").count() == 1
        assert order(page) == before
        # The tap after a drag is a choice too: the drag does not swallow the next click.
        mouse_drag(page, 0, 1)
        page.locator(".sort-tile").nth(4).click()
        assert page.locator(".sort-tile[aria-pressed='true']").count() == 1


def test_a_touch_drag_swaps_without_scrolling_the_page():
    with open_app() as (page, errors, _):
        go(page, "sort")
        before = order(page)
        cdp = page.context.new_cdp_session(page)
        (x0, y0), (x1, y1) = centre(page, 4), centre(page, 1)
        scroll = page.evaluate("scrollY")
        cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x0, "y": y0}]})
        for i in range(1, 9):
            cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [
                {"x": x0 + (x1 - x0) * i / 8, "y": y0 + (y1 - y0) * i / 8}]})
        cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
        wait_until(page, "!document.querySelector('.sort-tile.dragging')", 2000)
        expected = list(before)
        expected[1], expected[4] = before[4], before[1]
        assert order(page) == expected
        assert page.evaluate("scrollY") == scroll
        assert page.locator(".sort-tile").first.evaluate("e => getComputedStyle(e).touchAction") == "none"
        assert not errors, errors


def test_in_forced_colors_the_shades_keep_their_colors():
    # AUD-050: in Windows High Contrast the shades are the task, so they must not be replaced.
    with open_app() as (page, _, _):
        page.emulate_media(forced_colors="active")
        go(page, "sort")
        tiles = page.locator(".sort-tile")
        colors = tiles.evaluate_all("els => els.map(e => getComputedStyle(e).backgroundColor)")
        assert len(set(colors)) == COUNT, f"each shade keeps its own color: {colors}"
        assert tiles.first.evaluate("e => getComputedStyle(e).forcedColorAdjust") == "none"
