// Standards and research (REQ-020, REQ-024, REQ-029). A standard is listed only when
// data/standards.json records a verified check; otherwise the page says plainly that none is
// claimed. Every technique shows how strong its evidence is, and its sources.

let run = null;

function escape(text) {
  return String(text).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
}

export async function start(container, ctx) {
  const { t } = ctx;
  const current = {};
  run = current;
  // A failed load rejects, and the shell falls back to the menu (AUD-008).
  const load = (url) => fetch(url).then((r) => {
    if (!r.ok) throw new Error(`${url}: HTTP ${r.status}`);
    return r.json();
  });
  const [standards, research] = await Promise.all([load("data/standards.json"), load("data/research.json")]);
  if (run !== current) return;

  // A standard is claimed only for the version it was checked on (AUD-023): an update clears the
  // claim until the new version is checked again.
  const forThisVersion = standards.verified.filter((s) => s.version === self.FREELIEF_VERSION);
  const verified = forThisVersion.length
    ? `<p>${t("standards.verifiedIntro")}</p>
       <ul class="standards-list">${forThisVersion.map((s) => `<li>${escape(t("standards.verifiedItem", {
         name: s.name, level: s.level, date: s.checked, tester: s.tester }))}</li>`).join("")}</ul>`
    : `<p class="standards-none">${t("standards.none")}</p>`;

  const techniques = research.techniques.map((technique) => `
    <section class="technique" data-technique="${escape(technique.id)}">
      <h3>${t(`standards.technique.${technique.id}`)}</h3>
      <p>${t(`standards.evidence.${technique.id}`)}</p>
      <p class="sources-label">${t("standards.sourcesLabel")}</p>
      <ul class="sources">
        ${technique.sources.map((id) => {
          const source = research.sources[id];
          return `<li><a class="text-link" href="${escape(source.url)}" rel="noopener">${escape(source.citation)}</a>
                  <span class="hint">(${escape(t("standards.checked", { date: source.checked }))})</span></li>`;
        }).join("")}
      </ul>
    </section>`).join("");

  container.innerHTML = `
    <section class="page standards">
      <h1>${t("standards.title")}</h1>
      <h2>${t("standards.standardsHeading")}</h2>
      ${verified}
      <p>${t("standards.help")} <a class="text-link" href="#feedback">${t("footer.feedback")}</a></p>
      <h2>${t("standards.researchHeading")}</h2>
      <p>${t("standards.researchIntro")}</p>
      ${techniques}
    </section>`;
}

export function stop() {
  run = null;
}
