// Zen Garden (RLG-055, owner 2026-10-10): a tray of sand to rake, with a few stones and a small plant
// to place, move and remove. It replaces Trace a shape. No score, no failure, no timer and no end.
//
// A finger or a mouse drawn across the sand rakes a set of parallel lines along its path. Around each
// stone and plant the sand keeps a few rings, as in a raked garden, so the lines seem to flow around
// them. The sand is one focusable control: the arrow keys move a rake and draw as it moves, so the
// task works with a keyboard alone. Each stone and plant is a button with a name; the arrow keys move
// a chosen one, and Remove takes it away. Smooth the sand clears the lines and keeps the stones.
// Everything is SVG; no canvas is used, by the architecture rule.

let run = null;

const SVG_NS = "http://www.w3.org/2000/svg";
const W = 400;
const H = 300;

function svg(tag, attributes = {}) {
  const node = document.createElementNS(SVG_NS, tag);
  for (const [name, value] of Object.entries(attributes)) node.setAttribute(name, value);
  return node;
}

export function start(container, ctx) {
  stop();
  const { t, config, audio } = ctx;
  const settings = config.garden;
  const current = { strokes: [], items: [], chosen: null, last: null, rake: { x: W / 2, y: H / 2 }, sound: 0 };
  run = current;

  container.innerHTML = `
    <section class="activity garden">
      <h1>${t("garden.title")}</h1>
      <p class="visually-hidden" id="garden-intro">${t("garden.intro")}</p>
      <div class="garden-tray">
        <svg class="garden-sand" viewBox="0 0 ${W} ${H}" role="group" aria-label="${t("garden.trayLabel")}"
             aria-describedby="garden-intro">
          <rect class="garden-rake-area" x="0" y="0" width="${W}" height="${H}" tabindex="0" role="button"
                aria-label="${t("garden.sandLabel")}"></rect>
          <defs><mask id="garden-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="${W}" height="${H}">
            <rect x="0" y="0" width="${W}" height="${H}" fill="white"></rect><g class="garden-holes"></g>
          </mask></defs>
          <g class="garden-lines" mask="url(#garden-mask)" aria-hidden="true"></g>
          <g class="garden-rings" aria-hidden="true"></g>
          <g class="garden-items"></g>
          <circle class="garden-rake" r="5" aria-hidden="true" visibility="hidden"></circle>
        </svg>
      </div>
      <p class="garden-status" aria-live="polite"></p>
      <div class="exercise-actions">
        <button type="button" class="button garden-add-stone">${t("garden.addStone")}</button>
        <button type="button" class="button garden-add-plant">${t("garden.addPlant")}</button>
        <button type="button" class="button garden-remove" disabled>${t("garden.remove")}</button>
        <button type="button" class="button garden-smooth">${t("garden.smooth")}</button>
      </div>
    </section>`;

  const sand = container.querySelector(".garden-sand");
  const area = container.querySelector(".garden-rake-area");
  const lines = container.querySelector(".garden-lines");
  const rings = container.querySelector(".garden-rings");
  const holes = container.querySelector(".garden-holes");
  const itemsLayer = container.querySelector(".garden-items");
  const rakeDot = container.querySelector(".garden-rake");
  const status = container.querySelector(".garden-status");
  const removeButton = container.querySelector(".garden-remove");

  // A point of the pointer in the sand's own units.
  function local(event) {
    const box = sand.getBoundingClientRect();
    return { x: ((event.clientX - box.left) / box.width) * W, y: ((event.clientY - box.top) / box.height) * H };
  }
  const clamp = (p) => ({ x: Math.min(W, Math.max(0, p.x)), y: Math.min(H, Math.max(0, p.y)) });

  // A soft brush of sand, at most once every few hundred milliseconds while raking.
  function sandSound() {
    const now = performance.now();
    if (now - current.sound < settings.soundEveryMs) return;
    current.sound = now;
    audio.sand();
  }

  // One rake stroke is a set of parallel lines, the tines, offset across the direction of travel.
  function rakeTo(point) {
    const from = current.last;
    current.last = point;
    if (!from) return;
    const dx = point.x - from.x;
    const dy = point.y - from.y;
    const length = Math.hypot(dx, dy);
    if (length < 0.5) return;
    const nx = -dy / length;
    const ny = dx / length;
    const half = (settings.tines - 1) / 2;
    for (let i = 0; i < settings.tines; i++) {
      const offset = (i - half) * settings.tineGap;
      lines.append(svg("line", {
        x1: (from.x + nx * offset).toFixed(1), y1: (from.y + ny * offset).toFixed(1),
        x2: (point.x + nx * offset).toFixed(1), y2: (point.y + ny * offset).toFixed(1),
      }));
    }
    // The oldest lines go first, so the garden never grows without end.
    while (lines.childElementCount > settings.maxLines) lines.firstElementChild.remove();
    sandSound();
  }

  // ---- stones and plants -------------------------------------------------------------------

  // Inside the rings around a stone or a plant the raked lines do not show, so the lines seem to
  // flow around it, as in a raked garden.
  function drawRings() {
    holes.replaceChildren(...current.items.map((item) => svg("circle", {
      cx: item.x, cy: item.y, r: item.size + settings.ringGap * (settings.rings + 0.5), fill: "black",
    })));
    rings.replaceChildren(...current.items.flatMap((item) =>
      [...Array(settings.rings).keys()].map((i) => svg("circle", {
        cx: item.x, cy: item.y, r: item.size + settings.ringGap * (i + 1),
      }))));
  }

  function itemName(item) {
    const name = item.kind === "stone" ? t("garden.stone", { number: item.number }) : t("garden.plant", { number: item.number });
    return t("garden.itemAt", { name, across: Math.round((item.x / W) * 100), down: Math.round((item.y / H) * 100) });
  }

  function place(item) {
    item.node.setAttribute("transform", `translate(${item.x.toFixed(1)} ${item.y.toFixed(1)})`);
    item.node.setAttribute("aria-label", itemName(item));
    drawRings();
  }

  function choose(item) {
    if (current.chosen) current.chosen.node.setAttribute("aria-pressed", "false");
    current.chosen = item;
    removeButton.disabled = !item;
    if (item) {
      item.node.setAttribute("aria-pressed", "true");
      status.textContent = t("garden.chosen", { name: itemName(item) });
    }
  }

  // A free place for a new item: away from the others, and inside the sand.
  function freeSpot(size) {
    for (let tries = 0; tries < 40; tries++) {
      const spot = { x: size + Math.random() * (W - 2 * size), y: size + Math.random() * (H - 2 * size) };
      if (current.items.every((other) => Math.hypot(other.x - spot.x, other.y - spot.y) > other.size + size + settings.ringGap * settings.rings)) {
        return spot;
      }
    }
    return { x: W / 2, y: H / 2 };
  }

  function add(kind, quiet = false) {
    const count = current.items.filter((item) => item.kind === kind).length;
    if (current.items.length >= settings.maxItems) {
      status.textContent = t("garden.full");
      return;
    }
    const size = kind === "stone" ? settings.stoneSize : settings.plantSize;
    const item = { kind, size, number: count + 1, ...freeSpot(size) };
    const node = svg("g", { class: `garden-item ${kind}`, tabindex: "0", role: "button", "aria-pressed": "false" });
    // A round hit area under the drawing, so every item is a target at least as wide as it is long.
    node.append(svg("circle", { class: "hit", r: size }));
    if (kind === "stone") {
      node.append(svg("ellipse", { rx: size, ry: size * 0.78 }), svg("ellipse", { class: "shine", rx: size * 0.45, ry: size * 0.3, cx: -size * 0.25, cy: -size * 0.25 }));
    } else {
      // A small plant: a few leaves around a center.
      for (let i = 0; i < 5; i++) {
        node.append(svg("ellipse", { rx: size * 0.32, ry: size * 0.9, transform: `rotate(${i * 72}) translate(0 ${-size * 0.55})` }));
      }
      node.append(svg("circle", { class: "heart", r: size * 0.25 }));
    }
    item.node = node;
    node.addEventListener("pointerdown", (event) => grab(event, item));
    node.addEventListener("click", () => { if (!current.moved) choose(current.chosen === item ? null : item); });
    node.addEventListener("keydown", (event) => itemKey(event, item));
    itemsLayer.append(node);
    current.items.push(item);
    place(item);
    if (quiet) return;
    choose(item);
    audio.play("choose");
    ctx.haptic("choose");
    status.textContent = t("garden.added", { name: itemName(item) });
    node.focus();
  }

  function remove(item) {
    if (!item) return;
    item.node.remove();
    current.items = current.items.filter((other) => other !== item);
    drawRings();
    choose(null);
    status.textContent = t("garden.removed");
    area.focus();
  }

  // A drag moves a stone or a plant; a tap with no movement chooses it.
  function grab(event, item) {
    if (event.button !== 0) return;
    event.stopPropagation();
    current.moved = false;
    const startPoint = local(event);
    const origin = { x: item.x, y: item.y };
    item.node.setPointerCapture?.(event.pointerId);
    const move = (moveEvent) => {
      const point = local(moveEvent);
      if (!current.moved && Math.hypot(point.x - startPoint.x, point.y - startPoint.y) < settings.dragThreshold) return;
      current.moved = true;
      const to = clamp({ x: origin.x + point.x - startPoint.x, y: origin.y + point.y - startPoint.y });
      item.x = to.x;
      item.y = to.y;
      place(item);
    };
    const up = () => {
      item.node.removeEventListener("pointermove", move);
      item.node.removeEventListener("pointerup", up);
      item.node.removeEventListener("pointercancel", up);
      if (current.moved) status.textContent = itemName(item);
      setTimeout(() => { current.moved = false; }, 0);
    };
    item.node.addEventListener("pointermove", move);
    item.node.addEventListener("pointerup", up);
    item.node.addEventListener("pointercancel", up);
  }

  const ARROWS = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] };

  function itemKey(event, item) {
    const step = ARROWS[event.key];
    if (step) {
      event.preventDefault();
      const to = clamp({ x: item.x + step[0] * settings.keyStep, y: item.y + step[1] * settings.keyStep });
      item.x = to.x;
      item.y = to.y;
      place(item);
      status.textContent = itemName(item);
    } else if (event.key === "Delete" || event.key === "Backspace") {
      event.preventDefault();
      remove(item);
    } else if (event.key === "Escape") {
      choose(null);
    }
  }

  // ---- raking ----------------------------------------------------------------------------------

  area.addEventListener("pointerdown", (event) => {
    if (event.button !== 0) return;
    area.setPointerCapture?.(event.pointerId);
    current.last = local(event);
    choose(null);
  });
  area.addEventListener("pointermove", (event) => {
    if (!current.last) return;
    rakeTo(clamp(local(event)));
  });
  const endRake = () => { current.last = null; };
  area.addEventListener("pointerup", endRake);
  area.addEventListener("pointercancel", endRake);

  // The arrow keys move a rake across the sand and draw as it moves; the dot shows where it is.
  area.addEventListener("focus", () => rakeDot.setAttribute("visibility", "visible"));
  area.addEventListener("blur", () => rakeDot.setAttribute("visibility", "hidden"));
  area.addEventListener("keydown", (event) => {
    const step = ARROWS[event.key];
    if (!step) return;
    event.preventDefault();
    const from = { ...current.rake };
    const to = clamp({ x: from.x + step[0] * settings.keyStep, y: from.y + step[1] * settings.keyStep });
    current.last = from;
    rakeTo(to);
    current.last = null;
    current.rake = to;
    rakeDot.setAttribute("cx", to.x.toFixed(1));
    rakeDot.setAttribute("cy", to.y.toFixed(1));
  });
  rakeDot.setAttribute("cx", current.rake.x);
  rakeDot.setAttribute("cy", current.rake.y);

  container.querySelector(".garden-add-stone").addEventListener("click", () => add("stone"));
  container.querySelector(".garden-add-plant").addEventListener("click", () => add("plant"));
  removeButton.addEventListener("click", () => remove(current.chosen));
  container.querySelector(".garden-smooth").addEventListener("click", () => {
    lines.replaceChildren();
    status.textContent = t("garden.smoothed");
  });

  // The garden starts with a few stones, so there is something to rake around.
  for (let i = 0; i < settings.startStones; i++) add("stone", true);
}

export function stop() {
  run = null;
}
