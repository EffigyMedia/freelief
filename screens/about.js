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
      <h2>${t("about.madeByHeading")}</h2>
      <div class="maker">
        <img class="maker-logo" src="icons/effigy-media.png" width="200" height="120" alt="${t("about.logoAlt")}">
        <p>${t("about.madeBy")}</p>
        <p><a class="button" href="${config.project.makerUrl}" rel="noopener">${t("about.website")}</a></p>
      </div>
      <p class="hint about-version">${t("about.version", { version: self.FREELIEF_VERSION })}</p>
    </section>`;
}

export function stop() {}
