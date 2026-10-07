// About and disclaimer (REQ-006): the full self-help statement, privacy, and the open license.

export function start(container, ctx) {
  const { t, config } = ctx;
  const paragraph = (key) => `<p>${t(key)}</p>`;
  container.innerHTML = `
    <section class="page about">
      <h1>${t("about.title")}</h1>
      <h2>${t("about.selfHelpHeading")}</h2>
      ${paragraph("about.selfHelp1")}
      ${paragraph("about.selfHelp2")}
      ${paragraph("about.selfHelp3")}
      <h2>${t("about.privacyHeading")}</h2>
      ${paragraph("about.privacy1")}
      ${paragraph("about.privacy2")}
      <h2>${t("about.openHeading")}</h2>
      ${paragraph("about.open1")}
      <p><a class="text-link" href="${config.project.sourceUrl}" rel="noopener">${t("about.sourceLink")}</a></p>
      <p class="hint">${t("about.version", { version: self.FREELIEF_VERSION })}</p>
    </section>`;
}

export function stop() {}
