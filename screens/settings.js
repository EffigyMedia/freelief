// Settings: breathing rhythm, colors, vibration, the region for urgent help, where Freelief opens,
// how long the screen stays on, Reset, and the offline copy and its update (REQ-023, REQ-007,
// REQ-021, REQ-005, REQ-037). Every change is saved at once through settings.js, the only module that
// touches storage.

import { getSetting, setSetting, resetSettings } from "../settings.js";
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
        <legend>${t("settings.openOn")}</legend>
        ${radios("openOn", config.settings.openOnChoices, getSetting("openOn"), "settings.openOn")}
      </fieldset>
      <fieldset aria-describedby="awake-hint">
        <legend>${t("settings.awake")}</legend>
        ${config.wakeLock.idleMinutesChoices.map((minutes) => `
        <label class="choice">
          <input type="radio" name="awakeMinutes" value="${minutes}" ${minutes === getSetting("awakeMinutes") ? "checked" : ""}>
          <span>${t(`settings.awake.${minutes}`)}</span>
        </label>`).join("")}
        <p id="awake-hint" class="hint small-hint">${t("settings.awakeHint")}</p>
      </fieldset>
      <fieldset>
        <legend>${t("settings.theme")}</legend>
        ${radios("theme", themes, getSetting("theme"), "settings.theme")}
      </fieldset>
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
      <div class="reset">
        <button type="button" class="button reset-settings" aria-describedby="reset-hint">${t("settings.reset")}</button>
        <p id="reset-hint" class="hint">${t("settings.resetHint")}</p>
        <div class="reset-confirm" hidden>
          <p id="reset-question">${t("settings.resetQuestion")}</p>
          <button type="button" class="button reset-yes" aria-describedby="reset-question">${t("settings.resetYes")}</button>
          <button type="button" class="button reset-no">${t("settings.resetNo")}</button>
        </div>
        <p class="reset-status" aria-live="polite"></p>
      </div>
      <div class="app-version">
        <p class="version-line">${t("settings.version", { version: self.FREELIEF_VERSION })}</p>
        <p class="offline-state"></p>
        <button type="button" class="button update-now" aria-describedby="update-hint">${t("settings.update")}</button>
        <p id="update-hint" class="hint">${t("settings.updateHint")}</p>
        <p class="update-status" aria-live="polite"></p>
      </div>
    </section>`;

  container.querySelectorAll("input[name=rhythm]").forEach((input) =>
    input.addEventListener("change", () => setSetting("rhythm", input.value)));
  container.querySelectorAll("input[name=openOn]").forEach((input) =>
    input.addEventListener("change", () => setSetting("openOn", input.value)));
  container.querySelectorAll("input[name=awakeMinutes]").forEach((input) =>
    input.addEventListener("change", () => setSetting("awakeMinutes", Number(input.value))));
  container.querySelectorAll("input[name=theme]").forEach((input) =>
    input.addEventListener("change", () => setSetting("theme", input.value)));
  container.querySelector("input[name=haptics]").addEventListener("change", (event) =>
    setSetting("haptics", event.target.checked));
  const region = container.querySelector("#help-region");
  // A saved region that is no longer curated shows as Automatic, which is what the dialog does.
  region.value = [...region.options].some((o) => o.value === getSetting("helpRegion")) ? getSetting("helpRegion") : "auto";
  region.addEventListener("change", () => setSetting("helpRegion", region.value));
  // Reset clears every choice, including the region for urgent help, so it asks once more. One
  // stray tap changes nothing (web-interface-review, 2026-10-09).
  const confirm = container.querySelector(".reset-confirm");
  container.querySelector(".reset-settings").addEventListener("click", () => {
    confirm.hidden = false;
    container.querySelector(".reset-no").focus();
  });
  container.querySelector(".reset-no").addEventListener("click", () => {
    confirm.hidden = true;
    container.querySelector(".reset-settings").focus();
  });
  container.querySelector(".reset-yes").addEventListener("click", () => {
    resetSettings();
    // Draw the screen again with the defaults. The status is set a moment after the new live region
    // exists, so a screen reader announces it.
    start(container, ctx);
    container.querySelector(".reset-settings").focus();
    setTimeout(() => { container.querySelector(".reset-status").textContent = t("settings.resetDone"); }, 100);
  });
  // Whether this version is saved for use with no network (AUD-112). The offline copy is written
  // all at once, so its cache exists only when every file is in it.
  const offline = container.querySelector(".offline-state");
  Promise.resolve(self.caches?.has(`freelief-${self.FREELIEF_VERSION}`))
    .catch(() => false)
    .then((ready) => { offline.textContent = t(ready ? "settings.offlineReady" : "settings.offlineNotReady"); });
  const status = container.querySelector(".update-status");
  const updateButton = container.querySelector(".update-now");
  updateButton.addEventListener("click", async () => {
    // One update at a time: repeated taps do not start parallel runs.
    if (updateButton.getAttribute("aria-disabled") === "true") return;
    updateButton.setAttribute("aria-disabled", "true");
    try {
      await updateNow(status, t);
    } finally {
      updateButton.removeAttribute("aria-disabled");
    }
  });
}

// "Update now" (owner, 2026-10-07): get the newest version and restart. Nothing is removed until
// the network is shown to work (AUD-056): registration.update() fetches the worker from the
// network and fails on a dead link or a captive portal, and then the current copy stays. A new
// version installs in its own cache and takes over; the same version is refreshed in full. Only
// Freelief's own caches are deleted; the origin is shared with other apps. Settings are kept.
async function updateNow(status, t) {
  if (!navigator.onLine) {
    status.textContent = t("settings.updateOffline");
    return;
  }
  status.textContent = t("settings.updating");
  const registration = await navigator.serviceWorker?.getRegistration().catch(() => null);
  if (!registration) {
    location.reload();
    return;
  }
  try {
    await registration.update();
  } catch {
    status.textContent = t("settings.updateFailed");
    return;
  }
  const incoming = registration.installing || registration.waiting;
  if (incoming) {
    // The new version waits after it installs (sw.js); the person asked for it, so it takes over.
    const settled = await new Promise((resolve) => {
      const check = () => {
        if (incoming.state === "installed") incoming.postMessage("skip");
        if (incoming.state === "activated") resolve(true);
        if (incoming.state === "redundant") resolve(false);
      };
      incoming.addEventListener("statechange", check);
      check();
    });
    if (settled) location.reload();
    else status.textContent = t("settings.updateFailed");
    return;
  }
  try {
    const keys = await caches.keys();
    await Promise.all(keys.filter((key) => key.startsWith("freelief-")).map((key) => caches.delete(key)));
    await registration.unregister();
  } finally {
    location.reload();
  }
}

export function stop() {}
