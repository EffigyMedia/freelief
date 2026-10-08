// Settings: breathing rhythm, colors, sounds and the region for urgent help (REQ-023, REQ-007,
// REQ-021, REQ-005). Every change is saved at once through settings.js, the only module that
// touches storage.

import { getSetting, setSetting } from "../settings.js";
import { unlockAudio } from "../audio.js";
import { regionList } from "../crisis.js";

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
          <input type="checkbox" name="sounds" ${getSetting("sounds") ? "checked" : ""}
                 aria-describedby="sounds-hint">
          <span>${t("settings.sounds")}</span>
        </label>
        <p id="sounds-hint" class="hint">${t("settings.soundsHint")}</p>
      </div>
      <div class="toggle">
        <label class="choice">
          <input type="checkbox" name="haptics" ${getSetting("haptics") ? "checked" : ""}
                 aria-describedby="haptics-hint">
          <span>${t("settings.haptics")}</span>
        </label>
        <p id="haptics-hint" class="hint small-hint">${t("settings.hapticsHint")}</p>
      </div>
      <div class="region-setting">
        <label class="field-label" for="help-region">${t("settings.region")}</label>
        <select id="help-region" class="country-select" aria-describedby="region-hint">
          <option value="auto">${t("settings.region.auto")}</option>
          ${regionList().map((region) => `<option value="${region.code}">${region.country}</option>`).join("")}
        </select>
        <p id="region-hint" class="hint">${t("settings.regionHint")}</p>
      </div>
      <p class="hint">${t("settings.saved")}</p>
      <div class="app-version">
        <p class="version-line">${t("settings.version", { version: self.FREELIEF_VERSION })}</p>
        <button type="button" class="button update-now" aria-describedby="update-hint">${t("settings.update")}</button>
        <p id="update-hint" class="hint">${t("settings.updateHint")}</p>
        <p class="update-status" aria-live="polite"></p>
      </div>
    </section>`;

  container.querySelectorAll("input[name=rhythm]").forEach((input) =>
    input.addEventListener("change", () => setSetting("rhythm", input.value)));
  container.querySelectorAll("input[name=theme]").forEach((input) =>
    input.addEventListener("change", () => setSetting("theme", input.value)));
  container.querySelector("input[name=haptics]").addEventListener("change", (event) =>
    setSetting("haptics", event.target.checked));
  const region = container.querySelector("#help-region");
  // A saved region that is no longer curated shows as Automatic, which is what the dialog does.
  region.value = [...region.options].some((o) => o.value === getSetting("helpRegion")) ? getSetting("helpRegion") : "auto";
  region.addEventListener("change", () => setSetting("helpRegion", region.value));
  const status = container.querySelector(".update-status");
  container.querySelector(".update-now").addEventListener("click", () => updateNow(status, t));
  container.querySelector("input[name=sounds]").addEventListener("change", (event) => {
    if (event.target.checked) unlockAudio();
    setSetting("sounds", event.target.checked);
  });
}

// "Update now" (owner, 2026-10-07): drop Freelief's offline copy and its worker, then reload from
// the internet, so the newest version loads at once. Settings live in localStorage and are kept.
// Only Freelief's own caches are deleted; the origin is shared with other apps.
async function updateNow(status, t) {
  if (!navigator.onLine) {
    status.textContent = t("settings.updateOffline");
    return;
  }
  status.textContent = t("settings.updating");
  try {
    const keys = await caches.keys();
    await Promise.all(keys.filter((key) => key.startsWith("freelief-")).map((key) => caches.delete(key)));
    const registration = await navigator.serviceWorker?.getRegistration();
    if (registration) await registration.unregister();
  } finally {
    location.reload();
  }
}

export function stop() {}
