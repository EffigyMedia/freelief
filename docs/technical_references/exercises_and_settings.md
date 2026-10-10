# Exercises, screens, settings and sound

The owning document for the router in `app.js`, the activities (`activities/*.js`), the menu and
Settings screens (`screens/menu.js`, `screens/settings.js`), `settings.js`, every sound (`audio.js`,
`background.js`), vibration (`haptics.js`) and the screen wake lock (`wakelock.js`). The shell, the
breathing exercise, urgent help and the offline layer are in `app_shell_and_offline.md`. The trust
pages are in `trust_pages.md`. Design: `docs/Design_Document.md` flows F1, F2, F5 and F7, section 8,
and the Decision Log.

## The screen contract
Every exercise, activity and screen exports `start(container, ctx)` and `stop()`. `ctx` holds:

| Field | What it is |
|---|---|
| `t`, `list` | The text functions from `strings.js`. |
| `config` | The loaded `config.json`. |
| `motion` | `motion.js`; `reducedMotion()` tells whether to move. |
| `audio` | `audio.js`, for the screen's own tones and cues. |
| `haptic` | `haptics.pulse(name)`, one short vibration. |
| `keepAwake` | `wakelock.keepAwake()`, which returns a release function. |
| `rhythm`, `soundsOn` | Read-only setting values at start. |

A screen never touches Settings or storage itself. `screens/settings.js` is the one exception: it
imports `settings.js` and `crisis.regionList()` directly.

The shell calls `stop()` on the old screen before `start()` on the new one. Thus a module must
clear its own timers, frames and observers in `stop()`. **A pending timer or frame must check that
its run is still the current one.** Each module keeps a `run` object, and a callback returns early
when the module's current run is a different object. Without this, a frame queued before `stop()`
runs against a cleared state and throws.

## Router
`app.js` maps the URL hash to a module in `ROUTES`. It accepts only its own names
(`Object.hasOwn`), so a hash such as `#constructor` is not a screen (AUD-005).
- With no hash, the shell shows the screen that the `openOn` setting names: the menu (the default),
  or breathing.
- An unknown hash shows the menu.
- A screen that cannot load, or that fails in `start()`, falls back to the menu, and the address
  becomes `#menu`.

The shell awaits `start()`, then sets `main[data-shown]`. Tests wait on `data-shown`, not on
`data-screen`. A `hashchange` focuses the new screen's `<h1>` (given `tabindex="-1"`), so a screen
reader announces the screen. The first screen at launch takes no focus.

The "Back to menu" row (`#menu`) sits between the header and the screen on every screen. The whole
row is hidden on the menu (UNT-030). Every route change also sets the background-sound duck (see
Background sound).

## The menu (`screens/menu.js`)
The first screen: "What would help right now?" with one large link for each exercise and activity.
Breathe is the first item, and its card is filled and larger. Settings is not on this list. It is
the gear in the header.

## Bubble field (`activities/bubbles.js`)
The field is a `<ul>` of absolutely placed `<li>`, each holding one `<button class="bubble">`. The
field is a grid of `columns` x `rows` slots (`config.json` → `bubbles`). Each bubble takes a free
slot, sits at a random place inside it, and is sized to leave `driftX` and `driftY` pixels for its
drift. Thus no bubble covers another.

A pop plays `audio.pop()`, vibrates once (`pop`), frees the slot and adds `.popping` (a
scale-and-fade of `popMs`). Then the bubble is removed, and a new one appears after `respawnMs`.
Focus passes to the next bubble (or the previous one) before the popped one leaves, so a keyboard
user stays in the field.

Drift is a CSS `drift` animation of `translate`. The "Stop the drifting" toggle pauses it with
`.held`. Under reduced motion no bubble gets `.drifting`, and the toggle is hidden. **Playwright
cannot click a drifting bubble normally** (it is never "stable"). Tests use `click(force=True)`.

## Zen Garden (`activities/garden.js`, route `#garden`)
A tray of sand in SVG (400 by 300 units), with stones and plants (RLG-055, REQ-038).
- **Raking.** A pointer drag across the sand adds one line per tine (`garden.tines`, `tineGap`
  apart) for each move, across the direction of travel. The sand area is a focusable button: the
  arrow keys move a rake dot `keyStep` units and draw as it moves. The oldest lines go when there are
  more than `maxLines`. Smooth the sand removes every line. A sand sound (`audio.sand()`) plays at
  most every `soundEveryMs` while raking.
- **Stones and plants.** Each is a `role="button"` group with a name ("Stone 1, 40 percent across,
  60 percent down") and a round hit area at least 44 px on a phone. A tap chooses it; a drag moves
  it and does not choose; the arrow keys move a focused one; Delete, Backspace or Remove takes it
  away. Add a stone and Add a plant place a new one where there is room, up to `maxItems`. Three
  stones are there at the start.
- **Rings.** Around each item the sand keeps `rings` circles, and a mask hides the raked lines
  inside them, so the lines seem to flow around the item.
- No score, no timer, no end. A polite live line says what happened.

## Unblock (`activities/unblock.js`)
A calm sliding-block puzzle. It replaced the colour sort (`sort.js`) on 2026-10-09 (RLG-040,
REQ-035). Blocks lie on a `size` x `size` board (6 x 6). Each block slides only along its length.
The person slides them to make a way for the blue block, which leaves through the gap in the right
edge at row `exitRow`. There is no score, move count, timer or losing state.

**The boards** are in `config.json` → `unblock.boards`: 15 boards from easy to hard. Each board is
a list of six strings. `.` is an empty cell, `A` is the blue block, and each other letter is one
block. `test_unblock.py` solves every board, so add a board only when it passes that test. The board
in use stays chosen while the app is open.

**Names.** Every block is a `<button>` with a name that says its number, its direction and its
cells, such as "Block 3, down, column 4, rows 1 to 3". The blue block has no number. A polite live
region says what happened.

**Three ways to move:**
- Drag a block along its length. It moves cell by cell as far as there is room. A drag starts only
  after `dragThreshold` pixels, and the whole drag is one move for Undo.
- Press an arrow key on a focused block. An arrow across the block's length says which way it can
  go and does not move it.
- Choose a block (tap, Enter or Space). Two Slide buttons appear for it. Choose it again, or press
  Escape, to let it go.

Each move plays the `swap` cue and vibrates once. When the blue block reaches the right edge, the
board is solved: it plays `done`, vibrates `done`, says so, and moves focus to "Next board". Undo
takes back any move, including the last move. Start again resets the board. Under reduced motion
the board gets `.still`, and blocks do not slide in an animation.

## Ripple pond (`activities/ripple.js`)
Still water. A touch makes rings spread from that point, and a finger drawn across the water leaves
a ripple every `trailSpacing` pixels (REQ-032). The pond is one real `<button>`. A key press, or a
screen reader's activation, sends a click with no pointer before it, and that makes a ripple at a
random place at least `keyboardMargin` pixels from the edge. Each ripple plays `audio.drop()`. A
touch and a key press vibrate once (`ripple`). The trail of a drag does not vibrate, because it is
continuous.

**The rings interfere** (RLG-041). The water is a fine grid of SVG dots, `wave.dotSpacing` pixels
apart. No canvas is used, by the architecture rule. The exported `waveHeight()` gives the height of
the water at one point: the sum of one wave packet per ripple. A packet is a few crests under a
bell-shaped envelope. It travels out at `wave.speed`, and it fades with time (`fadeSeconds`) and
with distance (`spreadFalloff`). Each dot's opacity is `restLevel` plus that sum. Where two crests
meet, the water is brighter. Where a crest meets a trough, they cancel.

The grid is drawn on animation frames only while a ripple moves. A dot is written only when its
level changes by a visible amount. When the last ripple ends, the frames stop, so still water costs
nothing. At most `maxRipples` ripples live at once. A `ResizeObserver` lays out the grid again when
the pond changes size.

Under reduced motion there is no dot grid. Each ripple shows `rings` still rings that only fade.

## Mandala coloring (`activities/mandala.js`)
The person chooses a soft color, then taps a part of the mandala to fill it (REQ-033). There is no
score, timer or end. **New mandala** starts the next of the eight designs, blank. After the last
design, it starts the first again.

The designs are formulas in `config.json` → `mandala.designs`, so no image ships. Each design is a
list of rings: a center, then rings of `petal`, `band`, `dot`, `scallop` or `diamond` parts, with a
`count`, an `inner` and an `outer` radius, and an optional `offset` and `width`. `mandala.palette`
holds six colors, each with a name, an HSL color and a note. The CSP refuses inline style
attributes, so script sets each swatch's color through `--swatch`.

The colors are a `<fieldset>` of radio buttons. Choosing a color plays its note with
`audio.chime()`. Each part of the mandala is an SVG `<path>` with `role="button"` and a name such as
"Ring 2, shape 3 of 12, blank". A fill plays the color's chime, vibrates once (`fill`) and updates a
polite live line. The SVG is one tab stop (roving `tabindex`):
- Left and right arrows move around a ring.
- Up and down arrows move between rings, in the same direction around the circle.
- Home goes to the center, and End goes to the outer ring.
- Enter or Space fills the part.

## The Kaleidoscope (`activities/calm.js`, route `#calm`)
The Kaleidoscope (RLG-057): a slow kaleidoscope in SVG. `pattern()` mirrors one wedge of
`calm.kaleidoscope.shapesPerCell` shapes into `folds` copies; the `.kaleido-turn` group turns once
in `turnSeconds`, the field's hue drifts over `hueSeconds`, and every `patternSeconds` a new layer
cross-fades in over `fadeSeconds`. Under reduced motion the turn and the drift stop. It has no sound choice of its own
(RLG-049). The sound bar in the header plays music, rain or waves on every screen, this one too;
its hidden intro says so.

**The patterns.** `nextPattern()` appends a new layer to `.kaleido-turn` every `patternSeconds`;
the CSS class `shown` fades it in over `fadeSeconds` (`--fade`) while the old layer fades out, and
the old layer is removed after the fade. The turn (`--turn`) and the hue drift (`--hue`) are CSS
animations. Under reduced motion the field has the class `still`, so only the cross-fade remains.

**Full screen** fills the screen with the stage, through the browser's full screen where it exists
and a CSS class everywhere. In full screen the stage shows its own "Need urgent help?" button
(AUD-075), which leaves full screen and opens help, and an Exit button. Escape also leaves full
screen.

**Black screen** appends one full-screen black `<button>` to `body`. A click, Enter, Space or Escape
removes it and returns focus. Under the cover, no new pattern is drawn and the stage stops moving
(the class `asleep`).
The sound keeps playing.

The screen takes the wake lock while it runs. `stop()` clears the timers, releases the wake lock,
removes the cover and leaves full screen. It does not stop the sound.

## Settings (`settings.js`, `screens/settings.js`)
`settings.js` is the only module that touches `localStorage`. The key is
`config.json` → `settings.storageKey` (`freelief.settings.v2`).

**Only the values the person changed are stored** (AUD-062). The defaults come from `config.json`
at each boot. Thus a setting that the person never touched follows the default of the version they
run, and a new default reaches them. `setSetting()` writes only the chosen values, and a choice
of the default value removes the stored value (AUD-110). `resetSettings()`, behind Reset settings,
removes every stored value except `sounds` (the header speaker's, so a reset never starts sound;
AUD-114) and tells the listeners each setting that changed.

At boot, `initSettings()` does this:
1. If no v2 store exists, it migrates the v1 store (`legacyStorageKey`). Only a value that differs
   from today's default carries over, and a stored `box` rhythm is dropped. Then it deletes the v1
   key.
2. It uses a stored value only if it passes its check. A stored value it cannot read, such as a
   setting of a newer version or one this version retired, is kept apart and written back at each
   save, so a rollback loses no choice (AUD-121); a new choice of that setting replaces it. A rhythm must exist in
   `config.json`. A theme, an `openOn` or an `awakeMinutes` must be in its list of choices
   (`awakeMinutes` 0 means Always). `sounds` and
   `haptics` must be booleans. `helpRegion` must be `auto` or two capital letters. Checks use own
   keys only.

Every access is in try/catch. With storage blocked, the defaults stand, and a change holds for the
visit only. Listeners (`onSettingChange`) let the shell act on a change at once.

| Setting | Where it is set | Default |
|---|---|---|
| `rhythm` | Settings | `breathing.defaultRhythm` |
| `openOn` ("When Freelief opens") | Settings | `settings.openOnDefault` (`menu`) |
| `awakeMinutes` ("Keep the screen on") | Settings | `wakeLock.idleMinutesDefault` (30) |
| `theme` | Settings | `theme.default` (`system`) |
| `haptics` (vibration) | Settings | `haptics.enabledByDefault` |
| `helpRegion` | Settings | `crisis.defaultRegion` (`auto`) |
| `sounds` | The header's sound button | `sounds.enabledByDefault` |

Theme: `system` removes `html[data-theme]`; `dark` or `light` sets it, and the CSS gives the
attribute priority over `prefers-color-scheme`. A saved region that is no longer curated shows as
Automatic in the Settings select. Under the version line, a line says whether this version is
saved for use with no internet: the offline cache is written all at once, so it exists only when it
is complete (AUD-112). The version line and Update now are in `app_shell_and_offline.md`.

## Sound (`audio.js`)
Every sound is made with Web Audio, so no audio file ships. All tunables are in `config.json` →
`sounds`.

**Before the first gesture, nothing is created.** A browser allows sound only after the first tap
or key press. The first gesture anywhere in the app unlocks sound. The breath sound then begins at
the next phase.

**One master volume.** Every sound goes through one gain node (`output`). The background sound goes
through a second gain node (`bed`) first, so a screen can lower it.

**The sound button.** `applySound(false)` fades the master volume to 0 over
`sounds.muteFadeSeconds`, cuts every sound that is fading, and then suspends the audio context.
`applySound(true)` resumes it and fades back in over the same time. While the audio clock is
paused, a sound that stops is cut at once, not faded. Otherwise its frozen fade would play when
sound comes back. The shell also calls `applySound(false)` while urgent help is open and while the
page is hidden.

The sounds:

| Function | Used by | What it is |
|---|---|---|
| `cue(phase, seconds)` | Breathing | The sound of a breath (RLG-050): soft looping noise for the whole in or out phase, through a band filter that brightens on the in-breath and darkens on the out-breath (`sounds.breath.in` and `.out`); it swells in and fades out. A hold plays one light tap (a short burst of filtered noise, `sounds.breath.tap`) at each second. It returns a stop function. |
| `play(name)` | Zen Garden, Unblock | A named cue from `sounds.cues` (`choose`, `swap`, `done`): one or more notes, a gap apart. |
| `sand()` | Zen Garden | A soft sand sound while raking: filtered noise centered on A5. |
| `pop()` | Bubbles | A short burst of band-passed noise over a falling thump. |
| `drop()` | Ripple pond | A short sine whose pitch rises fast, through a low-pass filter. |
| `chime(note)` | Mandala | A struck bell: inharmonic partials and a quieter second strike. |
| `pads(level)` | Background (music) | Slow chords from `sounds.pads`: each note is two detuned triangle waves through one low-pass filter, with long swells. |
| `rain(level)` | Background (nature) | Filtered looping noise that swells slowly, with soft drops pitched to C major notes. |
| `waves(level)` | Background (nature) | Filtered looping noise. Each wave swells and opens the filter, then falls back, at uneven gaps and heights. |

Pitched sounds that can play with the music stay in C major (RLG-046). The pop and the water drop
are natural sounds and are not tuned. A test cannot listen; the sound tests count audio nodes, such
as `createOscillator` calls, instead. **How a sound sounds is for the owner to judge on a device.**

## Background sound (`background.js`) and the sound bar
**The background sound** is music, and rain or waves, which keeps playing on every screen until the
person stops it (RLG-045, RLG-049). `background.js` only plays. It never touches storage, and it
never starts a sound by itself, so each visit starts silent.
- `toggle(sound)` turns `music`, `rain` or `waves` on or off. Rain and waves replace each other;
  music plays with either. Both parts start again at their new levels, because the mix changes:
  with both, the nature sound sits under the music (`calm.bothMix`).
- `current()` gives `{ music, nature }`; `playing()` says whether anything plays.
- `hold()` stops the loops while sound is held (urgent help open, app hidden), so no notes queue
  in the paused clock (AUD-113). `restart()` starts what plays again.

**Ducking.** On each route change, the shell calls `audio.duck()`. On a route in
`calm.duckRoutes` (breathing), the `bed` volume falls to `sounds.background.duckLevel` over
`duckSeconds`, so the background sits under the breath sound. On other routes it comes back up.

**The sound bar** (RLG-049) is three round toggle buttons in the header's middle row, on every
screen: a music note, a raindrop and a wave, in a `role="group"` named "Background sound". Each has
a fixed name and `aria-pressed`, and a pressed button is filled. A tap calls `toggle()`; a tap that
turns a sound on while the speaker is off also turns sound on.

## Vibration (`haptics.js`)
One short vibration for a single triggered event in an activity (REQ-034), never for anything
continuous. `pulse(name)` plays the pattern in `config.json` → `haptics.patterns`: `pop`, `choose`,
`swap`, `done`, `ripple` and `fill`. It does nothing when the `haptics` setting is off, or
when the browser has no Vibration API (such as Safari on iPhone). A refused vibration is not an
error. The breath, a drag trail and raking never vibrate. `haptics.js` reads Settings only
through `getSetting()`.

## Screen wake lock (`wakelock.js`)
Keeps the screen on while breathing or the Kaleidoscope runs, so the phone does not dim or lock
mid-breath. `keepAwake()` asks for the Screen Wake Lock and returns a release function. Calls nest:
the last release frees the lock. The browser drops the lock when the page is hidden, so the module
asks again when the page becomes visible. A browser without the API, or one that refuses, lets the
screen sleep, and nothing fails.

The lock has an end (AUD-103, REQ-037). Each touch or key starts an idle time again. After the time
in `awakeMinutes` (10, 30 or 60 minutes) with no input, the module releases the lock, and the
exercise goes on; the next touch takes it back. With 0 (Always, RLG-048) there is no idle time. No countdown is shown. Breathing releases the lock
when it is paused and takes it again on resume. Only one request is in flight at a time, and a lock
granted after the screen stopped wanting it is released at once (AUD-081).

## Grounding and calming words (removed 2026-10-07, UNT-032)
Both screens were removed for weak research. One lesson from them still applies everywhere:
`[hidden]` is forced to `display: none !important`, because `.button` sets `display`.
