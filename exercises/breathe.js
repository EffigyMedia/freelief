// Paced breathing (REQ-001). The guide grows on the in-breath and shrinks on the out-breath.
// Under reduced motion it stays still and the count carries the rhythm (REQ-010).
// The person can pause at any time; nothing waits for them to act (REQ-011).

const PHASES = [
  { key: "in", scale: "max" },
  { key: "holdIn", scale: "max" },
  { key: "out", scale: "min" },
  { key: "holdOut", scale: "min" },
];

let state = null;

export function start(container, ctx) {
  stop();
  const { t, config, motion } = ctx;
  const breathing = config.breathing;
  const rhythm = breathing.rhythms[ctx.rhythm] || breathing.rhythms[breathing.defaultRhythm];
  const phases = PHASES.filter((phase) => rhythm[phase.key] > 0)
    .map((phase) => ({ ...phase, seconds: rhythm[phase.key] }));

  container.innerHTML = `
    <section class="breathe">
      <h1 class="visually-hidden">${t("breathe.title")}</h1>
      <div class="guide" role="img" aria-label="${t("breathe.guideLabel")}">
        <div class="guide-circle"></div>
        <div class="guide-count" aria-hidden="true"></div>
      </div>
      <p class="phase" aria-live="polite"></p>
      <button type="button" class="button pause"></button>
    </section>`;

  const circle = container.querySelector(".guide-circle");
  const count = container.querySelector(".guide-count");
  const phaseLabel = container.querySelector(".phase");
  const pauseButton = container.querySelector(".pause");

  // This run's own state. A pending frame or timer from a stopped run checks it and does nothing.
  const run = { timers: [], index: 0, paused: false, frame: 0, stopTone: () => {} };
  state = run;

  const scaleFor = (which) => (which === "max" ? breathing.guideMaxScale : breathing.guideMinScale);

  function clearTimers() {
    run.timers.forEach(clearTimeout);
    run.timers = [];
  }

  function runPhase() {
    if (state !== run || run.paused) return;
    const phase = phases[run.index];
    phaseLabel.textContent = t(`breathe.${phase.key}`);
    run.stopTone();
    run.stopTone = ctx.audio.cue(phase.key, phase.seconds);
    if (motion.reducedMotion()) {
      circle.style.transition = "none";
      circle.style.transform = "scale(0.8)";
    } else {
      circle.style.transition = `transform ${phase.seconds}s ease-in-out`;
      circle.style.transform = `scale(${scaleFor(phase.scale)})`;
    }
    for (let second = 0; second < phase.seconds; second++) {
      run.timers.push(setTimeout(() => { count.textContent = String(second + 1); }, second * 1000));
    }
    run.timers.push(setTimeout(() => {
      run.index = (run.index + 1) % phases.length;
      runPhase();
    }, phase.seconds * 1000));
  }

  function setPaused(paused) {
    run.paused = paused;
    pauseButton.textContent = t(paused ? "breathe.resume" : "breathe.pause");
    pauseButton.setAttribute("aria-pressed", String(paused));
    clearTimers();
    if (paused) {
      run.stopTone();
      phaseLabel.textContent = t("breathe.paused");
      count.textContent = "";
      const current = getComputedStyle(circle).transform;
      circle.style.transition = "none";
      circle.style.transform = current === "none" ? "" : current;
    } else {
      runPhase();
    }
  }

  pauseButton.addEventListener("click", () => setPaused(!run.paused));

  // Start from the out-breath scale, so the first in-breath grows the circle.
  circle.style.transition = "none";
  circle.style.transform = `scale(${breathing.guideMinScale})`;
  pauseButton.textContent = t("breathe.pause");
  pauseButton.setAttribute("aria-pressed", "false");
  run.frame = requestAnimationFrame(() => { run.frame = requestAnimationFrame(runPhase); });
}

export function stop() {
  if (state) {
    state.timers.forEach(clearTimeout);
    cancelAnimationFrame(state.frame);
    state.stopTone();
    state = null;
  }
}
