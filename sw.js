// The offline cache (REQ-008). Its name carries the app version, so an update replaces it whole.
// It never fetches from another origin (REQ-015).

importScripts("version.js");

const CACHE = `freelief-${self.FREELIEF_VERSION}`;

// Every file the app needs offline. tools/tests/test_offline.py fails if a shipped file is missing.
const FILES = [
  "./",
  "index.html",
  "styles.css",
  "version.js",
  "app.js",
  "strings.js",
  "crisis.js",
  "motion.js",
  "settings.js",
  "audio.js",
  "exercises/breathe.js",
  "exercises/ground.js",
  "exercises/statements.js",
  "activities/bubbles.js",
  "activities/trace.js",
  "activities/sort.js",
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

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (event.request.method !== "GET" || url.origin !== self.location.origin) return;
  event.respondWith(
    caches.match(event.request, { ignoreSearch: true })
      .then((cached) => cached || fetch(event.request)),
  );
});
