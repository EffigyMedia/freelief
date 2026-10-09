"""Unblock (RLG-040): every board solvable, from easy to hard; by keyboard, by the Slide buttons a
screen reader reaches, by drag; Undo and Start again; no score, timer or losing state."""

import json
from collections import deque

from harness import ROOT, open_app, wait_until

CONFIG = json.loads((ROOT / "config.json").read_text("utf-8"))
STRINGS = json.loads((ROOT / "strings" / "en.json").read_text("utf-8"))
SETTINGS = CONFIG["unblock"]
SIZE = SETTINGS["size"]
LEVELS = ["easy", "medium", "hard"]


def blocks_of(rows):
    cells = {}
    for r, line in enumerate(rows):
        for c, ch in enumerate(line):
            if ch != ".":
                cells.setdefault(ch, []).append((r, c))
    blocks = {}
    for name, found in cells.items():
        across = len({r for r, _ in found}) == 1
        r0, c0 = min(r for r, _ in found), min(c for _, c in found)
        straight = [(r0, c0 + k) if across else (r0 + k, c0) for k in range(len(found))]
        assert sorted(found) == straight, f"block {name} is not one straight line: {rows}"
        blocks[name] = (across, len(found), r0, c0)
    return blocks


def solve(rows):
    """Breadth-first search: the fewest moves, as [(block, steps)], or None. A move slides one block
    any distance along its length. Solved when the key block A reaches the right edge."""
    blocks = blocks_of(rows)
    names = sorted(blocks)
    fixed = [(blocks[n][0], blocks[n][1], blocks[n][2] if blocks[n][0] else blocks[n][3]) for n in names]
    start = tuple(blocks[n][3] if blocks[n][0] else blocks[n][2] for n in names)
    key = names.index("A")
    came = {start: None}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        if state[key] == SIZE - 2:
            path = []
            while came[state]:
                state, move = came[state]
                path.append(move)
            return path[::-1]
        filled = set()
        for (across, length, line), pos in zip(fixed, state):
            filled |= {(line, pos + k) if across else (pos + k, line) for k in range(length)}
        for i, ((across, length, line), pos) in enumerate(zip(fixed, state)):
            for step in (-1, 1):
                p = pos
                while True:
                    edge = p + step if step < 0 else p + step + length - 1
                    if not 0 <= edge < SIZE or ((line, edge) if across else (edge, line)) in filled:
                        break
                    p += step
                    new = state[:i] + (p,) + state[i + 1:]
                    if new not in came:
                        came[new] = (state, (names[i], p - pos))
                        queue.append(new)
    return None


def go(page, route):
    page.evaluate(f"location.hash = '{route}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 3000)


def block(page, name):
    return page.locator(f".unblock-block[data-block='{name}']")


def status(page):
    return page.locator(".unblock-status").inner_text()


def test_every_board_is_solvable_and_the_boards_go_from_easy_to_hard():
    boards = SETTINGS["boards"]
    assert len(boards) >= 12
    levels = [b["level"] for b in boards]
    assert levels == sorted(levels, key=LEVELS.index), "easy boards first, hard boards last"
    assert set(levels) == set(LEVELS)
    fewest = []
    for i, board in enumerate(boards):
        rows = board["rows"]
        assert len(rows) == SIZE and all(len(r) == SIZE for r in rows), f"board {i + 1} is 6 by 6"
        key = blocks_of(rows)["A"]
        assert key[0] and key[1] == 2 and key[2] == SETTINGS["exitRow"], f"board {i + 1}: the blue block"
        assert all(rows[SETTINGS["exitRow"]][c] in ".A" or not blocks_of(rows)[rows[SETTINGS["exitRow"]][c]][0]
                   for c in range(SIZE)), f"board {i + 1}: nothing else lies across the exit row"
        path = solve(rows)
        assert path, f"board {i + 1} has no solution"
        fewest.append(len(path))
    for level in LEVELS:
        moves = [m for m, b in zip(fewest, boards) if b["level"] == level]
        assert moves == sorted(moves), f"{level} boards grow harder in turn: {moves}"
    assert max(f for f, b in zip(fewest, boards) if b["level"] == "easy") < \
        min(f for f, b in zip(fewest, boards) if b["level"] == "hard")


def test_every_block_has_a_name_and_the_board_says_how_to_play():
    with open_app() as (page, errors, _):
        go(page, "unblock")
        board = page.locator(".unblock-board")
        assert board.get_attribute("aria-describedby") == "unblock-intro"
        assert page.locator("#unblock-intro").inner_text() == STRINGS["unblock.intro"]
        labels = page.locator(".unblock-block").evaluate_all("els => els.map(e => e.getAttribute('aria-label'))")
        assert len(set(labels)) == len(labels), "no two blocks share a name"
        key = block(page, "A").get_attribute("aria-label")
        rows = SETTINGS["boards"][0]["rows"]
        col = rows[SETTINGS["exitRow"]].index("A")
        assert key == STRINGS["unblock.across"].format(name=STRINGS["unblock.keyName"], row=SETTINGS["exitRow"] + 1,
                                                       **{"from": col + 1, "to": col + 2})
        assert page.locator(".unblock-board-name").inner_text() == STRINGS["unblock.boardName"].format(
            number=1, total=len(SETTINGS["boards"]), level=STRINGS["unblock.level.easy"])
        assert page.locator(".unblock-status").get_attribute("aria-live") == "polite"
        assert page.locator(".unblock-exit").get_attribute("aria-hidden") == "true"
        assert not errors, errors


def test_a_board_can_be_solved_by_keyboard_alone():
    path = solve(SETTINGS["boards"][0]["rows"])
    with open_app() as (page, errors, _):
        go(page, "unblock")
        page.locator(".nav-back").focus()
        page.keyboard.press("Tab")  # into the board: each block is a stop
        assert page.evaluate("document.activeElement.classList.contains('unblock-block')")
        for name, steps in path:
            block(page, name).focus()
            across = block(page, name).evaluate("e => e.classList.contains('across')")
            key = ("ArrowRight" if steps > 0 else "ArrowLeft") if across else ("ArrowDown" if steps > 0 else "ArrowUp")
            for _ in range(abs(steps)):
                page.keyboard.press(key)
        assert status(page) == STRINGS["unblock.free"]
        assert "free" in block(page, "A").get_attribute("class")
        assert page.evaluate("document.activeElement.classList.contains('unblock-next')"), "focus goes to Next board"
        assert not errors, errors


def test_the_slide_buttons_move_a_chosen_block_for_a_screen_reader():
    rows = SETTINGS["boards"][0]["rows"]
    path = solve(rows)
    with open_app() as (page, _, _):
        go(page, "unblock")
        assert page.locator(".unblock-slide").is_hidden()
        for name, steps in path:
            block(page, name).focus()
            page.keyboard.press("Enter")
            assert block(page, name).get_attribute("aria-pressed") == "true"
            across = block(page, name).evaluate("e => e.classList.contains('across')")
            back, on = page.locator(".unblock-slide button").all()
            assert (back.inner_text(), on.inner_text()) == (
                (STRINGS["unblock.slideLeft"], STRINGS["unblock.slideRight"]) if across
                else (STRINGS["unblock.slideUp"], STRINGS["unblock.slideDown"]))
            for _ in range(abs(steps)):
                (on if steps > 0 else back).click()
            if status(page) != STRINGS["unblock.free"]:
                block(page, name).click()  # choosing it again lets it go
                assert block(page, name).get_attribute("aria-pressed") == "false"
        assert status(page) == STRINGS["unblock.free"]
        assert page.locator(".unblock-slide").is_hidden()


def test_a_blocked_slide_says_so_and_an_arrow_across_a_block_says_which_way_it_goes():
    with open_app() as (page, _, _):
        go(page, "unblock")
        blocks = page.locator(".unblock-block").all()
        said = set()
        for element in blocks:
            element.focus()
            across = "across" in element.get_attribute("class")
            page.keyboard.press("ArrowUp" if across else "ArrowLeft")
            assert status(page) == STRINGS["unblock.onlyAcross" if across else "unblock.onlyDown"]
            before = element.get_attribute("aria-label")
            for _ in range(SIZE):
                page.keyboard.press("ArrowLeft" if across else "ArrowUp")
            said.add(status(page))
            page.evaluate("void 0")
            assert element.get_attribute("aria-label") is not None and before is not None
        assert STRINGS["unblock.noRoom"] in said, "a slide into the edge or a block says there is no room"


def test_a_board_can_be_solved_by_drag_and_one_drag_is_one_move():
    rows = SETTINGS["boards"][0]["rows"]
    path = solve(rows)
    with open_app(viewport={"width": 360, "height": 740}) as (page, _, _):
        go(page, "unblock")
        cell = page.locator(".unblock-board").evaluate("e => e.clientWidth") / SIZE
        first = True
        for name, steps in path:
            box = block(page, name).bounding_box()
            x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
            across = "across" in block(page, name).get_attribute("class")
            label = block(page, name).get_attribute("aria-label")
            page.mouse.move(x, y)
            page.mouse.down()
            dx, dy = (steps * cell, 0) if across else (0, steps * cell)
            page.mouse.move(x + dx, y + dy, steps=10)
            page.mouse.up()
            assert block(page, name).get_attribute("aria-pressed") == "false", "a drag chooses nothing"
            if first and status(page) != STRINGS["unblock.free"]:
                # Undo takes back the whole drag at once, then the drag is done again.
                page.locator(".unblock-undo").click()
                assert block(page, name).get_attribute("aria-label") == label
                page.mouse.move(x, y)
                page.mouse.down()
                page.mouse.move(x + dx, y + dy, steps=10)
                page.mouse.up()
                first = False
        assert status(page) == STRINGS["unblock.free"]
        assert page.locator(".unblock-board").evaluate("e => getComputedStyle(e).touchAction") == "none"


def test_a_short_tap_chooses_and_a_drag_past_the_edge_stops_at_the_edge():
    with open_app(viewport={"width": 360, "height": 740}) as (page, _, _):
        go(page, "unblock")
        element = page.locator(".unblock-block").first
        box = element.bounding_box()
        x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
        page.mouse.move(x, y)
        page.mouse.down()
        page.mouse.move(x + SETTINGS["dragThreshold"] - 3, y)
        page.mouse.up()
        assert element.get_attribute("aria-pressed") == "true", "a small slip is still a tap"
        across = "across" in element.get_attribute("class")
        page.mouse.move(x, y)
        page.mouse.down()
        page.mouse.move(x + (2000 if across else 0), y + (0 if across else 2000), steps=20)
        page.mouse.up()
        inside = page.locator(".unblock-board").bounding_box()
        moved = element.bounding_box()
        assert moved["x"] + moved["width"] <= inside["x"] + inside["width"] + 1
        assert moved["y"] + moved["height"] <= inside["y"] + inside["height"] + 1


def test_undo_and_start_again_take_back_any_move_even_the_last_one():
    rows = SETTINGS["boards"][0]["rows"]
    path = solve(rows)
    with open_app() as (page, _, _):
        go(page, "unblock")
        start = page.locator(".unblock-block").evaluate_all("els => els.map(e => e.getAttribute('aria-label'))")
        page.locator(".unblock-undo").click()
        assert status(page) == STRINGS["unblock.nothingToUndo"]
        for name, steps in path:
            block(page, name).focus()
            across = "across" in block(page, name).get_attribute("class")
            key = ("ArrowRight" if steps > 0 else "ArrowLeft") if across else ("ArrowDown" if steps > 0 else "ArrowUp")
            for _ in range(abs(steps)):
                page.keyboard.press(key)
        assert status(page) == STRINGS["unblock.free"]
        page.locator(".unblock-undo").click()
        assert "free" not in block(page, "A").get_attribute("class"), "the blue block comes back"
        page.locator(".unblock-restart").click()
        assert status(page) == STRINGS["unblock.restarted"]
        assert page.locator(".unblock-block").evaluate_all("els => els.map(e => e.getAttribute('aria-label'))") == start


def test_next_board_goes_through_every_board_and_coming_back_keeps_the_board():
    total = len(SETTINGS["boards"])
    with open_app() as (page, _, _):
        go(page, "unblock")
        page.locator(".unblock-next").click()
        name = STRINGS["unblock.boardName"].format(number=2, total=total, level=STRINGS["unblock.level." + SETTINGS["boards"][1]["level"]])
        assert page.locator(".unblock-board-name").inner_text() == name
        assert status(page) == name
        go(page, "menu")
        go(page, "unblock")
        assert page.locator(".unblock-board-name").inner_text() == name, "the board in use stays chosen"
        for _ in range(total - 1):
            page.locator(".unblock-next").click()
        assert page.locator(".unblock-board-name").inner_text().startswith("Board 1 of"), "after the last, the first"


def test_every_block_is_a_large_target_on_a_phone_and_nothing_is_counted():
    with open_app(viewport={"width": 360, "height": 740}) as (page, _, _):
        go(page, "unblock")
        for _ in SETTINGS["boards"]:
            sizes = page.locator(".unblock-block").evaluate_all(
                "els => els.map(e => { const b = e.getBoundingClientRect(); return Math.min(b.width, b.height); })")
            assert min(sizes) >= 44, f"smallest block {min(sizes):.1f}px"
            page.locator(".unblock-next").click()
        # Everything shown, without the intro, which says there is no score and no time limit.
        text = page.evaluate("""(() => { const m = document.querySelector('main').cloneNode(true);
            m.querySelector('#unblock-intro').remove(); return m.textContent.toLowerCase(); })()""")
        for word in ("score", "moves", "time", "lose", "failed"):
            assert word not in text, f"the puzzle shows no {word}"


def test_in_forced_colors_the_blue_block_stays_distinct():
    with open_app() as (page, _, _):
        page.emulate_media(forced_colors="active")
        go(page, "unblock")
        width = lambda e: e.evaluate("e => getComputedStyle(e, '::before').borderTopWidth")
        assert width(block(page, "A")) != width(page.locator(".unblock-block:not(.key)").first)


def test_under_reduced_motion_the_blocks_do_not_slide():
    with open_app(reduced_motion="reduce") as (page, _, _):
        go(page, "unblock")
        duration = page.locator(".unblock-block").first.evaluate("e => getComputedStyle(e).transitionDuration")
        assert set(duration.replace(" ", "").split(",")) == {"0s"}
