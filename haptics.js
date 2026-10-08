// Haptic feedback (REQ-034, owner 2026-10-07): one short vibration for a single triggered event in
// an activity, never for anything continuous. On by default; Settings turns it off. A device
// without the Vibration API (such as Safari on iPhone) gets nothing, and nothing fails.

import { getSetting } from "./settings.js";

let patterns = {};

export function initHaptics(config) {
  patterns = config.haptics.patterns;
}

export function pulse(name) {
  const pattern = patterns[name];
  if (!pattern || !getSetting("haptics") || typeof navigator.vibrate !== "function") return;
  try {
    navigator.vibrate(pattern);
  } catch {
    // A browser may refuse a vibration before the first touch; that is not an error.
  }
}
