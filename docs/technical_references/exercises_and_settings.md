# Exercises, screens, settings and tones

The owning document for the exercises (`exercises/*.js`), the screens (`screens/*.js`), the
router in `app.js`, `settings.js` and `audio.js`. The shell, urgent help and offline layer are in
`app_shell_and_offline.md`. Design: `docs/Design_Document.md` Stages 5 and 8.

## The screen contract
Every exercise and screen exports `start(container, ctx)` and `stop()`. `ctx` holds `t` and `list`
(strings), `config`, `motion`, `audio` and `rhythm` (the rhythm setting at start). The shell calls
`stop()` on the old screen before `start()` on the new one, so a module must clear its own timers
and frames in `stop()`. **A pending timer or frame must check that its run is still the current
one**: `breathe.js` keeps a `run` object and returns early when `state !== run`. Without this, a
frame queued before `stop()` runs against a cleared state and throws.

## Router
`app.js` maps the URL hash to a module in `ROUTES`. No hash, or an unknown one, shows `breathe`.
A `hashchange` focuses the new screen's `<h1>` (given `tabindex="-1"`), so a screen reader
announces the screen; the first screen at launch takes no focus. The nav link under the screen is
"More ways to calm" (`#menu`) on the breathing screen and "Back to breathing" (`#breathe`) on every
other screen.

## Grounding and calming words
Both are steppers with Back and Next. The text is a polite live region; focus stays on the button
the person used. Grounding has five steps, then a closing line, and "Start again" loops it. Back
is hidden on the first step; `[hidden]` is forced to `display: none !important` because `.button`
sets `display`. Calming words come from the `statements.list` array in `strings/en.json` and wrap
around in both directions.

## Settings
`settings.js` reads `localStorage[config.settings.storageKey]` once at boot, keeps only known
values (a stored rhythm that no longer exists in `config.json` falls back to the default), and
writes the whole object on every change. Every access is in try/catch: with storage blocked, the
defaults stand and a change holds for the visit only. Listeners (`onSettingChange`) let the shell
apply a theme at once. Theme: `system` removes `html[data-theme]`; `dark` or `light` sets it, and
the CSS gives the attribute priority over `prefers-color-scheme`.

## Tones
`audio.js` makes one sine tone per breathing phase with Web Audio: a linear swell over
`attackSeconds` and a fade over `releaseSeconds`, at `volume`, with a frequency per phase, all from
`config.json`. Nothing is created unless the tones setting is on. Turning tones on calls
`unlockAudio()` inside the change event, so the browser's autoplay rule allows sound. A test cannot
listen; `test_slice2.py` counts `createOscillator` calls instead. **How the tones sound is for the
owner to judge on a device.**
