// Keep the screen on while breathing or the Visualizer runs (design review, owner 2026-10-08), so
// the phone does not dim or lock mid-breath. The Screen Wake Lock API; a browser without it, or one
// that refuses, simply lets the screen sleep. The lock drops when the page is hidden, so it is taken
// again when the page comes back.
//
// The lock has an end (AUD-103, owner 2026-10-09): after a time with no touch or key, chosen in
// Settings (10, 30 or 60 minutes), the screen may sleep while the exercise goes on. A person who
// falls asleep on Breathe does not wake to a flat phone. The next touch or key keeps it on again.
// No countdown is shown; it is not a timer the person must beat (REQ-011).

import { getSetting } from "./settings.js";

let sentinel = null;
let pending = null;
let wanted = 0;
let idle = false;
let idleTimer = 0;

function dropSentinel() {
  if (!sentinel) return;
  sentinel.release().catch(() => {});
  sentinel = null;
}

async function acquire() {
  if (!wanted || idle || sentinel || pending || !("wakeLock" in navigator)
    || document.visibilityState !== "visible") return;
  pending = navigator.wakeLock.request("screen");
  try {
    const granted = await pending;
    // The lock may be granted after the screen no longer wants it, or after another request won.
    // Then it is released at once, so it cannot keep the screen on (AUD-081).
    if (!wanted || idle || sentinel) {
      granted.release().catch(() => {});
      return;
    }
    sentinel = granted;
    sentinel.addEventListener("release", () => { if (sentinel === granted) sentinel = null; });
  } catch {
    // Refused (battery saver, no gesture yet): not an error.
  } finally {
    pending = null;
  }
}

// Each touch or key starts the idle time again, and takes the lock back if idle had released it.
function active() {
  clearTimeout(idleTimer);
  if (!wanted) return;
  idle = false;
  idleTimer = setTimeout(() => {
    idle = true;
    dropSentinel();
  }, getSetting("awakeMinutes") * 60 * 1000);
  acquire();
}

document.addEventListener("visibilitychange", acquire);
window.addEventListener("pointerdown", active, true);
window.addEventListener("keydown", active, true);

// Returns a function that lets the screen sleep again. Calls nest: the last release frees it.
export function keepAwake() {
  wanted += 1;
  active();
  let released = false;
  return () => {
    if (released) return;
    released = true;
    wanted = Math.max(0, wanted - 1);
    if (!wanted) {
      clearTimeout(idleTimer);
      idle = false;
      dropSentinel();
    }
  };
}
