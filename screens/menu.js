// The menu, Freelief's first screen (owner, 2026-10-07): large links to every exercise and activity.
// Settings is the gear at the top right, not on this list.

// The order is the owner's (2026-10-10, RLG-058). Trace a shape holds Zen Garden's place until Zen
// Garden replaces it (RLG-055).
const ITEMS = [
  { route: "breathe", label: "nav.breathe", hint: "nav.breatheHint" },
  { route: "bubbles", label: "nav.bubbles", hint: "nav.bubblesHint" },
  { route: "trace", label: "nav.trace", hint: "nav.traceHint" },
  { route: "ripple", label: "nav.ripple", hint: "nav.rippleHint" },
  { route: "mandala", label: "nav.mandala", hint: "nav.mandalaHint" },
  { route: "unblock", label: "nav.unblock", hint: "nav.unblockHint" },
  { route: "calm", label: "nav.calm", hint: "nav.calmHint" },
];

export function start(container, ctx) {
  const { t } = ctx;
  container.innerHTML = `
    <section class="menu">
      <h1>${t("nav.menuTitle")}</h1>
      <ul class="menu-list">
        ${ITEMS.map((item) => `
          <li>
            <a class="menu-item${item.route === "breathe" ? " menu-item-first" : ""}" href="#${item.route}">
              <span class="menu-label">${t(item.label)}</span>
              <span class="menu-hint">${t(item.hint)}</span>
            </a>
          </li>`).join("")}
      </ul>
    </section>`;
}

export function stop() {}
