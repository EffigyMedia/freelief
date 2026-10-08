// Calm (owner, 2026-10-07): slow musical pads, and simple geometric shapes that fade in and out
// like a screen saver. "Black screen" covers everything in black; one tap or key brings the
// screen back, and the music keeps playing. Nothing to do, nothing to win.
// Under reduced motion the shapes do not move or grow; they only fade.

import { getSetting, setSetting } from "../settings.js";

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
  const { t, config, motion, audio } = ctx;
  const settings = config.calm;
  const still = motion.reducedMotion();

  container.innerHTML = `
    <section class="activity calm">
      <h1>${t("calm.title")}</h1>
      <p class="visually-hidden">${t("calm.intro")}</p>
      <fieldset class="calm-mode">
        <legend>${t("calm.mode")}</legend>
        ${config.calm.modes.map((mode) => `<label class="choice"><input type="radio" name="calm-mode" value="${mode}"
          ${mode === getSetting("calmMode") ? "checked" : ""}><span>${t(`calm.mode.${mode}`)}</span></label>`).join("")}
      </fieldset>
      <div class="calm-stage">
        <svg class="calm-field" viewBox="0 0 400 300" aria-hidden="true" focusable="false"></svg>
        <button type="button" class="button calm-exit" hidden>${t("calm.exitFullScreen")}</button>
      </div>
      <p class="hint calm-sound-note" hidden>${t("calm.soundsOff")}</p>
      <div class="exercise-actions">
        <button type="button" class="button full-screen">${t("calm.fullScreen")}</button>
        <button type="button" class="button black-screen" aria-describedby="black-hint">${t("calm.blackScreen")}</button>
      </div>
      <p id="black-hint" class="hint">${t("calm.blackHint")}</p>
    </section>`;

  const field = container.querySelector(".calm-field");
  const blackButton = container.querySelector(".black-screen");
  // Music (tonal pads), Rain (atonal noise) or Both, remembered in Settings (owner, 2026-10-07).
  // Both plays the two at once, each at its own level from config.json, so the rain sits under
  // the music.
  function playMode(mode) {
    if (mode === "rain") return audio.rain();
    if (mode !== "both") return audio.pads();
    const mix = config.calm.bothMix;
    const parts = [audio.pads(mix.music), audio.rain(mix.rain)];
    return { stop() { parts.forEach((part) => part.stop()); } };
  }
  const current = { timers: [], music: playMode(getSetting("calmMode")), cover: null };
  run = current;
  container.querySelector(".calm-sound-note").hidden = ctx.soundsOn;

  const random = (min, max) => min + Math.random() * (max - min);

  function addShape() {
    if (run !== current) return;
    if (field.childElementCount < settings.maxShapes) {
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
      current.timers.push(setTimeout(() => group.remove(), settings.shapeLifeSeconds * 1000));
    }
    current.timers.push(setTimeout(addShape, settings.shapeEveryMs));
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
      blackButton.focus();
    };
    cover.addEventListener("click", restore);
    cover.addEventListener("keydown", (event) => { if (event.key === "Escape") restore(); });
    document.body.append(cover);
    current.cover = cover;
    cover.focus();
  }

  container.querySelectorAll("input[name=calm-mode]").forEach((input) => input.addEventListener("change", () => {
    setSetting("calmMode", input.value);
    current.music.stop();
    current.music = playMode(input.value);
  }));

  // Full screen (owner, 2026-10-07): the stage fills the screen. The browser's own full screen is
  // used where it exists; the CSS class does the work everywhere, including phones without it.
  const stage = container.querySelector(".calm-stage");
  const exit = container.querySelector(".calm-exit");
  const fullButton = container.querySelector(".full-screen");
  function leaveFull() {
    stage.classList.remove("full");
    exit.hidden = true;
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    fullButton.focus();
  }
  fullButton.addEventListener("click", () => {
    stage.classList.add("full");
    exit.hidden = false;
    stage.requestFullscreen?.().catch(() => {});
    exit.focus();
  });
  exit.addEventListener("click", leaveFull);
  stage.addEventListener("keydown", (event) => { if (event.key === "Escape") leaveFull(); });
  current.leaveFull = () => { if (stage.classList.contains("full")) leaveFull(); };

  blackButton.addEventListener("click", blackOut);
  addShape();
}

export function stop() {
  if (run) {
    run.timers.forEach(clearTimeout);
    run.music.stop();
    if (run.cover) run.cover.remove();
    if (run.leaveFull && document.fullscreenElement) document.exitFullscreen().catch(() => {});
  }
  run = null;
}
