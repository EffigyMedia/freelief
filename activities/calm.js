// The Visualizer (owner, 2026-10-07): simple geometric shapes that fade in and out like a screen
// saver. "Black screen" covers everything in black; one tap or key brings the screen back, and any
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

// Each shape is drawn inside a 100 x 100 box, as an SVG element name and its attributes.
const FORMS = [
  ["circle", { cx: 50, cy: 50, r: 40 }],
  ["polygon", { points: "50,8 92,84 8,84" }],
  ["rect", { x: 14, y: 14, width: 72, height: 72, rx: 6 }],
  ["polygon", { points: "50,6 89,28 89,72 50,94 11,72 11,28" }],
  ["polygon", { points: "50,6 94,50 50,94 6,50" }],
  ["circle", { cx: 50, cy: 50, r: 24 }],
];

export function start(container, ctx) {
  stop();
  const { t, config, motion } = ctx;
  const settings = config.calm;
  const still = motion.reducedMotion();

  container.innerHTML = `
    <section class="activity calm">
      <h1>${t("calm.title")}</h1>
      <p class="visually-hidden">${t("calm.intro")}</p>
      <div class="calm-stage">
        <svg class="calm-field" viewBox="0 0 400 300" aria-hidden="true" focusable="false"></svg>
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

  const random = (min, max) => min + Math.random() * (max - min);
  // A timer drops its own id when it fires, so the list holds only pending timers (AUD-038, AUD-083).
  function later(callback, ms) {
    const id = setTimeout(() => {
      current.timers = current.timers.filter((pending) => pending !== id);
      callback();
    }, ms);
    current.timers.push(id);
  }

  function addShape() {
    if (run !== current) return;
    // Under the black screen nothing new is drawn, which saves power (owner, 2026-10-08).
    if (!current.cover && field.childElementCount < settings.maxShapes) {
      const [tag, attributes] = FORMS[Math.floor(Math.random() * FORMS.length)];
      const size = random(settings.minSize, settings.maxSize);
      const group = document.createElementNS(SVG_NS, "g");
      const x = random(0, 400 - size), y = random(0, 300 - size);
      group.setAttribute("transform", `translate(${x.toFixed(1)} ${y.toFixed(1)}) scale(${(size / 100).toFixed(3)})`);
      const inner = document.createElementNS(SVG_NS, "g");
      inner.setAttribute("class", still ? "calm-shape still" : "calm-shape");
      inner.style.animationDuration = `${settings.shapeLifeSeconds}s`;
      inner.style.setProperty("--spin", `${random(-25, 25).toFixed(0)}deg`);
      const shape = document.createElementNS(SVG_NS, tag);
      for (const [name, value] of Object.entries(attributes)) shape.setAttribute(name, value);
      inner.append(shape);
      group.append(inner);
      field.append(group);
      later(() => group.remove(), settings.shapeLifeSeconds * 1000);
    }
    later(addShape, settings.shapeEveryMs);
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
  addShape();
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
