// Soft tones that mark the breath (REQ-007). Generated with Web Audio, so no audio file ships.
// Off by default; nothing plays unless the person turns tones on in Settings.

import { getSetting } from "./settings.js";

let context = null;
let toneConfig = null;

export function initAudio(config) {
  toneConfig = config.tones;
}

function ensureContext() {
  if (!context) {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) return null;
    context = new AudioContextClass();
  }
  if (context.state === "suspended") context.resume();
  return context;
}

// Call from a user gesture (turning tones on), so the browser allows sound.
export function unlockAudio() {
  ensureContext();
}

// One soft tone for a breathing phase: a sine wave that swells and fades.
export function cue(phaseKey) {
  if (!getSetting("tones") || !toneConfig) return;
  const ctx = ensureContext();
  if (!ctx) return;
  const frequency = toneConfig.frequencies[phaseKey];
  if (!frequency) return;
  const now = ctx.currentTime;
  const oscillator = ctx.createOscillator();
  const gain = ctx.createGain();
  oscillator.type = "sine";
  oscillator.frequency.value = frequency;
  gain.gain.setValueAtTime(0, now);
  gain.gain.linearRampToValueAtTime(toneConfig.volume, now + toneConfig.attackSeconds);
  gain.gain.linearRampToValueAtTime(0, now + toneConfig.attackSeconds + toneConfig.releaseSeconds);
  oscillator.connect(gain).connect(ctx.destination);
  oscillator.start(now);
  oscillator.stop(now + toneConfig.attackSeconds + toneConfig.releaseSeconds + 0.05);
}
