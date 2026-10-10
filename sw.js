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
  "activities/garden.js",
  "activities/unblock.js",
  "activities/ripple.js",
  "activities/mandala.js",
  "activities/calm.js",
  "screens/menu.js",
  "screens/settings.js",
  "screens/about.js",
  "screens/feedback.js",
  "config.json",
  "strings/en.json",
  "data/crisis-lines.json",
  "manifest.webmanifest",
  "icons/icon.svg",
  "icons/icon-192.png",
  "icons/icon-512.png",
];

// Orders "0.8.9" before "0.8.10": numbers, part by part.
function compareVersions(a, b) {
  const x = a.split(".").map(Number);
  const y = b.split(".").map(Number);
  for (let i = 0; i < Math.max(x.length, y.length); i++) {
    const d = (x[i] || 0) - (y[i] || 0);
    if (d) return d;
  }
  return 0;
}

// Fill the cache from the network, past the browser's HTTP cache, so a new version never stores
// an old file (AUD-013).
function precache() {
  return caches.open(CACHE)
    .then((cache) => cache.addAll(FILES.map((file) => new Request(file, { cache: "reload" }))));
}

// A new version installs into its own cache and then waits. The page lets it take over when that
// is safe: on a fresh open, before the first touch, or when the person presses Update now. A
// version never changes under a page the person is using, so an old page never loads new files
// (AUD-057). A page knows only its own state, so the worker takes over only when the page that asks
// is Freelief's only open window: a second window, such as the installed app beside a browser tab,
// may be in use, and the new version then waits until every window is closed.
self.addEventListener("install", (event) => {
  event.waitUntil(precache());
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      // One other version's cache is kept until the next update: a page that version opened may
      // still be in use, and it asks for its screens by its version (AUD-057). It is the highest
      // other version: the one this update replaces, or, after a rollback, the one rolled back from.
      .then((keys) => {
        const others = keys.filter((key) => key.startsWith(PREFIX) && key !== CACHE)
          .sort((a, b) => compareVersions(a.slice(PREFIX.length), b.slice(PREFIX.length)));
        return Promise.all(others.slice(0, -1).map((key) => caches.delete(key)));
      })
      .then(() => self.clients.claim()),
  );
});

// The network may already serve a newer version. A file is stored in this version's cache only
// while the network still serves this version, so one cache never holds two versions (AUD-120).
function thisVersionIsDeployed() {
  return fetch(new Request("version.js", { cache: "reload" }))
    .then((response) => (response.ok ? response.text() : ""))
    .then((text) => text.includes(`"${self.FREELIEF_VERSION}"`))
    .catch(() => false);
}

// A page asks for a repair on each online launch. Any file missing from the cache is fetched
// again, so a cache that another app deleted, and that refilled only partly, becomes whole.
// The reply says whether it worked.
self.addEventListener("message", (event) => {
  if (event.data === "skip") {
    event.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then((windows) => {
      const alone = windows.every((client) => client.id === event.source?.id);
      if (alone) return self.skipWaiting();
      event.source?.postMessage({ skip: false });
      return undefined;
    }));
    return;
  }
  // Update now, when the version is already current: fetch every file again into a separate cache,
  // and copy it over this version's cache only when all of them arrived. One failed file leaves the
  // working copy as it was (AUD-133). The temporary name does not start with PREFIX, so no cleanup
  // reads it as a version.
  if (event.data === "refresh") {
    const temporary = `freelief~refresh-${self.FREELIEF_VERSION}`;
    event.waitUntil(caches.delete(temporary)
      .then(() => caches.open(temporary))
      .then((fresh) => fresh.addAll(FILES.map((file) => new Request(file, { cache: "reload" })))
        .then(() => Promise.all([fresh.keys(), caches.open(CACHE)]))
        .then(([requests, cache]) => Promise.all(requests.map((request) => fresh.match(request)
          .then((response) => cache.put(request, response))))))
      .then(() => true, () => false)
      .then((ok) => caches.delete(temporary).then(() => event.source?.postMessage({ refresh: ok }))));
    return;
  }
  if (event.data !== "heal") return;
  const reply = (ok) => event.source && event.source.postMessage({ heal: ok });
  event.waitUntil(
    thisVersionIsDeployed()
      .then((same) => (same ? caches.open(CACHE) : null))
      // A newer version is deployed: its own worker repairs its own cache, so nothing is stored.
      .then((cache) => cache && Promise.all(FILES.map((file) => cache.match(file).then((hit) => (hit ? null : file))))
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
  // Answer from ONE version's cache, never from all of them. caches.match() searches every cache, so
  // while an old version's cache still exists it can serve old files to a new version, or a mix of
  // both, and the app may not start (owner, 2026-10-07: "Can't load").
  // A lazy screen names the version of the page that asks for it (?v=). It is answered from that
  // version's cache while the cache exists, so a page keeps its own version's files (AUD-057).
  const asked = url.searchParams.get("v");
  const own = asked && asked !== self.FREELIEF_VERSION ? `${PREFIX}${asked}` : CACHE;
  event.respondWith(
    caches.has(own).then((kept) => caches.open(kept ? own : CACHE))
      .then((cache) => cache.match(event.request, { ignoreSearch: true })).then((cached) => {
      if (cached) return cached;
      return fetch(event.request).then((response) => {
        // Store what came from the network, so a cache that was deleted fills again with use.
        if (response.ok && response.type === "basic") {
          const copy = response.clone();
          event.waitUntil(thisVersionIsDeployed()
            .then((same) => same && caches.open(CACHE).then((cache) => cache.put(event.request, copy))));
        }
        return response;
      });
    }).catch(() => fetch(event.request)), // a Cache Storage fault falls back to the network (AUD-059)
  );
});
