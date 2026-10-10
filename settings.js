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
    // "auto", or a two-letter region code. crisis.js shows the general route for a region it does
    // not have, so a code that is no longer curated is safe.
    helpRegion: (v) => v === "auto" || /^[A-Z]{2}$/.test(v),
    openOn: (v) => config.settings.openOnChoices.includes(v),
    awakeMinutes: (v) => config.wakeLock.idleMinutesChoices.includes(v),
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
    helpRegion: config.crisis.defaultRegion,
    haptics: config.haptics.enabledByDefault,
    openOn: config.settings.openOnDefault,
    awakeMinutes: config.wakeLock.idleMinutesDefault,
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

function save() {
  try {
    localStorage.setItem(key, JSON.stringify(chosen));
  } catch {
    // Storage is blocked or full: the choice holds for this visit only.
  }
}

// A choice of the default value is not stored, so it follows a new default later (AUD-110).
export function setSetting(name, value) {
  values[name] = value;
  if (value === defaults[name]) delete chosen[name];
  else chosen[name] = value;
  save();
  listeners.forEach((listener) => listener(name, value));
}

// Every setting back to its default (AUD-110). Each listener hears each setting that changed. Sound
// on or off is the header's speaker, not a setting on the Settings screen, so a reset leaves it as
// it is: a reset must never make Freelief start to play (AUD-114).
const KEPT_BY_RESET = ["sounds"];

export function resetSettings() {
  const kept = Object.fromEntries(KEPT_BY_RESET.filter((name) => Object.hasOwn(chosen, name))
    .map((name) => [name, chosen[name]]));
  const changed = Object.keys(chosen).filter((name) => !Object.hasOwn(kept, name) && chosen[name] !== defaults[name]);
  chosen = kept;
  values = { ...defaults, ...kept };
  save();
  changed.forEach((name) => listeners.forEach((listener) => listener(name, values[name])));
}

export function onSettingChange(listener) {
  listeners.add(listener);
}
