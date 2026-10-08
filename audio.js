// Subtle sounds (REQ-007): soft tones for the breath and short cues for the activities. Generated
// with Web Audio, so no audio file ships. On by default; one "Sounds" switch in Settings turns all
// of them off (owner, 2026-10-07).
//
// Browsers allow sound only after the person's first tap or key press. Until then nothing is
// created, so no "AudioContext was not allowed to start" warning appears; the first gesture
// anywhere in the app unlocks sound, and the breathing tones begin at the next phase.

import { getSetting } from "./settings.js";

let context = null;
let sounds = null;
let unlocked = false;

export function initAudio(config) {
  sounds = config.sounds;
  const unlock = () => {
    unlocked = true;
    if (getSetting("sounds")) ensureContext();
    window.removeEventListener("pointerdown", unlock, true);
    window.removeEventListener("keydown", unlock, true);
  };
  window.addEventListener("pointerdown", unlock, true);
  window.addEventListener("keydown", unlock, true);
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

// Call from a user gesture (turning sounds on), so the browser allows sound.
export function unlockAudio() {
  unlocked = true;
  ensureContext();
}

// One sine note that swells and fades, starting `delay` seconds from now.
function note(ctx, frequency, delay, attack, release, volume) {
  const start = ctx.currentTime + delay;
  const oscillator = ctx.createOscillator();
  const gain = ctx.createGain();
  oscillator.type = "sine";
  oscillator.frequency.value = frequency;
  gain.gain.setValueAtTime(0, start);
  gain.gain.linearRampToValueAtTime(volume, start + attack);
  gain.gain.linearRampToValueAtTime(0, start + attack + release);
  oscillator.connect(gain).connect(ctx.destination);
  oscillator.start(start);
  oscillator.stop(start + attack + release + 0.05);
}

function canPlay() {
  return sounds && unlocked && getSetting("sounds");
}

// A named cue from config.json → sounds.cues: one or more notes, a gap apart.
export function play(name) {
  if (!canPlay()) return;
  const cue = sounds.cues[name];
  const ctx = cue && ensureContext();
  if (!ctx) return;
  cue.notes.forEach((frequency, i) =>
    note(ctx, frequency, i * cue.gapSeconds, cue.attackSeconds, cue.releaseSeconds, cue.volume));
}

const SILENT = () => {};

// A soft tone that lasts the whole breathing phase (owner, 2026-10-07): it swells in, holds, and
// fades out as the phase ends. A quiet octave above the note warms it. Returns a function that
// stops the tone at once (pause, or leaving the screen).
export function cue(phaseKey, seconds) {
  if (!canPlay()) return SILENT;
  const breath = sounds.breath;
  const frequency = breath.frequencies[phaseKey];
  const ctx = frequency && ensureContext();
  if (!ctx) return SILENT;
  const start = ctx.currentTime;
  const end = start + seconds;
  const attack = Math.min(breath.attackSeconds, seconds * 0.3);
  const release = Math.min(breath.releaseSeconds, seconds * 0.4);
  const gain = ctx.createGain();
  gain.gain.setValueAtTime(0, start);
  gain.gain.linearRampToValueAtTime(breath.volume, start + attack);
  gain.gain.setValueAtTime(breath.volume, end - release);
  gain.gain.linearRampToValueAtTime(0, end);
  gain.connect(ctx.destination);
  const voices = [[frequency, 1], [frequency * 2, breath.octaveLevel]].map(([hz, level]) => {
    const oscillator = ctx.createOscillator();
    const voice = ctx.createGain();
    oscillator.type = "sine";
    oscillator.frequency.value = hz;
    voice.gain.value = level;
    oscillator.connect(voice).connect(gain);
    oscillator.start(start);
    oscillator.stop(end + 0.05);
    return oscillator;
  });
  return () => {
    const now = ctx.currentTime;
    gain.gain.cancelScheduledValues(now);
    gain.gain.setTargetAtTime(0, now, 0.08);
    voices.forEach((oscillator) => { try { oscillator.stop(now + 0.4); } catch { /* already stopped */ } });
  };
}

// The Calm screen's music (owner, 2026-10-07): slow, soft pads that move through a few gentle
// chords. Each chord note is two slightly detuned triangle waves through a low-pass filter, with
// long swells, and each chord overlaps the next. `level` scales the volume (the Both mix).
// Returns { stop() }. Silent when sounds are off.
export function pads(level = 1) {
  if (!canPlay()) return { stop: SILENT };
  const ctx = ensureContext();
  if (!ctx) return { stop: SILENT };
  const settings = sounds.pads;
  const master = ctx.createGain();
  master.gain.value = settings.volume * level;
  const filter = ctx.createBiquadFilter();
  filter.type = "lowpass";
  filter.frequency.value = settings.cutoffHz;
  filter.connect(master).connect(ctx.destination);
  const live = new Set();
  let chord = 0;
  let timer = 0;

  function playChord() {
    const start = ctx.currentTime;
    const end = start + settings.chordSeconds + settings.releaseSeconds;
    for (const frequency of settings.chords[chord % settings.chords.length]) {
      const voice = ctx.createGain();
      voice.gain.setValueAtTime(0, start);
      voice.gain.linearRampToValueAtTime(1, start + settings.attackSeconds);
      voice.gain.setValueAtTime(1, start + settings.chordSeconds);
      voice.gain.linearRampToValueAtTime(0, end);
      voice.connect(filter);
      for (const cents of [-settings.detuneCents, settings.detuneCents]) {
        const oscillator = ctx.createOscillator();
        oscillator.type = "triangle";
        oscillator.frequency.value = frequency;
        oscillator.detune.value = cents;
        oscillator.connect(voice);
        oscillator.start(start);
        oscillator.stop(end + 0.05);
        live.add(oscillator);
        oscillator.onended = () => live.delete(oscillator);
      }
    }
    chord += 1;
    timer = setTimeout(playChord, settings.chordSeconds * 1000);
  }

  playChord();
  return {
    stop() {
      clearTimeout(timer);
      const now = ctx.currentTime;
      master.gain.setTargetAtTime(0, now, 0.4);
      live.forEach((oscillator) => { try { oscillator.stop(now + 2); } catch { /* already stopped */ } });
    },
  };
}

// The shape trace's "singing glass" (owner, 2026-10-07): a sustained, slightly beating tone, like a
// wet finger on a crystal rim. It sounds only while the person moves, louder with speed, and
// fades when they stop. Returns { move(speed), stop() }.
export function glass(frequency) {
  let voice = null;
  let idle = 0;

  function build(ctx) {
    const settings = sounds.glass;
    const master = ctx.createGain();
    master.gain.value = 0;
    master.connect(ctx.destination);
    const oscillators = [];
    for (const [ratio, level] of settings.partials) {
      for (const detune of [0, settings.beatHz]) {
        const oscillator = ctx.createOscillator();
        const partial = ctx.createGain();
        oscillator.type = "sine";
        oscillator.frequency.value = (frequency || settings.frequency) * ratio + detune;
        partial.gain.value = level / 2;
        oscillator.connect(partial).connect(master);
        oscillator.start();
        oscillators.push(oscillator);
      }
    }
    return { ctx, master, oscillators, settings };
  }

  return {
    move(speed) {
      if (!canPlay()) return;
      const ctx = ensureContext();
      if (!ctx) return;
      voice = voice || build(ctx);
      // Louder with speed (owner, 2026-10-07): from a quiet floor when slow to full volume when fast.
      const level = (voice.settings.minLevel + (1 - voice.settings.minLevel) * Math.min(1, speed)) * voice.settings.volume;
      voice.master.gain.setTargetAtTime(level, ctx.currentTime, voice.settings.riseSeconds);
      clearTimeout(idle);
      idle = setTimeout(() => {
        if (voice) voice.master.gain.setTargetAtTime(0, voice.ctx.currentTime, voice.settings.fallSeconds);
      }, voice.settings.idleMs);
    },
    stop() {
      clearTimeout(idle);
      if (!voice) return;
      const { ctx, master, oscillators } = voice;
      master.gain.setTargetAtTime(0, ctx.currentTime, 0.1);
      oscillators.forEach((oscillator) => oscillator.stop(ctx.currentTime + 0.6));
      voice = null;
    },
  };
}

// A buffer of white noise, made once and reused by the pop and the rain.
let noiseBuffer = null;
function noise(ctx) {
  if (!noiseBuffer) {
    noiseBuffer = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate);
    const data = noiseBuffer.getChannelData(0);
    for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
  }
  const source = ctx.createBufferSource();
  source.buffer = noiseBuffer;
  return source;
}

// A soft, percussive pop when a bubble bursts (owner: "more soft percussive than a tone"): a very
// short burst of band-passed noise over a quick, falling thump.
export function pop() {
  if (!canPlay()) return;
  const ctx = ensureContext();
  if (!ctx) return;
  const settings = sounds.pop;
  const now = ctx.currentTime;
  const pitch = settings.pitchVariation * (Math.random() * 2 - 1);

  const burst = noise(ctx);
  const band = ctx.createBiquadFilter();
  band.type = "bandpass";
  band.frequency.value = settings.noiseHz * (1 + pitch);
  band.Q.value = settings.noiseQ;
  const burstGain = ctx.createGain();
  burstGain.gain.setValueAtTime(settings.noiseVolume, now);
  burstGain.gain.exponentialRampToValueAtTime(0.0001, now + settings.noiseSeconds);
  burst.connect(band).connect(burstGain).connect(ctx.destination);
  burst.start(now, Math.random());
  burst.stop(now + settings.noiseSeconds + 0.02);

  const thump = ctx.createOscillator();
  const thumpGain = ctx.createGain();
  thump.type = "sine";
  thump.frequency.setValueAtTime(settings.thumpStartHz * (1 + pitch), now);
  thump.frequency.exponentialRampToValueAtTime(settings.thumpEndHz, now + settings.thumpSeconds);
  thumpGain.gain.setValueAtTime(settings.thumpVolume, now);
  thumpGain.gain.exponentialRampToValueAtTime(0.0001, now + settings.thumpSeconds);
  thump.connect(thumpGain).connect(ctx.destination);
  thump.start(now);
  thump.stop(now + settings.thumpSeconds + 0.02);
}

// The Calm screen's rain (owner: an atonal mode, "noise like rain"): looping noise, shaped by a
// low-pass and a high-pass filter, whose level breathes slowly, with soft drops now and then.
// `level` scales the volume (the Both mix). Returns { stop() }. Silent when sounds are off.
export function rain(level = 1) {
  if (!canPlay()) return { stop: SILENT };
  const ctx = ensureContext();
  if (!ctx) return { stop: SILENT };
  const settings = sounds.rain;
  const master = ctx.createGain();
  master.gain.setValueAtTime(0, ctx.currentTime);
  master.gain.linearRampToValueAtTime(settings.volume * level, ctx.currentTime + settings.fadeInSeconds);
  master.connect(ctx.destination);

  const bed = noise(ctx);
  bed.loop = true;
  const low = ctx.createBiquadFilter();
  low.type = "lowpass";
  low.frequency.value = settings.lowpassHz;
  const high = ctx.createBiquadFilter();
  high.type = "highpass";
  high.frequency.value = settings.highpassHz;
  const swell = ctx.createGain();
  swell.gain.value = 1 - settings.swellDepth;
  const lfo = ctx.createOscillator();
  const lfoDepth = ctx.createGain();
  lfo.frequency.value = settings.swellHz;
  lfoDepth.gain.value = settings.swellDepth;
  lfo.connect(lfoDepth).connect(swell.gain);
  bed.connect(low).connect(high).connect(swell).connect(master);
  bed.start();
  lfo.start();

  let timer = 0;
  function drop() {
    const now = ctx.currentTime;
    const tick = noise(ctx);
    const band = ctx.createBiquadFilter();
    band.type = "bandpass";
    band.frequency.value = settings.dropHz * (0.7 + Math.random() * 0.6);
    band.Q.value = settings.dropQ;
    const gain = ctx.createGain();
    gain.gain.setValueAtTime(settings.dropVolume * (0.4 + Math.random() * 0.6), now);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + settings.dropSeconds);
    tick.connect(band).connect(gain).connect(master);
    tick.start(now, Math.random());
    tick.stop(now + settings.dropSeconds + 0.02);
    timer = setTimeout(drop, settings.dropEveryMs * (0.3 + Math.random() * 1.4));
  }
  drop();

  return {
    stop() {
      clearTimeout(timer);
      const now = ctx.currentTime;
      master.gain.cancelScheduledValues(now);
      master.gain.setTargetAtTime(0, now, 0.4);
      bed.stop(now + 2);
      lfo.stop(now + 2);
    },
  };
}
