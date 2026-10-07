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
