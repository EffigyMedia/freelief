// About and disclaimer (REQ-006): the full self-help statement, privacy, and the open license.

// Every data value written into HTML is escaped, even committed config (AUD-033).
function escape(text) {
  return String(text).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
}

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
      <p><a class="text-link" href="${escape(config.project.sourceUrl)}" rel="noopener">${t("about.sourceLink")}</a></p>
      <h2>${t("about.madeByHeading")}</h2>
      <div class="maker">
        <svg class="maker-logo" viewBox="0 0 197 94" role="img" aria-label="${t("about.logoAlt")}">
          <rect width="95" height="26"/><rect y="34" width="95" height="26"/><rect y="68" width="95" height="26"/>
          <rect x="103" width="26" height="94"/><rect x="137" width="26" height="94"/><rect x="171" width="26" height="94"/>
        </svg>
        <p>${t("about.madeBy")}<br><span class="maker-name">${t("about.madeByName")}</span></p>
        <p><a class="button" href="${escape(config.project.makerUrl)}" rel="noopener">${t("about.website")}</a></p>
      </div>
      <p class="hint about-version">${t("about.version", { version: self.FREELIEF_VERSION })}</p>
    </section>`;
}

export function stop() {}
