// 5-4-3-2-1 grounding (REQ-002). Five prompts, one sense at a time, advanced at the person's own
// pace. Nothing is typed or stored. Focus stays on the control the person used; the prompt is a
// polite live region, so a screen reader reads each new step.

let cleanup = null;

export function start(container, ctx) {
  stop();
  const { t } = ctx;
  const steps = [5, 4, 3, 2, 1];
  let index = 0;

  container.innerHTML = `
    <section class="exercise ground">
      <h1>${t("ground.title")}</h1>
      <p class="exercise-intro">${t("ground.intro")}</p>
      <p class="step-count" aria-hidden="true"></p>
      <p class="prompt" aria-live="polite"></p>
      <div class="exercise-actions">
        <button type="button" class="button previous">${t("ground.previous")}</button>
        <button type="button" class="button primary next">${t("ground.next")}</button>
      </div>
    </section>`;

  const count = container.querySelector(".step-count");
  const prompt = container.querySelector(".prompt");
  const previous = container.querySelector(".previous");
  const next = container.querySelector(".next");

  function render() {
    const done = index === steps.length;
    count.textContent = done ? "" : t("ground.step", { count: index + 1 });
    prompt.textContent = done ? t("ground.done") : t(`ground.${steps[index]}`);
    previous.hidden = index === 0;
    next.textContent = done ? t("ground.again") : t("ground.next");
  }

  previous.addEventListener("click", () => {
    index = Math.max(0, index - 1);
    render();
    if (previous.hidden) next.focus();
  });
  next.addEventListener("click", () => {
    index = index === steps.length ? 0 : index + 1;
    ctx.audio.play("step");
    render();
  });

  render();
  cleanup = () => {};
}

export function stop() {
  if (cleanup) cleanup();
  cleanup = null;
}
