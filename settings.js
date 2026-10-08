// The single source of truth for Settings, and the only module that touches localStorage.
// Settings stay on the device (REQ-015). Every storage access is in try/catch, so blocked or
// broken storage never breaks a screen: the defaults from config.json stand (REQ-023).
//
// Only what the person changed is stored (AUD-062). A setting they never touched follows the
// default of the version they run, so a new default reaches them.

let key = "freelief.settings.v2";
let values = {};
let chosen = {};
let defaults = {};
const listeners = new Set();

function read(storageKey) {
  try {
    return JSON.parse(localStorage.getItem(storageKey) || "{}") || {};
  } catch {
    return {};
  }
}

// The checks a stored value must pass. Own keys only: a stored name such as "constructor" must not
// pass (audit, inherited names).
function validators(config) {
  return {
    rhythm: (v) => Object.hasOwn(config.breathing.rhythms, v),
    sounds: (v) => typeof v === "boolean",
    haptics: (v) => typeof v === "boolean",
    theme: (v) => config.theme.choices.includes(v),
    calmMode: (v) => config.calm.modes.includes(v),
    // "auto", or a two-letter region code. crisis.js shows the general route for a region it does
    // not have, so a code that is no longer curated is safe.
    helpRegion: (v) => v === "auto" || /^[A-Z]{2}$/.test(v),
    openOn: (v) => config.settings.openOnChoices.includes(v),
  };
}

// The v1 store saved every value, chosen or not. Only a value that differs from today's default
// can have been a choice, so only those carry over. A stored "box" rhythm is dropped: box was the
// default from 2026-10-07 to 2026-10-08, so it was most likely never chosen.
function migrate(config, valid) {
  const old = read(config.settings.legacyStorageKey);
  const carried = {};
  for (const [name, check] of Object.entries(valid)) {
    const value = old[name];
    if (!check(value) || value === defaults[name]) continue;
    if (name === "rhythm" && value === "box") continue;
    carried[name] = value;
  }
  try {
    localStorage.removeItem(config.settings.legacyStorageKey);
    if (Object.keys(carried).length) localStorage.setItem(key, JSON.stringify(carried));
  } catch {
    // Storage is blocked: nothing to move.
  }
  return carried;
}

export function initSettings(config) {
  key = config.settings.storageKey;
  defaults = {
    rhythm: config.breathing.defaultRhythm,
    sounds: config.sounds.enabledByDefault,
    theme: config.theme.default,
    calmMode: config.calm.defaultMode,
    helpRegion: config.crisis.defaultRegion,
    haptics: config.haptics.enabledByDefault,
    openOn: config.settings.openOnDefault,
  };
  const valid = validators(config);
  let hasV2 = false;
  try {
    hasV2 = localStorage.getItem(key) !== null;
  } catch {
    hasV2 = false;
  }
  const stored = hasV2 ? read(key) : migrate(config, valid);
  chosen = {};
  for (const [name, check] of Object.entries(valid)) {
    if (Object.hasOwn(stored, name) && check(stored[name])) chosen[name] = stored[name];
  }
  values = { ...defaults, ...chosen };
}

export function getSetting(name) {
  return values[name];
}

export function setSetting(name, value) {
  values[name] = value;
  chosen[name] = value;
  try {
    localStorage.setItem(key, JSON.stringify(chosen));
  } catch {
    // Storage is blocked or full: the choice holds for this visit only.
  }
  listeners.forEach((listener) => listener(name, value));
}

export function onSettingChange(listener) {
  listeners.add(listener);
}
