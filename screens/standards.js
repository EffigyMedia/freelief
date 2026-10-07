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
  const [standards, research] = await Promise.all([
    fetch("data/standards.json").then((r) => r.json()),
    fetch("data/research.json").then((r) => r.json()),
  ]);
  if (run !== current) return;

  const verified = standards.verified.length
    ? `<p>${t("standards.verifiedIntro")}</p>
       <ul class="standards-list">${standards.verified.map((s) => `<li>${escape(t("standards.verifiedItem", {
         name: s.name, level: s.level, date: s.checked, tester: s.tester }))}</li>`).join("")}</ul>`
    : `<p class="standards-none">${t("standards.none")}</p>`;

  const techniques = research.techniques.map((technique) => `
    <section class="technique" data-technique="${technique.id}">
      <h3>${t(`standards.technique.${technique.id}`)}</h3>
      <p>${t(`standards.evidence.${technique.id}`)}</p>
      <p class="sources-label">${t("standards.sourcesLabel")}</p>
      <ul class="sources">
        ${technique.sources.map((id) => {
          const source = research.sources[id];
          return `<li><a class="text-link" href="${escape(source.url)}" rel="noopener">${escape(source.citation)}</a>
                  <span class="hint">(${t("standards.checked", { date: source.checked })})</span></li>`;
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
