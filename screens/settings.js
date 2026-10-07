// Settings: breathing rhythm, soft tones and colours (REQ-023, REQ-007, REQ-021). Every change is
// saved at once through settings.js, the only module that touches storage.

import { getSetting, setSetting } from "../settings.js";
import { unlockAudio } from "../audio.js";

export function start(container, ctx) {
  const { t, config } = ctx;
  const rhythms = config.breathing.rhythmOrder;
  const themes = config.theme.choices;

  const radios = (name, choices, current, labelPrefix) => choices.map((choice) => `
    <label class="choice">
      <input type="radio" name="${name}" value="${choice}" ${choice === current ? "checked" : ""}>
      <span>${t(`${labelPrefix}.${choice}`)}</span>
    </label>`).join("");

  container.innerHTML = `
    <section class="settings">
      <h1>${t("settings.title")}</h1>
      <fieldset>
        <legend>${t("settings.rhythm")}</legend>
        ${radios("rhythm", rhythms, getSetting("rhythm"), "settings.rhythm")}
      </fieldset>
      <fieldset>
        <legend>${t("settings.theme")}</legend>
        ${radios("theme", themes, getSetting("theme"), "settings.theme")}
      </fieldset>
      <div class="toggle">
        <label class="choice">
          <input type="checkbox" name="tones" ${getSetting("tones") ? "checked" : ""}
                 aria-describedby="tones-hint">
          <span>${t("settings.tones")}</span>
        </label>
        <p id="tones-hint" class="hint">${t("settings.tonesHint")}</p>
      </div>
      <p class="hint">${t("settings.saved")}</p>
    </section>`;

  container.querySelectorAll("input[name=rhythm]").forEach((input) =>
    input.addEventListener("change", () => setSetting("rhythm", input.value)));
  container.querySelectorAll("input[name=theme]").forEach((input) =>
    input.addEventListener("change", () => setSetting("theme", input.value)));
  container.querySelector("input[name=tones]").addEventListener("change", (event) => {
    if (event.target.checked) unlockAudio();
    setSetting("tones", event.target.checked);
  });
}

export function stop() {}
