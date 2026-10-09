// The background sound (RLG-045, owner 2026-10-09): music, nature or both, which keeps playing on
// every screen until it is turned off. The Visualizer starts it and chooses it; the shell shows a
// bar with a Stop button on the other screens. Nature is rain or waves, chosen in Settings (RLG-043).
//
// This module only plays. It never touches storage: the shell saves the choice through settings.js
// and tells this module what to play.

import * as audio from "./audio.js";

let config = null;
let mode = "off";
let nature = "rain";
let playing = { stop() {} };
const listeners = new Set();

const NATURE = { rain: (level) => audio.rain(level), waves: (level) => audio.waves(level) };

function start() {
  if (mode === "off") return { stop() {} };
  if (mode === "music") return audio.pads();
  if (mode === "nature") return NATURE[nature]();
  // Both: the nature sound sits under the music, each at its own level (config.calm.bothMix).
  const mix = config.calm.bothMix;
  const parts = [audio.pads(mix.music), NATURE[nature](mix.nature)];
  return { stop() { parts.forEach((part) => part.stop()); } };
}

export function initBackground(loaded, natureSound) {
  config = loaded;
  nature = natureSound;
}

// What plays now: "off", "music", "nature" or "both".
export function current() {
  return mode;
}

export function natureSound() {
  return nature;
}

// Play `next` in place of what plays now. The same choice again does nothing, so the music does not
// restart when the person comes back to the Visualizer.
export function play(next) {
  if (next === mode) return;
  playing.stop();
  mode = next;
  playing = start();
  listeners.forEach((listener) => listener(mode));
}

// Rain or waves. Only the nature part restarts, and only if nature plays now.
export function setNature(next) {
  if (next === nature) return;
  nature = next;
  if (mode === "nature" || mode === "both") restart();
}

// The header's sound button came back on: start the chosen sound again. While sound is off,
// audio.js makes every sound silent, so a restart is needed when it returns.
export function restart() {
  playing.stop();
  playing = start();
}

export function onChange(listener) {
  listeners.add(listener);
}
