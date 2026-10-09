// The ripple pond (REQ-032, owner 2026-10-07): still water; a touch makes soft rings spread from
// that point, and a finger drawn across the water leaves a trail of them. No score, no failure, no
// timer. The pond is one real button, so a key press or a screen reader's activation also makes a
// ripple, at a random place. Under reduced motion the rings only fade; they do not spread (REQ-010).
//
// The rings interfere (RLG-041, owner 2026-10-09). The water is a fine grid of dots in SVG, and each
// dot's brightness is the sum of every ripple's wave at that point: where two crests meet the water
// is brighter, and where a crest meets a trough they cancel and it is fainter. No canvas is used, by
// the architecture rule. The grid is drawn only while a ripple moves, so still water costs nothing.

let run = null;

const SVG_NS = "http://www.w3.org/2000/svg";

// The height of the water at (x, y), `now` seconds on the pond's clock: the sum of one wave packet
// per ripple. A packet is a few crests under a bell-shaped envelope that travels out at `speed`, and
// it fades with time and with distance. Exported so a test can check the sum itself.
export function waveHeight(sources, x, y, now, wave) {
  const k = (2 * Math.PI) / wave.wavelength;
  let height = 0;
  for (const source of sources) {
    const age = now - source.born;
    if (age < 0) continue;
    const r = Math.hypot(x - source.x, y - source.y);
    const offset = r - wave.speed * age;
    const envelope = Math.exp(-(offset * offset) / (2 * wave.packetWidth * wave.packetWidth));
    if (envelope < 0.01) continue;
    const fade = Math.exp(-age / wave.fadeSeconds) / (1 + r / wave.spreadFalloff);
    height += wave.amplitude * fade * envelope * Math.cos(k * offset);
  }
  return height;
}

export function start(container, ctx) {
  stop();
  const { t, config, motion, audio } = ctx;
  const settings = config.ripple;
  const wave = settings.wave;
  const still = motion.reducedMotion();

  container.innerHTML = `
    <section class="activity ripple">
      <h1>${t("ripple.title")}</h1>
      <p class="visually-hidden" id="ripple-intro">${t("ripple.intro")}</p>
      <button type="button" class="pond" aria-label="${t("ripple.pondLabel")}"
              aria-describedby="ripple-intro"></button>
    </section>`;

  const pond = container.querySelector(".pond");
  const current = { timers: [], last: null, fromPointer: false, sources: [], frame: 0, dots: [] };
  run = current;
  const clock = () => performance.now() / 1000;
  // A timer drops its own id when it fires, so the list holds only pending timers (AUD-083).
  function later(callback, ms) {
    const id = setTimeout(() => {
      current.timers = current.timers.filter((pending) => pending !== id);
      callback();
    }, ms);
    current.timers.push(id);
  }

  // The water's grid of dots, laid out again when the pond changes size.
  let field = null;
  function layout() {
    field?.remove();
    current.dots = [];
    if (still) return;
    const width = pond.clientWidth;
    const height = pond.clientHeight;
    field = document.createElementNS(SVG_NS, "svg");
    field.setAttribute("class", "pond-field");
    field.setAttribute("viewBox", `0 0 ${width} ${height}`);
    field.setAttribute("aria-hidden", "true");
    field.setAttribute("focusable", "false");
    const gap = wave.dotSpacing;
    for (let y = gap / 2; y < height; y += gap) {
      for (let x = gap / 2; x < width; x += gap) {
        const dot = document.createElementNS(SVG_NS, "circle");
        dot.setAttribute("cx", x.toFixed(1));
        dot.setAttribute("cy", y.toFixed(1));
        dot.setAttribute("r", wave.dotRadius);
        dot.setAttribute("opacity", wave.restLevel);
        field.append(dot);
        current.dots.push({ x, y, dot, level: wave.restLevel });
      }
    }
    pond.prepend(field);
  }

  function draw() {
    current.frame = 0;
    if (run !== current) return;
    const now = clock();
    const life = settings.lifeSeconds + settings.rings * settings.ringGapSeconds;
    current.sources = current.sources.filter((source) => now - source.born < life);
    for (const point of current.dots) {
      const h = waveHeight(current.sources, point.x, point.y, now, wave);
      const level = Math.min(1, Math.max(0, wave.restLevel + h));
      // Only a visible change is written, so a calm part of the pond costs no work.
      if (Math.abs(level - point.level) < 0.02) continue;
      point.level = level;
      point.dot.setAttribute("opacity", level.toFixed(2));
    }
    // When the last ripple is gone the water is still, and nothing more is drawn.
    if (current.sources.length) current.frame = requestAnimationFrame(draw);
    else current.dots.forEach((point) => { point.level = wave.restLevel; point.dot.setAttribute("opacity", wave.restLevel); });
  }

  function ripple(x, y) {
    if (run !== current) return;
    const sets = pond.querySelectorAll(".ripple-set");
    if (sets.length >= settings.maxRipples) {
      sets[0].remove();
      current.sources.shift();
    }
    // Each ripple keeps a marker at its center: under reduced motion it holds the fading rings.
    const set = document.createElement("span");
    set.className = "ripple-set";
    set.style.left = `${x}px`;
    set.style.top = `${y}px`;
    if (still) {
      for (let i = 0; i < settings.rings; i++) {
        const ring = document.createElement("span");
        ring.className = "ripple-ring still";
        ring.style.animationDuration = `${settings.lifeSeconds}s`;
        ring.style.animationDelay = `${i * settings.ringGapSeconds}s`;
        set.append(ring);
      }
    } else {
      current.sources.push({ x, y, born: clock() });
      if (!current.frame) current.frame = requestAnimationFrame(draw);
    }
    pond.append(set);
    const life = settings.lifeSeconds + settings.rings * settings.ringGapSeconds;
    later(() => set.remove(), life * 1000);
    audio.drop();
  }

  const local = (event) => {
    const box = pond.getBoundingClientRect();
    return { x: event.clientX - box.left, y: event.clientY - box.top };
  };

  pond.addEventListener("pointerdown", (event) => {
    if (event.button !== 0) return;
    pond.setPointerCapture?.(event.pointerId);
    current.fromPointer = true;
    current.last = local(event);
    ripple(current.last.x, current.last.y);
    ctx.haptic("ripple"); // the touch only: the trail of a drag is continuous, so it stays still
  });

  // A finger drawn across the water leaves a ripple every trailSpacing pixels.
  pond.addEventListener("pointermove", (event) => {
    if (!current.last) return;
    const point = local(event);
    if (Math.hypot(point.x - current.last.x, point.y - current.last.y) < settings.trailSpacing) return;
    current.last = point;
    ripple(point.x, point.y);
  });

  const endTrail = () => { current.last = null; };
  pond.addEventListener("pointerup", endTrail);
  pond.addEventListener("pointercancel", () => { endTrail(); current.fromPointer = false; });

  // A key press, or a screen reader's activation, sends a click with no pointer down before it.
  // The click that follows a touch or a drag belongs to that touch, however long it took.
  pond.addEventListener("keydown", () => { current.fromPointer = false; });
  pond.addEventListener("click", () => {
    if (current.fromPointer) {
      current.fromPointer = false;
      return;
    }
    const margin = settings.keyboardMargin;
    const width = Math.max(pond.clientWidth - 2 * margin, 1);
    const height = Math.max(pond.clientHeight - 2 * margin, 1);
    ripple(margin + Math.random() * width, margin + Math.random() * height);
    ctx.haptic("ripple");
  });

  layout();
  // A phone turned on its side, or a resized window: the grid is laid out again.
  let size = [pond.clientWidth, pond.clientHeight];
  current.resize = new ResizeObserver(() => {
    const next = [pond.clientWidth, pond.clientHeight];
    if (next[0] === size[0] && next[1] === size[1]) return;
    size = next;
    layout();
  });
  current.resize.observe(pond);
}

export function stop() {
  if (run) {
    run.timers.forEach(clearTimeout);
    cancelAnimationFrame(run.frame);
    run.resize?.disconnect();
    run = null;
  }
}
