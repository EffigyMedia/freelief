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

  state = { timers: [], index: 0, paused: false };

  const scaleFor = (which) => (which === "max" ? breathing.guideMaxScale : breathing.guideMinScale);

  function clearTimers() {
    state.timers.forEach(clearTimeout);
    state.timers = [];
  }

  function runPhase() {
    const phase = phases[state.index];
    phaseLabel.textContent = t(`breathe.${phase.key}`);
    if (motion.reducedMotion()) {
      circle.style.transition = "none";
      circle.style.transform = "scale(0.8)";
    } else {
      circle.style.transition = `transform ${phase.seconds}s ease-in-out`;
      circle.style.transform = `scale(${scaleFor(phase.scale)})`;
    }
    for (let second = 0; second < phase.seconds; second++) {
      state.timers.push(setTimeout(() => { count.textContent = String(second + 1); }, second * 1000));
    }
    state.timers.push(setTimeout(() => {
      state.index = (state.index + 1) % phases.length;
      runPhase();
    }, phase.seconds * 1000));
  }

  function setPaused(paused) {
    state.paused = paused;
    pauseButton.textContent = t(paused ? "breathe.resume" : "breathe.pause");
    pauseButton.setAttribute("aria-pressed", String(paused));
    clearTimers();
    if (paused) {
      phaseLabel.textContent = t("breathe.paused");
      count.textContent = "";
      const current = getComputedStyle(circle).transform;
      circle.style.transition = "none";
      circle.style.transform = current === "none" ? "" : current;
    } else {
      runPhase();
    }
  }

  pauseButton.addEventListener("click", () => setPaused(!state.paused));

  // Start from the out-breath scale, so the first in-breath grows the circle.
  circle.style.transition = "none";
  circle.style.transform = `scale(${breathing.guideMinScale})`;
  pauseButton.textContent = t("breathe.pause");
  pauseButton.setAttribute("aria-pressed", "false");
  requestAnimationFrame(() => requestAnimationFrame(runPhase));
}

export function stop() {
  if (state) {
    state.timers.forEach(clearTimeout);
    state = null;
  }
}
