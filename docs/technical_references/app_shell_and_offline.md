# App shell, urgent help and offline

The owning document for the shell (`app.js`, `index.html`, `fallback.js`), the urgent-help dialog
(`crisis.js`, `data/crisis-lines.json`), the breathing exercise (`exercises/breathe.js`) and the
offline layer (`sw.js`, `manifest.webmanifest`, `version.js`). The router, the other screens,
Settings and every sound are in `exercises_and_settings.md`. Design: `docs/Design_Document.md`
flows F1 and F6, section 8, and the Decision Log.

## Boot
`index.html` loads `fallback.js` and `version.js` as classic scripts, and `app.js` as a module.

`fallback.js` adds `html.hide-fallback` before the body is drawn, so a normal start does not paint
the static fallback. If `html[data-ready]` is not `"true"` after 2 s, it removes the class and the
fallback shows. The 2 s is a constant in the file, not in `config.json`, because the script must
work when `config.json` cannot load. With JavaScript off, the script does not run and the fallback
shows.

`app.js` imports the menu (`screens/menu.js`) with the shell, because the menu is the first and
default screen (REQ-018). Every other screen is a dynamic `import()` in `ROUTES` and loads on its
first visit (RLG-006). `app.js` registers the service worker. Then it loads `config.json`,
`strings/en.json` and `data/crisis-lines.json` in parallel. It starts `settings.js`, `audio.js`,
`background.js` and `haptics.js`, applies the theme, builds the shell and shows the first screen.
Then it sets `html[data-ready="true"]` and the `freelief-ready` performance mark. Tests and `bench`
wait on those two signals.

If the boot fails, `app.js` logs the error, puts back the static fallback, sets
`html[data-ready="fallback"]` and removes `hide-fallback` at once. The fallback holds a breathing
line, the emergency instruction and the directory link (AUD-002). Its text is in `index.html`,
because it must show when `strings/en.json` cannot load.

## The header and the footer
The header is three centered rows (RLG-049): the name (plain text, not a link); then five round
buttons: the sound bar's music, rain and waves, the sound button and the Settings gear; then "Need
urgent help?" on its own line, as text. The Tab order follows what is seen, so "Need urgent help?"
is the sixth stop.

- **The sound button** turns all sound on or off from every screen. It is a toggle button with the
  fixed name "Sound" and `aria-pressed`. It sets the `sounds` setting. The fade, the sound bar
  and the background sound are in `exercises_and_settings.md`.
- **The gear** is a link to `#settings` with an accessible name. Its icon is inline SVG, so no
  file ships.

The footer holds the calm line, the self-help line, and the links to About, Standards and research,
and Feedback. On the exercise and activity screens (`QUIET_FOOTER`), the footer shows only its calm
line, so the activity has the room.

## Content Security Policy
A meta tag allows only `'self'` for every resource type, and no inline script or style. It limits
what Freelief's page loads and connects to, and it is the back-up for REQ-015. `'self'` is the
shared origin `effigymedia.github.io` (see Offline). Thus it does not keep out a script on a sibling
path, and it does not protect Cache Storage or `localStorage` from a sibling site (AUD-004). Two
consequences:
- JavaScript may set `element.style.x` (CSSOM is allowed), but never a `style` attribute string.
- Playwright's `wait_for_function` evaluates a string and is refused (no `unsafe-eval`). Tests use
  `harness.wait_until`, which polls with `page.evaluate`.

## Breathing exercise
Phases come from the active rhythm in `config.json` → `breathing.rhythms` (`in`, `holdIn`, `out`,
`holdOut` in seconds). A zero phase is skipped. A line under the guide shows the rhythm, such as
"In 4 · Out 6". Each phase does four things:
- It sets the phase label, an `aria-live="polite"` region, so a screen reader hears each phase.
- It starts a CSS transform transition of the phase's length.
- It updates a visible count each second. The count is hidden from screen readers to avoid noise.
- It starts the phase's tone with `audio.cue()` (see `exercises_and_settings.md`).

Under reduced motion the circle stays at `guideStillScale` and the count carries the rhythm. Pause
clears every timer, stops the tone and freezes the circle where it is. Resume starts the current
phase again. The screen asks `ctx.keepAwake()` for the wake lock at start and releases it in
`stop()`. Pause also releases it, and Resume takes it again (AUD-103).

## Urgent help
**The region.** `crisis.deviceRegion()` reads `navigator.languages`. It takes the region of the
first tag that names one, through `new Intl.Locale(tag).region`. It never guesses a region from a
bare language: `en` gives no region, not `US` (AUD-026). A wrong emergency number is worse than the
general route. No location is read. `crisis.activeRegion(setting)` returns the region saved in
Settings (`helpRegion`), or the device region when the setting is `"auto"`.

**The dialog** is a native `<dialog>` opened with `showModal()`. It traps focus and closes on
Escape. Order in the dialog:
1. A header with the title and a **Back** button. The header stays at the top while the content
   scrolls, so the way out is always in sight.
2. The intro.
3. A **Country** select with every curated region in alphabetical order, and "Another country".
   It opens on the active region. A choice in it holds for this visit only. The saved region is
   set in Settings.
4. The emergency line for the region, or "call your local emergency number" when the region is not
   curated or not known.
5. One Call button for each number in the region's emergency text, so "112 or 999" gives two
   buttons.
6. The region's own lines. Each line has its Call, Text and Chat buttons, its hours and its
   last-checked date. A line with web chat says that chat needs an internet connection (AUD-052).
7. The international directory link, which says that it needs an internet connection. With no
   crisis data, the link comes from `config.json` → `crisis.directoryUrl`.

Each open resets the dialog to the active region. While the dialog is open:
- No sound plays (AUD-074). Sound comes back when the dialog closes, if the sound setting is on.
- The page under it does not scroll (`html.help-is-open`).
- The phone's back gesture closes the dialog. The open adds a history entry, and `popstate` closes
  the dialog.

**Every line in `data/crisis-lines.json` carries `source` and `checked`.** Change a line only
after you check its source in the same session, and set `checked` to that date. `build --release`
fails when a line is older than `config.json` → `crisis.maxCheckAgeDays`.

## Silence when hidden
When the page is hidden (for example, during a call to a line), `app.js` silences all sound. When
the page shows again, sound comes back if the sound setting is on and the help dialog is closed.
While sound is held silent (off, help open, or hidden), `audio.js` makes no sound and never resumes
the audio, so a breathing tone cannot wake it in the background (AUD-082).

## Offline
`sw.js` imports `version.js` and names its cache `freelief-<version>`. Install pre-caches the
`FILES` list with `cache: "reload"`, past the browser's HTTP cache (AUD-013), and then **waits**. It
calls `skipWaiting` only when a page posts `"skip"` and that page is Freelief's only open window
(AUD-057). With another window open, it replies `{ skip: false }` and keeps waiting until every
window is closed, because the other window may be in use. Activate deletes only caches whose
name starts with `freelief-`, and it keeps the current one and the highest other version, so a page
that version opened can still load its screens (AUD-057). Then it claims the clients.

Fetch answers same-origin GET requests from **one version's cache only**. A lazy screen is asked for
as `file.js?v=<page version>`, and the worker answers it from that version's cache while the cache
exists, so a page keeps its own version's screens even after a new version takes over (AUD-057).
Every other request is answered from this version's cache (`caches.open(CACHE)`).
It never uses `caches.match()`, because that searches every cache and let an old version's files
reach a new one. On a miss, it fetches from the network and stores a good response in the cache,
but only while the network still serves this version: `thisVersionIsDeployed()` fetches
`version.js` past the HTTP cache and compares the version (AUD-120). If
the cache lookup itself fails, it falls back to the network (AUD-059). It ignores every other
request.

**The origin is shared.** `effigymedia.github.io` also serves other apps, so CacheStorage and
`localStorage` are shared too (AUD-001). Another app's worker may delete Freelief's cache. The owner
chose to stay on this origin with self-repair (2026-10-07). On each online launch, `app.js` posts
`"heal"` to the active worker. If the network still serves this version, the worker fetches any
`FILES` entry missing from the cache; if a newer version is deployed, it stores nothing and leaves
the repair to the new worker (AUD-120). It replies `{ heal }`. `app.js` logs a failed repair with `console.warn` (AUD-060). **Freelief must
never delete a cache it does not own.**

`test_offline.py` checks this layer:
- It fails when a shipped file is missing from `FILES`, or when a listed file does not exist.
- It deletes every cache, reloads online, reloads offline, and expects the app to work.
- It runs a real version update from a scratch copy. It checks that a foreign cache survives and
  that the old Freelief cache goes.

**Add every new shipped file to `FILES`**, and bump the version so that the cache is replaced.
`python tools/freelief.py files` is the file audit: it lists every shipped file and fails when the
offline copy and the shipped files disagree (AUD-108).

**Persistent storage (AUD-080).** After the start, `app.js` calls `navigator.storage.persist()`, so
a browser under storage pressure does not evict the offline copy. It skips Firefox, which would ask
the person a question, and the call never holds up the start. A failed worker registration is
logged with its reason (AUD-085).

A screen that cannot load, or that fails as it starts, falls back to the menu. The address changes
to `#menu`, so the failed screen's link works again later (AUD-057).

## Updates
**The update check and the download of Freelief's own files are the only requests after
install** (REQ-015, AUD-025, AUD-098). The repair above is the second kind. When an online person
opens the app, the browser requests `sw.js` and its import `version.js` from GitHub Pages. The
request carries nothing about the person, but GitHub can see the IP address and the time. The About
privacy text says so. Offline, no request is made.

The browser checks `sw.js` on navigation. The worker is registered with `updateViaCache: "none"`,
so the check fetches `sw.js` and `version.js` past the HTTP cache (GitHub Pages sends
`max-age=600`; AUD-013). A changed worker installs into its own cache and waits.

`app.js` posts `"skip"` to a waiting or newly installed worker only when two conditions are true:
the page already had a controller, and the page is not in use. In use means the person has
touched or typed, or a breathing screen runs (AUD-107: with "Start breathing at once" a reload
would restart the breath). The worker then
activates and claims the page, and `controllerchange` reloads it once. After a touch, the new
worker keeps waiting, the page keeps its own version's files, and the next open gets the new
version (AUD-057).

Settings shows `Version X` and `Update now`. Update now works in this order:
1. Offline, it says so and does nothing.
2. It calls `registration.update()`. If that fails (dead link, captive portal), nothing is removed
   and it says so (AUD-056).
3. If a new version installs, it tells that worker to skip waiting, and the page reloads. If
   Freelief is open in another window, the worker refuses, and Settings asks the person to close
   that window and press Update now again (AUD-057).
4. Only when the version is already current does it delete every `freelief-` cache, unregister
   the worker and reload.

Settings in `localStorage` are kept.
