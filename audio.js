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
// Set while sound is off, urgent help is open or the app is hidden. Then nothing may wake the
// audio: a breathing tone or a cue would otherwise resume it silently in the background (AUD-082).
let held = false;

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

// Every sound goes through one master volume, so the sound button can fade it (owner, 2026-10-08).
// The background sound (music and nature, RLG-045) goes through its own volume first, so a screen
// with its own tones, such as breathing, can lower it under them.
let output = null;
let bed = null;
let ducked = false;
let fadeTimer = 0;

function ensureContext() {
  if (!context) {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) return null;
    context = new AudioContextClass();
    output = context.createGain();
    output.connect(context.destination);
    bed = context.createGain();
    bed.gain.value = ducked ? sounds.background.duckLevel : 1;
    bed.connect(output);
  }
  if (context.state === "suspended" && !held) context.resume();
  return context;
}

// Call from a user gesture (turning sounds on), so the browser allows sound.
export function unlockAudio() {
  unlocked = true;
  ensureContext();
}

// The header's sound button (owner, 2026-10-08). Off silences every sound at once, mid-note;
// on allows the next sound, and is a gesture, so the browser lets it start.
// Off fades every sound out and then pauses the audio; on resumes it and fades back in. A hard cut
// was jarring (owner, 2026-10-08). The fade length is sounds.muteFadeSeconds.
export function applySound(on) {
  const fade = sounds?.muteFadeSeconds ?? 0.6;
  clearTimeout(fadeTimer);
  held = !on;
  if (on) {
    unlockAudio();
    if (!output) return;
    const now = context.currentTime;
    hold(output.gain, now);
    output.gain.linearRampToValueAtTime(1, now + fade);
    return;
  }
  if (!context || context.state !== "running") return;
  const now = context.currentTime;
  hold(output.gain, now);
  output.gain.linearRampToValueAtTime(0, now + fade);
  fadeTimer = setTimeout(() => {
    fading.forEach((cut) => cut());
    fading.clear();
    if (context.state === "running") context.suspend();
  }, fade * 1000 + 50);
}

// Stop a parameter's planned changes and hold the value it has now. cancelScheduledValues alone
// drops a ramp that is still running, and the value then jumps back to where the ramp started: at
// the end of an out-breath that was a sharp click (owner report, RLG-053).
function hold(param, now) {
  if (param.cancelAndHoldAtTime) {
    param.cancelAndHoldAtTime(now);
    return;
  }
  const value = param.value;
  param.cancelScheduledValues(now);
  param.setValueAtTime(value, now);
}

// Lower the background sound under a screen's own tones, or bring it back (RLG-045). The change is a
// slow ramp, so it is not heard as a step.
export function duck(on) {
  ducked = on;
  if (!bed) return;
  const now = context.currentTime;
  hold(bed.gain, now);
  bed.gain.linearRampToValueAtTime(on ? sounds.background.duckLevel : 1, now + sounds.background.duckSeconds);
}

// While sound is off the audio clock is paused, so a fade scheduled on it would only run when sound
// comes back, and the person would hear the old sound again (owner report, 2026-10-08). A sound
// stopped while the clock is paused is cut off at once instead: silent, because nothing is heard.
function paused(ctx) {
  return ctx.state !== "running";
}

// Sounds that are fading out. When the audio pauses partway through a fade, each is cut off first,
// so the frozen tail of the fade cannot play when sound comes back (owner report, 2026-10-08).
const fading = new Set();
function fadingUntil(cut, seconds) {
  fading.add(cut);
  setTimeout(() => fading.delete(cut), seconds * 1000);
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
  oscillator.connect(gain).connect(output);
  oscillator.start(start);
  oscillator.stop(start + attack + release + 0.05);
}

function canPlay() {
  return sounds && unlocked && !held && getSetting("sounds");
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

// The breathing sound (owner, 2026-10-09; RLG-050): the sound of a breath, not a tone. Each in and
// out phase is soft noise that swells and fades over the whole phase, through a band filter that
// moves: it brightens as the person breathes in and darkens as they breathe out, so the two differ.
// A hold (box breathing) plays one light tap at each second, so the person can count it. Returns a
// function that stops the sound at once (pause, or leaving the screen).
export function cue(phaseKey, seconds) {
  if (!canPlay()) return SILENT;
  const ctx = ensureContext();
  if (!ctx) return SILENT;
  const breath = sounds.breath;
  const start = ctx.currentTime;
  const end = start + seconds;
  const master = ctx.createGain();
  // A gentle high cut over the whole breath sound, so it stays soft (owner, 2026-10-10; RLG-059).
  const soften = ctx.createBiquadFilter();
  soften.type = "lowpass";
  soften.frequency.value = breath.lowpassHz;
  master.connect(soften).connect(output);
  const sources = [];

  if (phaseKey === "in" || phaseKey === "out") {
    const shape = breath[phaseKey];
    const air = noise(ctx);
    air.loop = true;
    const band = ctx.createBiquadFilter();
    band.type = "bandpass";
    band.Q.value = shape.q;
    band.frequency.setValueAtTime(shape.fromCutoffHz, start);
    band.frequency.exponentialRampToValueAtTime(shape.toCutoffHz, end);
    const attack = Math.max(breath.minEdgeSeconds, seconds * breath.attackShare);
    const release = Math.max(breath.minEdgeSeconds, seconds * breath.releaseShare);
    master.gain.setValueAtTime(0, start);
    master.gain.linearRampToValueAtTime(breath.volume, start + attack);
    master.gain.setValueAtTime(breath.volume, Math.max(start + attack, end - release));
    master.gain.linearRampToValueAtTime(0, end);
    air.connect(band).connect(master);
    air.start(start, Math.random());
    air.stop(end + 0.05);
    sources.push(air);
  } else {
    // A hold: one light tap at the start of each second.
    const tap = breath.tap;
    for (let second = 0; second < Math.round(seconds); second++) {
      const at = start + second;
      const click = noise(ctx);
      const band = ctx.createBiquadFilter();
      band.type = "bandpass";
      band.frequency.value = tap.bandHz;
      band.Q.value = tap.q;
      const gain = ctx.createGain();
      gain.gain.setValueAtTime(0, at);
      gain.gain.linearRampToValueAtTime(tap.volume, at + 0.004);
      gain.gain.exponentialRampToValueAtTime(0.0001, at + tap.seconds);
      click.connect(band).connect(gain).connect(master);
      click.start(at, Math.random());
      click.stop(at + tap.seconds + 0.02);
      sources.push(click);
    }
  }

  const unplug = () => { master.disconnect(); soften.disconnect(); };
  return () => {
    const now = ctx.currentTime;
    const stopAll = (when) => sources.forEach((source) => { try { source.stop(when); } catch { /* already stopped */ } });
    if (paused(ctx)) {
      unplug();
      stopAll();
      return;
    }
    hold(master.gain, now);
    master.gain.setTargetAtTime(0, now, 0.08);
    stopAll(now + 0.4);
    // A source already told to stop at the phase's end keeps that time, so the faded sound is
    // disconnected once the fade is over.
    setTimeout(() => unplug(), 450);
    fadingUntil(() => {
      unplug();
      stopAll();
    }, 0.4);
  };
}

// The background music (owner, 2026-10-07; RLG-045): slow, soft pads that move through a few gentle
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
  filter.connect(master).connect(bed);
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
      if (paused(ctx)) {
        master.disconnect();
        live.forEach((oscillator) => { try { oscillator.stop(); } catch { /* already stopped */ } });
        return;
      }
      master.gain.setTargetAtTime(0, now, 0.4);
      live.forEach((oscillator) => { try { oscillator.stop(now + 2); } catch { /* already stopped */ } });
      fadingUntil(() => {
        master.disconnect();
        live.forEach((oscillator) => { try { oscillator.stop(); } catch { /* already stopped */ } });
      }, 2);
    },
  };
}

// Two seconds of white noise, made once and shared by every noise sound (the breath, the pop, the
// rain, the waves, the sand).
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

// The sound of raking sand (RLG-055): a short, soft brush of filtered noise. Noise has no pitch.
export function sand() {
  if (!canPlay()) return;
  const ctx = ensureContext();
  if (!ctx) return;
  const settings = sounds.sand;
  const now = ctx.currentTime;
  const brush = noise(ctx);
  const band = ctx.createBiquadFilter();
  band.type = "bandpass";
  band.frequency.value = settings.bandHz;
  band.Q.value = settings.q;
  const gain = ctx.createGain();
  gain.gain.setValueAtTime(0, now);
  gain.gain.linearRampToValueAtTime(settings.volume, now + settings.seconds * 0.3);
  gain.gain.linearRampToValueAtTime(0, now + settings.seconds);
  brush.connect(band).connect(gain).connect(output);
  brush.start(now, Math.random());
  brush.stop(now + settings.seconds + 0.02);
}

// One note chosen at random from a list of C-major notes, so a pitched sound that plays with the
// music stays in its key (RLG-046). The pop and the water drop are natural sounds and stay free
// (owner, 2026-10-09).
const anyOf = (notes) => notes[Math.floor(Math.random() * notes.length)];

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
  burst.connect(band).connect(burstGain).connect(output);
  burst.start(now, Math.random());
  burst.stop(now + settings.noiseSeconds + 0.02);

  const thump = ctx.createOscillator();
  const thumpGain = ctx.createGain();
  thump.type = "sine";
  thump.frequency.setValueAtTime(settings.thumpStartHz * (1 + pitch), now);
  thump.frequency.exponentialRampToValueAtTime(settings.thumpEndHz, now + settings.thumpSeconds);
  thumpGain.gain.setValueAtTime(settings.thumpVolume, now);
  thumpGain.gain.exponentialRampToValueAtTime(0.0001, now + settings.thumpSeconds);
  thump.connect(thumpGain).connect(output);
  thump.start(now);
  thump.stop(now + settings.thumpSeconds + 0.02);
}

// A water drop for the ripple pond (REQ-032): a short sine whose pitch rises fast, the "plip" of a
// drop on still water, a little different each time, through a low-pass filter that mutes it.
export function drop() {
  if (!canPlay()) return;
  const ctx = ensureContext();
  if (!ctx) return;
  const settings = sounds.drop;
  const now = ctx.currentTime;
  const pitch = 1 + settings.pitchVariation * (Math.random() * 2 - 1);
  const oscillator = ctx.createOscillator();
  const gain = ctx.createGain();
  oscillator.type = "sine";
  oscillator.frequency.setValueAtTime(settings.startHz * pitch, now);
  oscillator.frequency.exponentialRampToValueAtTime(settings.endHz * pitch, now + settings.riseSeconds);
  gain.gain.setValueAtTime(0, now);
  gain.gain.linearRampToValueAtTime(settings.volume, now + 0.005);
  gain.gain.exponentialRampToValueAtTime(0.0001, now + settings.seconds);
  const muffle = ctx.createBiquadFilter();
  muffle.type = "lowpass";
  muffle.frequency.value = settings.lowpassHz;
  oscillator.connect(gain).connect(muffle).connect(output);
  oscillator.start(now);
  oscillator.stop(now + settings.seconds + 0.02);
}

// A rain chime for mandala coloring (owner, 2026-10-08): a small bell struck once. A few sine
// partials at the inharmonic ratios of a struck rod, each fading at its own rate, and a quieter
// second strike a moment later, like a chime touched by rain. `frequency` is the color's note.
export function chime(frequency) {
  if (!canPlay()) return;
  const ctx = ensureContext();
  if (!ctx) return;
  const settings = sounds.chime;
  const strike = (delay, level) => {
    const start = ctx.currentTime + delay;
    for (const [ratio, partLevel, decay] of settings.partials) {
      const oscillator = ctx.createOscillator();
      const gain = ctx.createGain();
      oscillator.type = "sine";
      oscillator.frequency.value = frequency * ratio;
      gain.gain.setValueAtTime(0, start);
      gain.gain.linearRampToValueAtTime(settings.volume * level * partLevel, start + settings.attackSeconds);
      gain.gain.exponentialRampToValueAtTime(0.0001, start + decay);
      oscillator.connect(gain).connect(output);
      oscillator.start(start);
      oscillator.stop(start + decay + 0.05);
    }
  };
  strike(0, 1);
  strike(settings.echoSeconds, settings.echoLevel);
}

// The background rain (owner: an atonal mode, "noise like rain"): looping noise, shaped by a
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
  master.connect(bed);

  const hiss = noise(ctx);
  hiss.loop = true;
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
  hiss.connect(low).connect(high).connect(swell).connect(master);
  hiss.start();
  lfo.start();

  let timer = 0;
  function drop() {
    const now = ctx.currentTime;
    const tick = noise(ctx);
    const band = ctx.createBiquadFilter();
    band.type = "bandpass";
    band.frequency.value = anyOf(settings.dropNotes); // a narrow band has a faint pitch, so it stays in key
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
      if (paused(ctx)) {
        master.disconnect();
        hiss.stop();
        lfo.stop();
        return;
      }
      hold(master.gain, now);
      master.gain.setTargetAtTime(0, now, 0.4);
      hiss.stop(now + 2);
      lfo.stop(now + 2);
      fadingUntil(() => {
        master.disconnect();
        try { hiss.stop(); lfo.stop(); } catch { /* already stopped */ }
      }, 2);
    },
  };
}

// Waves on a shore (RLG-043): looping noise under a low-pass filter. Each wave swells and opens the
// filter as it rises, then breaks and falls back to a quiet trough. The waves come at uneven gaps
// and reach uneven heights, as on a real shore. Noise has no pitch, so it is in every key.
// `level` scales the volume (the Both mix). Returns { stop() }. Silent when sounds are off.
export function waves(level = 1) {
  if (!canPlay()) return { stop: SILENT };
  const ctx = ensureContext();
  if (!ctx) return { stop: SILENT };
  const settings = sounds.waves;
  const master = ctx.createGain();
  master.gain.setValueAtTime(0, ctx.currentTime);
  master.gain.linearRampToValueAtTime(settings.volume * level, ctx.currentTime + settings.fadeInSeconds);
  master.connect(bed);

  const surf = noise(ctx);
  surf.loop = true;
  const high = ctx.createBiquadFilter();
  high.type = "highpass";
  high.frequency.value = settings.highpassHz;
  const low = ctx.createBiquadFilter();
  low.type = "lowpass";
  low.frequency.value = settings.troughHz;
  const swell = ctx.createGain();
  swell.gain.value = settings.troughLevel;
  surf.connect(high).connect(low).connect(swell).connect(master);
  surf.start();

  let timer = 0;
  const between = (min, max) => min + Math.random() * (max - min);
  function wave() {
    const now = ctx.currentTime;
    const seconds = between(settings.minSeconds, settings.maxSeconds);
    const crest = now + seconds * settings.riseShare;
    const height = between(settings.minPeak, 1);
    hold(swell.gain, now);
    swell.gain.linearRampToValueAtTime(height, crest);
    swell.gain.exponentialRampToValueAtTime(settings.troughLevel, now + seconds);
    hold(low.frequency, now);
    low.frequency.exponentialRampToValueAtTime(settings.troughHz + (settings.crestHz - settings.troughHz) * height, crest);
    low.frequency.exponentialRampToValueAtTime(settings.troughHz, now + seconds);
    timer = setTimeout(wave, seconds * 1000);
  }
  wave();

  return {
    stop() {
      clearTimeout(timer);
      const now = ctx.currentTime;
      if (paused(ctx)) {
        master.disconnect();
        surf.stop();
        return;
      }
      hold(master.gain, now);
      master.gain.setTargetAtTime(0, now, 0.4);
      surf.stop(now + 2);
      fadingUntil(() => {
        master.disconnect();
        try { surf.stop(); } catch { /* already stopped */ }
      }, 2);
    },
  };
}
