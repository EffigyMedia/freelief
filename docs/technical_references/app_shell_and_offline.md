# App shell, urgent help and offline

The owning document for the shell (`app.js`), the urgent-help dialog (`crisis.js`,
`data/crisis-lines.json`), the breathing exercise (`exercises/breathe.js`) and the offline layer
(`sw.js`, `manifest.webmanifest`, `version.js`). Design: `docs/Design_Document.md` Stages 5 and 8.

## Boot
`index.html` loads `version.js` (a classic script) and `app.js` (a module). `app.js` registers the
service worker, then loads `config.json`, `strings/en.json` and `data/crisis-lines.json` in
parallel, builds the shell, starts the breathing exercise, sets `html[data-ready="true"]` and the
`freelief-ready` performance mark. Tests and `bench` wait on those two signals.

## Content Security Policy
A meta tag allows only the app's own origin for every resource type, and no inline script or
style. It is the back-up for REQ-015. Two consequences:
- JavaScript may set `element.style.x` (CSSOM is allowed), but never a `style` attribute string.
- Playwright's `wait_for_function` evaluates a string and is refused (no `unsafe-eval`). Tests use
  `harness.wait_until`, which polls with `page.evaluate`.

## Breathing exercise
Phases come from the active rhythm in `config.json` (`in`, `holdIn`, `out`, `holdOut` in seconds;
a zero phase is skipped). Each phase sets the label (an `aria-live="polite"` region, so a screen
reader hears each phase), a CSS transform transition of the phase's length, and a visible count
(hidden from screen readers to avoid noise). Under reduced motion the circle is fixed at scale 0.8
and the count carries the rhythm. Pause clears every timer and freezes the circle where it is;
Resume restarts the current phase.

## Urgent help
`crisis.deviceRegion()` reads `navigator.languages` and takes the region of the first tag that has
one, through `Intl.Locale(tag).maximize()`. A tag with no region gets its likely region, so `en`
maps to `US` and `fr` to `FR`. No location is read. The dialog is a native `<dialog>` opened with
`showModal()`: it traps focus, closes on Escape, and returns focus to the help control.

Order in the dialog: the intro; the emergency number of the region (or "your local emergency
number"); the region's own lines; the international directory; a closed "Lines in other
countries" disclosure with every other curated region; Close. The disclosure exists because a
device language can name the wrong country (a visitor, or an English phone set to `en-US`
anywhere).

**Every line in `data/crisis-lines.json` carries `source` and `checked`.** Change a line only
after you check its source in the same session, and set `checked` to that date.

## Offline
`sw.js` imports `version.js` and names its cache `freelief-<version>`. Install pre-caches the
`FILES` list with `cache: "reload"`, past the browser's HTTP cache (AUD-013), and calls
`skipWaiting`. Activate deletes only caches whose name starts with `freelief-` and is not the
current one, then claims the clients. Fetch answers same-origin GET requests from the cache first;
on a miss it fetches from the network and stores a good response in the cache. It ignores every
other request.

**The origin is shared** (`effigymedia.github.io` also serves Effigy Arcade, Tiny Arcade and
Drinax Ref Console), so CacheStorage and `localStorage` are shared too (AUD-001). Another app's
worker may delete Freelief's cache; the owner chose to stay on this origin with self-repair
(2026-10-07). On each online launch `app.js` posts `"heal"` to the active worker, which fetches any
`FILES` entry missing from the cache. `test_offline.py` deletes every cache, reloads online,
reloads offline, and expects the guide and the help control; another test runs a real version
update from a scratch copy and checks that a foreign cache survives and the old Freelief cache
goes. **Freelief must never delete a cache it does not own.** The arcades were told about their
own cleanup code through their inboxes. `test_offline.py` fails when a shipped file is missing from `FILES` or a
listed file does not exist, so **add every new shipped file to `FILES`** and bump the version so
the cache is replaced.
