// Unblock (RLG-040, owner 2026-10-09): a calm sliding-block puzzle that replaces Sort colors. Blocks
// lie on a 6 by 6 board; each slides only along its length. Slide them to make a way for the blue
// block to leave through the gap in the right edge. No score, no move count, no timer and no losing
// state: Undo takes back any move, and Start again resets the board. The boards come from
// config.json, from easy to hard, and every one is solvable (a test solves them all).
//
// Every block is a button with a name ("Block 3, down, column 4, rows 1 to 3"). Three ways to move:
// drag a block along its length; or press an arrow key on a focused block; or choose a block (tap,
// Enter or Space) and use the two Slide buttons, which a screen reader reaches as plain buttons.
// A polite live region says what happened.

let run = null;
// The board in use stays chosen while the app is open, so coming back continues it.
let boardIndex = 0;

const KEY = "A";

function parseBoard(rows) {
  const cells = new Map();
  rows.forEach((line, r) => [...line].forEach((ch, c) => {
    if (ch === ".") return;
    if (!cells.has(ch)) cells.set(ch, []);
    cells.get(ch).push([r, c]);
  }));
  // Blocks are numbered in reading order; the key block is the blue one and has no number.
  let number = 0;
  return [...cells.entries()].map(([id, list]) => {
    const across = new Set(list.map(([r]) => r)).size === 1;
    const row = Math.min(...list.map(([r]) => r));
    const col = Math.min(...list.map(([, c]) => c));
    return { id, key: id === KEY, number: id === KEY ? 0 : ++number, across, length: list.length, row, col };
  });
}

export function start(container, ctx) {
  stop();
  const { t, config, motion, audio } = ctx;
  const settings = config.unblock;
  const size = settings.size;
  const current = { blocks: [], history: [], chosen: null, drag: null, dragged: false, free: false };
  run = current;

  container.innerHTML = `
    <section class="activity unblock">
      <h1>${t("unblock.title")}</h1>
      <p class="visually-hidden" id="unblock-intro">${t("unblock.intro")}</p>
      <p class="unblock-board-name"></p>
      <div class="unblock-board" role="group" aria-label="${t("unblock.boardLabel")}"
           aria-describedby="unblock-intro">
        <span class="unblock-exit" aria-hidden="true"></span>
      </div>
      <div class="unblock-slide" hidden>
        <button type="button" class="button slide-back"></button>
        <button type="button" class="button slide-on"></button>
      </div>
      <p class="unblock-status" aria-live="polite"></p>
      <div class="exercise-actions">
        <button type="button" class="button unblock-undo">${t("unblock.undo")}</button>
        <button type="button" class="button unblock-restart">${t("unblock.restart")}</button>
        <button type="button" class="button unblock-next">${t("unblock.next")}</button>
      </div>
    </section>`;

  const board = container.querySelector(".unblock-board");
  const boardName = container.querySelector(".unblock-board-name");
  const status = container.querySelector(".unblock-status");
  const slideBar = container.querySelector(".unblock-slide");
  const [backButton, onButton] = slideBar.querySelectorAll("button");
  board.style.setProperty("--size", String(size));
  board.style.setProperty("--exit-row", String(settings.exitRow));
  if (motion.reducedMotion()) board.classList.add("still");

  const nameOf = (block) => {
    const name = block.key ? t("unblock.keyName") : t("unblock.blockName", { number: block.number });
    return block.across
      ? t("unblock.across", { name, row: block.row + 1, from: block.col + 1, to: block.col + block.length })
      : t("unblock.down", { name, col: block.col + 1, from: block.row + 1, to: block.row + block.length });
  };

  // How far a block can slide each way before it meets another block or the edge. The key block
  // can also leave through the exit, which is one step past the right edge.
  function room(block) {
    const filled = new Set();
    for (const other of current.blocks) {
      if (other === block || other.gone) continue;
      for (let k = 0; k < other.length; k++) {
        filled.add(other.across ? `${other.row},${other.col + k}` : `${other.row + k},${other.col}`);
      }
    }
    const at = (step) => (block.across
      ? `${block.row},${block.col + step}` : `${block.row + step},${block.col}`);
    const from = block.across ? block.col : block.row;
    let back = 0;
    while (from - back - 1 >= 0 && !filled.has(at(-back - 1))) back += 1;
    let on = 0;
    while (from + block.length + on < size && !filled.has(at(block.length + on))) on += 1;
    return { back, on };
  }

  function place(block) {
    block.element.style.setProperty("--row", String(block.row));
    block.element.style.setProperty("--col", String(block.col));
    block.element.setAttribute("aria-label", nameOf(block));
  }

  function render() {
    board.querySelectorAll(".unblock-block").forEach((element) => element.remove());
    for (const block of current.blocks) {
      const element = document.createElement("button");
      element.type = "button";
      element.className = block.key ? "unblock-block key" : "unblock-block";
      element.dataset.block = block.id;
      element.style.setProperty("--length", String(block.length));
      element.classList.add(block.across ? "across" : "down");
      element.setAttribute("aria-pressed", "false");
      element.addEventListener("click", () => {
        if (current.dragged) return;
        choose(block);
      });
      element.addEventListener("keydown", (event) => arrow(event, block));
      element.addEventListener("pointerdown", (event) => pointerDown(event, block));
      element.addEventListener("pointermove", (event) => pointerMove(event));
      element.addEventListener("pointerup", () => pointerUp());
      element.addEventListener("pointercancel", () => pointerUp());
      block.element = element;
      place(block);
      board.append(element);
    }
  }

  // Slide a block `steps` cells along its length (negative: left or up). Returns whether it moved.
  function slide(block, steps, { record = true } = {}) {
    if (!steps || current.free) return false;
    if (block.across) block.col += steps;
    else block.row += steps;
    if (record) current.history.push({ id: block.id, steps });
    place(block);
    // The key block at the right edge leaves through the exit: the board is solved.
    if (block.key && block.col + block.length === size) {
      current.free = true;
      block.element.classList.add("free");
      audio.play("done");
      ctx.haptic("done");
      status.textContent = t("unblock.free");
      choose(null);
      container.querySelector(".unblock-next").focus();
      return true;
    }
    audio.play("swap");
    ctx.haptic("swap");
    status.textContent = nameOf(block);
    updateSlideBar();
    return true;
  }

  function tryStep(block, direction) {
    const space = room(block);
    if ((direction < 0 ? space.back : space.on) === 0) {
      status.textContent = t("unblock.noRoom");
      return;
    }
    slide(block, direction);
  }

  // Arrow keys on a focused block slide it along its length. Arrows across it say which way it goes.
  function arrow(event, block) {
    const along = block.across
      ? { ArrowLeft: -1, ArrowRight: 1 }[event.key]
      : { ArrowUp: -1, ArrowDown: 1 }[event.key];
    const across = block.across
      ? { ArrowUp: 1, ArrowDown: 1 }[event.key]
      : { ArrowLeft: 1, ArrowRight: 1 }[event.key];
    if (along !== undefined) {
      event.preventDefault();
      tryStep(block, along);
    } else if (across !== undefined) {
      event.preventDefault();
      status.textContent = t(block.across ? "unblock.onlyAcross" : "unblock.onlyDown");
    } else if (event.key === "Escape" && current.chosen) {
      choose(null);
    }
  }

  // Choosing a block shows the two Slide buttons for it. Choosing it again, or Escape, lets it go.
  function choose(block) {
    const next = block && block !== current.chosen && !current.free ? block : null;
    if (current.chosen) current.chosen.element.setAttribute("aria-pressed", "false");
    current.chosen = next;
    if (next) {
      next.element.setAttribute("aria-pressed", "true");
      audio.play("choose");
      ctx.haptic("choose");
      status.textContent = t("unblock.chosen", { name: nameOf(next) });
    } else if (block && !current.free) {
      status.textContent = t("unblock.letGo");
    }
    updateSlideBar();
  }

  function updateSlideBar() {
    const block = current.chosen;
    slideBar.hidden = !block;
    if (!block) return;
    backButton.textContent = t(block.across ? "unblock.slideLeft" : "unblock.slideUp");
    onButton.textContent = t(block.across ? "unblock.slideRight" : "unblock.slideDown");
  }
  backButton.addEventListener("click", () => current.chosen && tryStep(current.chosen, -1));
  onButton.addEventListener("click", () => current.chosen && tryStep(current.chosen, 1));

  // A drag slides a block cell by cell, as far as there is room. A tap with no drag chooses it.
  function pointerDown(event, block) {
    if (event.button !== 0 || current.free) return;
    current.dragged = false;
    const cell = board.clientWidth / size;
    const space = room(block);
    current.drag = { block, cell, space, x: event.clientX, y: event.clientY, steps: 0, active: false };
    block.element.setPointerCapture?.(event.pointerId);
  }

  function pointerMove(event) {
    const drag = current.drag;
    if (!drag) return;
    const distance = drag.block.across ? event.clientX - drag.x : event.clientY - drag.y;
    if (!drag.active && Math.abs(distance) < settings.dragThreshold) return;
    drag.active = true;
    const steps = Math.max(-drag.space.back, Math.min(drag.space.on, Math.round(distance / drag.cell)));
    if (steps === drag.steps) return;
    // The block follows the finger without a record; the whole drag is one move when it ends.
    slide(drag.block, steps - drag.steps, { record: false });
    drag.steps = steps;
  }

  function pointerUp() {
    const drag = current.drag;
    current.drag = null;
    if (!drag?.active) return;
    // A drag ends without a click; the click that the browser may send after it is not a choice.
    current.dragged = true;
    setTimeout(() => { current.dragged = false; }, 0);
    if (drag.steps) current.history.push({ id: drag.block.id, steps: drag.steps });
  }

  function undo() {
    const last = current.history.pop();
    if (!last) {
      status.textContent = t("unblock.nothingToUndo");
      return;
    }
    const block = current.blocks.find((b) => b.id === last.id);
    if (current.free) {
      current.free = false;
      block.element.classList.remove("free");
    }
    slide(block, -last.steps, { record: false });
    status.textContent = t("unblock.undone", { name: nameOf(block) });
  }

  function load(index) {
    boardIndex = index % settings.boards.length;
    const spec = settings.boards[boardIndex];
    current.blocks = parseBoard(spec.rows);
    current.history = [];
    current.free = false;
    current.chosen = null;
    current.drag = null;
    boardName.textContent = t("unblock.boardName", {
      number: boardIndex + 1, total: settings.boards.length, level: t(`unblock.level.${spec.level}`) });
    render();
    updateSlideBar();
  }

  container.querySelector(".unblock-undo").addEventListener("click", undo);
  container.querySelector(".unblock-restart").addEventListener("click", () => {
    load(boardIndex);
    status.textContent = t("unblock.restarted");
  });
  container.querySelector(".unblock-next").addEventListener("click", () => {
    load(boardIndex + 1);
    status.textContent = boardName.textContent;
  });
  load(boardIndex);
}

export function stop() {
  run = null;
}
