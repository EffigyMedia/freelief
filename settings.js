// The single source of truth for Settings, and the only module that touches localStorage.
// Settings stay on the device (REQ-015). Every storage access is in try/catch, so blocked or
// broken storage never breaks a screen: the defaults from config.json stand (REQ-023).

let key = "freelief.settings.v1";
let values = {};
let defaults = {};
const listeners = new Set();

export function initSettings(config) {
  key = config.settings.storageKey;
  defaults = {
    rhythm: config.breathing.defaultRhythm,
    sounds: config.sounds.enabledByDefault,
    theme: config.theme.default,
    calmMode: config.calm.defaultMode,
    helpRegion: config.crisis.defaultRegion,
    haptics: config.haptics.enabledByDefault,
  };
  let stored = {};
  try {
    stored = JSON.parse(localStorage.getItem(key) || "{}") || {};
  } catch {
    stored = {};
  }
  values = { ...defaults };
  // Own keys only: a stored name such as "constructor" must not pass (audit, inherited names).
  if (Object.hasOwn(config.breathing.rhythms, stored.rhythm)) values.rhythm = stored.rhythm;
  // Sounds are a new key (2026-10-07): an old stored `tones: false` was never a choice, because
  // tones were off by default, so it does not carry over.
  if (typeof stored.sounds === "boolean") values.sounds = stored.sounds;
  if (typeof stored.haptics === "boolean") values.haptics = stored.haptics;
  if (config.theme.choices.includes(stored.theme)) values.theme = stored.theme;
  if (config.calm.modes.includes(stored.calmMode)) values.calmMode = stored.calmMode;
  // "auto", or a two-letter region code. crisis.js shows the general route for a region it does
  // not have, so a code that is no longer curated is safe.
  if (stored.helpRegion === "auto" || /^[A-Z]{2}$/.test(stored.helpRegion)) values.helpRegion = stored.helpRegion;
}

export function getSetting(name) {
  return values[name];
}

export function setSetting(name, value) {
  values[name] = value;
  try {
    localStorage.setItem(key, JSON.stringify(values));
  } catch {
    // Storage is blocked or full: the choice holds for this visit only.
  }
  listeners.forEach((listener) => listener(name, value));
}

export function onSettingChange(listener) {
  listeners.add(listener);
}
