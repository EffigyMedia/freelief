// Keep the screen on while breathing or the Visualizer runs (design review, owner 2026-10-08), so
// the phone does not dim or lock mid-breath. The Screen Wake Lock API; a browser without it, or one
// that refuses, simply lets the screen sleep. The lock drops when the page is hidden, so it is taken
// again when the page comes back.

let sentinel = null;
let wanted = 0;

async function acquire() {
  if (!wanted || sentinel || !("wakeLock" in navigator) || document.visibilityState !== "visible") return;
  try {
    sentinel = await navigator.wakeLock.request("screen");
    sentinel.addEventListener("release", () => { sentinel = null; });
  } catch {
    sentinel = null; // refused (battery saver, no gesture yet): not an error
  }
}

document.addEventListener("visibilitychange", acquire);

// Returns a function that lets the screen sleep again. Calls nest: the last release frees it.
export function keepAwake() {
  wanted += 1;
  acquire();
  let released = false;
  return () => {
    if (released) return;
    released = true;
    wanted = Math.max(0, wanted - 1);
    if (!wanted && sentinel) {
      sentinel.release().catch(() => {});
      sentinel = null;
    }
  };
}
