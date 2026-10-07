// The colour sort (REQ-014): put calm tiles in order, from lightest to darkest. No score, no
// failure, no timer. Every tile is a button with a name for its shade, so the task works without
// sight. Touch and keyboard use the same two steps: choose a tile, then choose the tile to swap it
// with. Arrow keys move between tiles. A polite live region says what happened.

let run = null;

function shuffled(items) {
  const copy = [...items];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

export function start(container, ctx) {
  stop();
  const { t, config } = ctx;
  const settings = config.sort;
  const current = { palette: -1, order: [], chosen: null };
  run = current;

  container.innerHTML = `
    <section class="activity sort">
      <h1>${t("sort.title")}</h1>
      <p class="exercise-intro" id="sort-intro">${t("sort.intro")}</p>
      <ul class="sort-tiles" aria-describedby="sort-intro"></ul>
      <p class="sort-status" aria-live="polite"></p>
      <div class="exercise-actions">
        <button type="button" class="button new-colours">${t("sort.newColours")}</button>
      </div>
    </section>`;

  const list = container.querySelector(".sort-tiles");
  list.style.setProperty("--count", String(settings.lightness.length));
  const status = container.querySelector(".sort-status");

  const shadeName = (shade) => t("sort.tileLabel", {
    hue: t(`sort.hue.${settings.palettes[current.palette].name}`),
    shade: t(`sort.shade.${shade}`),
  });

  function isSorted() {
    return current.order.every((shade, i) => shade === i);
  }

  function render(focusIndex) {
    const palette = settings.palettes[current.palette];
    list.replaceChildren(...current.order.map((shade, position) => {
      const item = document.createElement("li");
      const tile = document.createElement("button");
      tile.type = "button";
      tile.className = "sort-tile";
      tile.dataset.shade = String(shade);
      tile.style.backgroundColor = `hsl(${palette.hue} ${palette.saturation}% ${settings.lightness[shade]}%)`;
      tile.setAttribute("aria-label", t("sort.tilePosition", {
        name: shadeName(shade), position: position + 1, total: current.order.length }));
      tile.setAttribute("aria-pressed", String(current.chosen === position));
      tile.tabIndex = position === (focusIndex ?? 0) ? 0 : -1;
      tile.addEventListener("click", () => choose(position));
      tile.addEventListener("keydown", (event) => arrow(event, position));
      item.append(tile);
      return item;
    }));
    if (focusIndex !== undefined) list.children[focusIndex]?.querySelector("button").focus();
  }

  // Arrow keys move focus between tiles (one tab stop for the whole row).
  function arrow(event, position) {
    const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[event.key];
    const edge = { Home: 0, End: current.order.length - 1 }[event.key];
    if (step === undefined && edge === undefined) return;
    event.preventDefault();
    const target = edge ?? Math.min(current.order.length - 1, Math.max(0, position + step));
    [...list.querySelectorAll("button")].forEach((b, i) => { b.tabIndex = i === target ? 0 : -1; });
    list.children[target].querySelector("button").focus();
  }

  function choose(position) {
    if (current.chosen === null) {
      current.chosen = position;
      ctx.audio.play("choose");
      status.textContent = t("sort.chosen", { name: shadeName(current.order[position]) });
      render(position);
      return;
    }
    const from = current.chosen;
    current.chosen = null;
    if (from === position) {
      status.textContent = t("sort.unchosen");
      render(position);
      return;
    }
    [current.order[from], current.order[position]] = [current.order[position], current.order[from]];
    ctx.audio.play(isSorted() ? "done" : "swap");
    status.textContent = isSorted()
      ? t("sort.done")
      : t("sort.swapped", { name: shadeName(current.order[position]), position: position + 1 });
    render(position);
  }

  function newColours() {
    current.palette = (current.palette + 1) % settings.palettes.length;
    const shades = [...Array(settings.lightness.length).keys()];
    do { current.order = shuffled(shades); } while (isSorted());
    current.chosen = null;
    status.textContent = "";
    render();
  }

  container.querySelector(".new-colours").addEventListener("click", newColours);
  newColours();
}

export function stop() {
  run = null;
}
