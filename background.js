// The background sound (RLG-045, RLG-049; owner 2026-10-09): music, and rain or waves, which keep
// playing on every screen until they are turned off. The sound bar in the header has one button
// for each: a tap plays that sound, and a tap on a sound that plays stops it. Rain and waves replace
// each other; music plays with either.
//
// This module only plays. It never touches storage, and nothing is saved: Freelief never starts a
// sound by itself, so each visit starts silent.

import * as audio from "./audio.js";

let config = null;
let music = false;
let nature = null; // null, "rain" or "waves"
let musicPart = { stop() {} };
let naturePart = { stop() {} };
const listeners = new Set();

const NATURE = { rain: (level) => audio.rain(level), waves: (level) => audio.waves(level) };

// With both playing, the nature sound sits under the music (config.calm.bothMix).
const musicLevel = () => (nature ? config.calm.bothMix.music : 1);
const natureLevel = () => (music ? config.calm.bothMix.nature : 1);

function startMusic() {
  musicPart.stop();
  musicPart = music ? audio.pads(musicLevel()) : { stop() {} };
}

function startNature() {
  naturePart.stop();
  naturePart = nature ? NATURE[nature](natureLevel()) : { stop() {} };
}

export function initBackground(loaded) {
  config = loaded;
}

// What plays now: { music, nature }.
export function current() {
  return { music, nature };
}

export function playing() {
  return music || nature !== null;
}

// A tap on a button in the sound bar: "music", "rain" or "waves".
export function toggle(sound) {
  if (sound === "music") music = !music;
  else nature = nature === sound ? null : sound;
  // A change in what plays changes the mix, so both parts start again at their new levels.
  startMusic();
  startNature();
  listeners.forEach((listener) => listener(current()));
}

// While urgent help is open or the app is hidden, the audio clock is paused. A loop that kept
// scheduling would queue its notes at one frozen time, and they would all play at once when sound
// came back (AUD-113). So the loops stop while sound is held, and what plays is kept.
export function hold() {
  musicPart.stop();
  naturePart.stop();
  musicPart = { stop() {} };
  naturePart = { stop() {} };
}

// Sound came back: start what plays again. While sound is off, audio.js makes every sound silent.
export function restart() {
  startMusic();
  startNature();
}

export function onChange(listener) {
  listeners.add(listener);
}
