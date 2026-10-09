// The offline cache (REQ-008). Its name carries the app version, so an update replaces it whole.
// It never fetches from another origin (REQ-015).
//
// The origin effigymedia.github.io is shared with other apps (AUD-001). Their workers may delete
// caches they do not own, and Freelief must never delete theirs (AUD-014). So this worker:
// - deletes only caches named "freelief-...";
// - repairs itself: on each online launch the page asks the worker to fetch any missing file ("heal"),
//   and every same-origin file it fetches from the network is stored on the way through.

importScripts("version.js");

const PREFIX = "freelief-";
const CACHE = `${PREFIX}${self.FREELIEF_VERSION}`;

// Every file the app needs offline. tools/tests/test_offline.py fails if a shipped file is missing.
const FILES = [
  "./",
  "index.html",
  "styles.css",
  "fallback.js",
  "version.js",
  "app.js",
  "strings.js",
  "crisis.js",
  "motion.js",
  "settings.js",
  "audio.js",
  "background.js",
  "haptics.js",
  "wakelock.js",
  "exercises/breathe.js",
  "activities/bubbles.js",
  "activities/trace.js",
  "activities/unblock.js",
  "activities/ripple.js",
  "activities/mandala.js",
  "activities/calm.js",
  "screens/menu.js",
  "screens/settings.js",
  "screens/about.js",
  "screens/standards.js",
  "screens/feedback.js",
  "config.json",
  "strings/en.json",
  "data/crisis-lines.json",
  "data/research.json",
  "data/standards.json",
  "manifest.webmanifest",
  "icons/icon.svg",
  "icons/icon-192.png",
  "icons/icon-512.png",
];

// Fill the cache from the network, past the browser's HTTP cache, so a new version never stores
// an old file (AUD-013).
function precache() {
  return caches.open(CACHE)
    .then((cache) => cache.addAll(FILES.map((file) => new Request(file, { cache: "reload" }))));
}

// A new version installs into its own cache and then waits. The page lets it take over when that
// is safe: on a fresh open, before the first touch, or when the person presses Update now. A
// version never changes under a page the person is using, so an old page never loads new files
// (AUD-057).
self.addEventListener("install", (event) => {
  event.waitUntil(precache());
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys
        .filter((key) => key.startsWith(PREFIX) && key !== CACHE)
        .map((key) => caches.delete(key))))
      .then(() => self.clients.claim()),
  );
});

// A page asks for a repair on each online launch. Any file missing from the cache is fetched
// again, so a cache that another app deleted, and that refilled only partly, becomes whole.
// The reply says whether it worked.
self.addEventListener("message", (event) => {
  if (event.data === "skip") {
    self.skipWaiting();
    return;
  }
  if (event.data !== "heal") return;
  const reply = (ok) => event.source && event.source.postMessage({ heal: ok });
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => Promise.all(FILES.map((file) => cache.match(file).then((hit) => (hit ? null : file))))
        .then((missing) => missing.filter(Boolean))
        .then((missing) => (missing.length
          ? cache.addAll(missing.map((file) => new Request(file, { cache: "reload" })))
          : null)))
      .then(() => reply(true), () => reply(false)),
  );
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (event.request.method !== "GET" || url.origin !== self.location.origin) return;
  // Answer only from THIS version's cache. caches.match() searches every cache, so while an old
  // version's cache still exists it can serve old files to a new version, or a mix of both, and
  // the app may not start (owner, 2026-10-07: "Can't load").
  event.respondWith(
    caches.open(CACHE).then((cache) => cache.match(event.request, { ignoreSearch: true })).then((cached) => {
      if (cached) return cached;
      return fetch(event.request).then((response) => {
        // Store what came from the network, so a cache that was deleted fills again with use.
        if (response.ok && response.type === "basic") {
          const copy = response.clone();
          event.waitUntil(caches.open(CACHE).then((cache) => cache.put(event.request, copy)));
        }
        return response;
      });
    }).catch(() => fetch(event.request)), // a Cache Storage fault falls back to the network (AUD-059)
  );
});
