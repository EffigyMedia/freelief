// "More ways to calm": a short list of large links to every exercise and to Settings.

const ITEMS = [
  { route: "breathe", label: "nav.breathe", hint: "nav.breatheHint" },
  { route: "ground", label: "nav.ground", hint: "nav.groundHint" },
  { route: "statements", label: "nav.statements", hint: "nav.statementsHint" },
  { route: "bubbles", label: "nav.bubbles", hint: "nav.bubblesHint" },
  { route: "trace", label: "nav.trace", hint: "nav.traceHint" },
  { route: "sort", label: "nav.sort", hint: "nav.sortHint" },
  { route: "calm", label: "nav.calm", hint: "nav.calmHint" },
  { route: "settings", label: "nav.settings", hint: "nav.settingsHint" },
];

export function start(container, ctx) {
  const { t } = ctx;
  container.innerHTML = `
    <section class="menu">
      <h1>${t("nav.menuTitle")}</h1>
      <ul class="menu-list">
        ${ITEMS.map((item) => `
          <li>
            <a class="menu-item" href="#${item.route}">
              <span class="menu-label">${t(item.label)}</span>
              <span class="menu-hint">${t(item.hint)}</span>
            </a>
          </li>`).join("")}
      </ul>
    </section>`;
}

export function stop() {}
