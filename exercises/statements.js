// Calming statements (REQ-003), one at a time, advanced at the person's own pace. The list wraps
// around, so there is no end to reach and nothing to finish.

let cleanup = null;

export function start(container, ctx) {
  stop();
  const { t, list } = ctx;
  const statements = list("statements.list");
  let index = 0;

  container.innerHTML = `
    <section class="exercise statements">
      <h1>${t("statements.title")}</h1>
      <p class="step-count" aria-hidden="true"></p>
      <p class="prompt statement" aria-live="polite"></p>
      <div class="exercise-actions">
        <button type="button" class="button previous">${t("statements.previous")}</button>
        <button type="button" class="button primary next">${t("statements.next")}</button>
      </div>
    </section>`;

  const count = container.querySelector(".step-count");
  const text = container.querySelector(".statement");

  function render() {
    count.textContent = t("statements.position", { index: index + 1, total: statements.length });
    text.textContent = statements[index];
  }

  container.querySelector(".previous").addEventListener("click", () => {
    index = (index - 1 + statements.length) % statements.length;
    render();
  });
  container.querySelector(".next").addEventListener("click", () => {
    index = (index + 1) % statements.length;
    render();
  });

  render();
  cleanup = () => {};
}

export function stop() {
  if (cleanup) cleanup();
  cleanup = null;
}
