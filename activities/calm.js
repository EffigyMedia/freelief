// The Kaleidoscope (owner, 2026-10-07; redrawn 2026-10-10, RLG-057): a slow, full-width kaleidoscope
// of soft shapes and colors. One wedge of shapes is mirrored around the center into a full circle;
// the whole turns very slowly and its colors drift, and every so often a new pattern fades in over
// the old one. Nothing flashes: no brightness changes faster than a slow fade. "Black screen" covers everything in black; one tap or key brings the screen back, and any
// sound keeps playing. Nothing to do, nothing to win. Sound is chosen in the sound bar of the
// header, on every screen (RLG-049); this screen has no sound choice of its own.
// Under reduced motion the shapes do not move or grow; they only fade.


let run = null;

// Everything on the page except `keep` and what holds it becomes inert: Tab and a screen reader's
// cursor cannot reach what a cover hides (web-interface-review, 2026-10-09). Returns the undo.
function inertAround(keep) {
  const made = [];
  for (let node = keep; node && node !== document.body; node = node.parentElement) {
    for (const sibling of node.parentElement.children) {
      if (sibling !== node && !sibling.inert) {
        sibling.inert = true;
        made.push(sibling);
      }
    }
  }
  return () => made.forEach((element) => { element.inert = false; });
}

const SVG_NS = "http://www.w3.org/2000/svg";

// One wedge of a kaleidoscope, mirrored into a circle: the wedge is copied `folds` times, every other
// copy flipped, so the pattern is symmetric like a real kaleidoscope.
function pattern(settings) {
  const step = 360 / settings.folds;
  const random = (min, max) => min + Math.random() * (max - min);
  const hueBase = random(0, 360);
  const cell = document.createElementNS(SVG_NS, "g");
  for (let i = 0; i < settings.shapesPerCell; i++) {
    // Out to the corners of the square (the corners are about 141 units from the center).
    const r = random(6, 145);
    const a = (random(4, step - 4) * Math.PI) / 180;
    const x = r * Math.cos(a);
    const y = r * Math.sin(a);
    const size = random(6, 20);
    const kind = Math.floor(random(0, 4));
    const color = `hsl(${((hueBase + random(-60, 60)) % 360 + 360) % 360} ${Math.round(random(40, 70))}% ${Math.round(random(55, 72))}%)`;
    let shape;
    if (kind === 0) {
      shape = document.createElementNS(SVG_NS, "circle");
      shape.setAttribute("r", size.toFixed(1));
    } else if (kind === 1) {
      shape = document.createElementNS(SVG_NS, "ellipse");
      shape.setAttribute("rx", (size * 0.45).toFixed(1));
      shape.setAttribute("ry", (size * 1.3).toFixed(1));
    } else {
      const corners = kind === 2 ? 3 : 4;
      shape = document.createElementNS(SVG_NS, "polygon");
      shape.setAttribute("points", [...Array(corners).keys()].map((k) => {
        const t = (k / corners) * Math.PI * 2;
        return `${(size * Math.cos(t)).toFixed(1)},${(size * Math.sin(t)).toFixed(1)}`;
      }).join(" "));
    }
    shape.setAttribute("transform", `translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${Math.round(random(0, 180))})`);
    shape.setAttribute("fill", color);
    cell.append(shape);
  }
  const layer = document.createElementNS(SVG_NS, "g");
  layer.setAttribute("class", "kaleido-layer");
  for (let i = 0; i < settings.folds; i++) {
    const copy = cell.cloneNode(true);
    copy.setAttribute("transform", i % 2 ? `rotate(${(i + 1) * step}) scale(1 -1)` : `rotate(${i * step})`);
    layer.append(copy);
  }
  return layer;
}

export function start(container, ctx) {
  stop();
  const { t, config, motion } = ctx;
  const settings = config.calm.kaleidoscope;
  const still = motion.reducedMotion();

  container.innerHTML = `
    <section class="activity calm">
      <h1>${t("calm.title")}</h1>
      <p class="visually-hidden">${t("calm.intro")}</p>
      <div class="calm-stage">
        <svg class="calm-field" viewBox="-100 -100 200 200" aria-hidden="true" focusable="false">
          <g class="kaleido-turn"></g>
        </svg>
        <div class="calm-stage-actions" hidden>
          <button type="button" class="button calm-help">${t("help.open")}</button>
          <button type="button" class="button calm-exit">${t("calm.exitFullScreen")}</button>
        </div>
      </div>
      <div class="exercise-actions">
        <button type="button" class="button full-screen">${t("calm.fullScreen")}</button>
        <button type="button" class="button black-screen" aria-describedby="black-hint">${t("calm.blackScreen")}</button>
      </div>
      <p id="black-hint" class="hint">${t("calm.blackHint")}</p>
    </section>`;

  const field = container.querySelector(".calm-field");
  const stageBox = container.querySelector(".calm-stage");
  const blackButton = container.querySelector(".black-screen");
  const current = { timers: [], cover: null, wake: ctx.keepAwake() };
  run = current;

  // A timer drops its own id when it fires, so the list holds only pending timers (AUD-038, AUD-083).
  function later(callback, ms) {
    const id = setTimeout(() => {
      current.timers = current.timers.filter((pending) => pending !== id);
      callback();
    }, ms);
    current.timers.push(id);
  }

  // A new pattern fades in over the old one, and the old one goes when the fade is over. Under the
  // black screen nothing new is drawn, which saves power (owner, 2026-10-08).
  const turn = field.querySelector(".kaleido-turn");
  if (still) field.classList.add("still");
  field.style.setProperty("--turn", `${settings.turnSeconds}s`);
  field.style.setProperty("--hue", `${settings.hueSeconds}s`);
  field.style.setProperty("--fade", `${settings.fadeSeconds}s`);
  function nextPattern() {
    if (run !== current) return;
    if (!current.cover) {
      const layer = pattern(settings);
      turn.append(layer);
      const old = [...turn.children].slice(0, -1);
      // The new pattern fades in while the old one fades out, so the change is one slow cross-fade.
      requestAnimationFrame(() => requestAnimationFrame(() => {
        layer.classList.add("shown");
        old.forEach((g) => g.classList.remove("shown"));
      }));
      later(() => old.forEach((g) => g.remove()), settings.fadeSeconds * 1000 + 100);
    }
    later(nextPattern, settings.patternSeconds * 1000);
  }

  // The black screen is one large button over everything, so a tap or any key brings the screen
  // back, and a screen reader can name it. The page under it is inert.
  function blackOut() {
    const cover = document.createElement("button");
    cover.type = "button";
    cover.className = "black-cover";
    cover.setAttribute("aria-label", t("calm.blackLabel"));
    let release = () => {};
    const restore = () => {
      if (!cover.isConnected) return;
      release();
      cover.remove();
      current.cover = null;
      current.releaseCover = null;
      stageBox.classList.remove("asleep");
      blackButton.focus();
    };
    cover.addEventListener("click", restore);
    cover.addEventListener("keydown", (event) => {
      event.preventDefault();
      restore();
    });
    document.body.append(cover);
    release = inertAround(cover);
    current.cover = cover;
    current.releaseCover = release;
    // The shapes and the sky stop moving under the cover: nothing unseen is drawn.
    stageBox.classList.add("asleep");
    cover.focus();
  }

  // Full screen (owner, 2026-10-07): the stage fills the screen. The browser's own full screen is
  // used where it exists; the CSS class does the work everywhere, including phones without it.
  const stage = stageBox;
  const exit = container.querySelector(".calm-exit");
  const stageActions = container.querySelector(".calm-stage-actions");
  const fullButton = container.querySelector(".full-screen");
  let releaseFull = () => {};
  function leaveFull() {
    releaseFull();
    releaseFull = () => {};
    stage.classList.remove("full");
    stageActions.hidden = true;
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    fullButton.focus();
  }
  fullButton.addEventListener("click", () => {
    stage.classList.add("full");
    stageActions.hidden = false;
    releaseFull = inertAround(stage);
    stage.requestFullscreen?.().catch(() => {});
    exit.focus();
  });
  exit.addEventListener("click", leaveFull);
  // The way to urgent help stays in full screen (AUD-075): it leaves full screen and opens help.
  container.querySelector(".calm-help").addEventListener("click", () => {
    leaveFull();
    document.querySelector(".help-open").click();
  });
  stage.addEventListener("keydown", (event) => { if (event.key === "Escape") leaveFull(); });
  // The browser's own Escape leaves its full screen without a click on the button; the stage leaves too.
  current.onFullscreen = () => {
    if (!document.fullscreenElement && stage.classList.contains("full")) leaveFull();
  };
  document.addEventListener("fullscreenchange", current.onFullscreen);
  current.leaveFull = () => { if (stage.classList.contains("full")) leaveFull(); };

  blackButton.addEventListener("click", blackOut);
  nextPattern();
}

export function stop() {
  if (run) {
    run.timers.forEach(clearTimeout);
    run.wake();
    if (run.cover) {
      run.releaseCover?.();
      run.cover.remove();
    }
    run.leaveFull?.();
    document.removeEventListener("fullscreenchange", run.onFullscreen);
    if (run.leaveFull && document.fullscreenElement) document.exitFullscreen().catch(() => {});
  }
  run = null;
}
