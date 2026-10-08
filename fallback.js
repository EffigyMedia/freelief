// The static fallback in index.html (AUD-002) must show when the app cannot start, but painting it
// on every launch delayed the breathing guide by about 90 ms (RLG-006). This classic script runs
// in <head>, before the body is drawn: it hides the fallback, and shows it again if the app has not
// started within REVEAL_AFTER_MS. With JavaScript off this script never runs, so the fallback shows.
//
// REVEAL_AFTER_MS is a constant here, not a config.json tunable, on purpose: this script must work
// when config.json cannot load, and the app's own start-up is far below it (about 0.2 s).

const REVEAL_AFTER_MS = 2000;

document.documentElement.classList.add("hide-fallback");
setTimeout(() => {
  if (document.documentElement.dataset.ready !== "true") {
    document.documentElement.classList.remove("hide-fallback");
  }
}, REVEAL_AFTER_MS);
