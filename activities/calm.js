// Calm (owner, 2026-10-07): slow musical pads, and simple geometric shapes that fade in and out
// like a screen saver. "Black screen" covers everything in black; one tap or key brings the
// screen back, and the music keeps playing. Nothing to do, nothing to win.
// The sound is the background sound (RLG-045): this screen chooses it, and it keeps playing after
// the person leaves, until they choose Off here or Stop in the shell's sound bar.
// Under reduced motion the shapes do not move or grow; they only fade.


let run = null;

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
      <fieldset class="calm-mode" aria-describedby="nature-hint">
        <legend>${t("calm.mode")}</legend>
        ${config.calm.modes.map((mode) => `<label class="choice"><input type="radio" name="calm-mode" value="${mode}"
          ${mode === ctx.calmMode ? "checked" : ""}><span>${t(`calm.mode.${mode}`)}</span></label>`).join("")}
      </fieldset>
      <p id="nature-hint" class="hint">${t("calm.natureHint")}</p>
      <div class="calm-stage">
        <svg class="calm-field" viewBox="0 0 400 300" aria-hidden="true" focusable="false"></svg>
        <div class="calm-stage-actions" hidden>
          <button type="button" class="button calm-help">${t("help.open")}</button>
          <button type="button" class="button calm-exit">${t("calm.exitFullScreen")}</button>
        </div>
      </div>
      <p class="hint calm-sound-note" hidden>${t("calm.soundsOff")}</p>
      <div class="exercise-actions">
        <button type="button" class="button full-screen">${t("calm.fullScreen")}</button>
        <button type="button" class="button black-screen" aria-describedby="black-hint">${t("calm.blackScreen")}</button>
      </div>
      <p id="black-hint" class="hint">${t("calm.blackHint")}</p>
    </section>`;

  const field = container.querySelector(".calm-field");
  const stageBox = container.querySelector(".calm-stage");
  const blackButton = container.querySelector(".black-screen");
  // Off, Music (tonal pads), Nature (rain or waves, chosen in Settings) or Both, remembered in
  // Settings (owner, 2026-10-07; RLG-043, RLG-045). The shell owns the sound: a choice here is saved,
  // and the shell plays it.
  ctx.startBackground();
  const current = { timers: [], cover: null, wake: ctx.keepAwake() };
  run = current;
  current.note = container.querySelector(".calm-sound-note");
  current.note.hidden = ctx.soundsOn;

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

  // The black screen is one large button over everything, so a tap, Enter, Space or Escape all
  // bring the screen back, and a screen reader can name it.
  function blackOut() {
    const cover = document.createElement("button");
    cover.type = "button";
    cover.className = "black-cover";
    cover.setAttribute("aria-label", t("calm.blackLabel"));
    const restore = () => {
      cover.remove();
      current.cover = null;
      stageBox.classList.remove("asleep");
      blackButton.focus();
    };
    cover.addEventListener("click", restore);
    cover.addEventListener("keydown", (event) => { if (event.key === "Escape") restore(); });
    document.body.append(cover);
    current.cover = cover;
    // The shapes and the sky stop moving under the cover: nothing unseen is drawn.
    stageBox.classList.add("asleep");
    cover.focus();
  }

  container.querySelectorAll("input[name=calm-mode]").forEach((input) => input.addEventListener("change", () => {
    ctx.saveCalmMode(input.value); // the shell owns Settings (AUD-066) and the background sound
  }));

  // Full screen (owner, 2026-10-07): the stage fills the screen. The browser's own full screen is
  // used where it exists; the CSS class does the work everywhere, including phones without it.
  const stage = stageBox;
  const exit = container.querySelector(".calm-exit");
  const stageActions = container.querySelector(".calm-stage-actions");
  const fullButton = container.querySelector(".full-screen");
  function leaveFull() {
    stage.classList.remove("full");
    stageActions.hidden = true;
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    fullButton.focus();
  }
  fullButton.addEventListener("click", () => {
    stage.classList.add("full");
    stageActions.hidden = false;
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
  current.leaveFull = () => { if (stage.classList.contains("full")) leaveFull(); };

  blackButton.addEventListener("click", blackOut);
  addShape();
}

// The header's sound button changed. The shell starts or stops the sound; this screen only shows
// or hides its note that sound is off.
export function soundChanged(on) {
  if (!run) return;
  run.note.hidden = on;
}

export function stop() {
  if (run) {
    run.timers.forEach(clearTimeout);
    run.wake();
    if (run.cover) run.cover.remove();
    if (run.leaveFull && document.fullscreenElement) document.exitFullscreen().catch(() => {});
  }
  run = null;
}
