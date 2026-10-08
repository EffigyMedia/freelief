// The shape trace (REQ-013): a slow, looping shape. The person moves a marker along it with a
// finger, a mouse, or the arrow keys. The marker is a slider (role="slider"), so a screen reader
// reads its position. There is no target, no score and no timer; each full loop is only noted.
// "New shape" moves through many shapes (owner, 2026-10-07), and each shape sings on its own note.

let run = null;

const TAU = Math.PI * 2;

// Each shape is a closed curve, given as a function of t from 0 to 1. Size does not matter: every
// shape is scaled to fit the field.
const SHAPES = {
  eight: (t) => { const a = t * TAU, d = 1 + Math.sin(a) ** 2; return [Math.cos(a) / d, (Math.sin(a) * Math.cos(a)) / d]; },
  circle: (t) => [Math.cos(t * TAU), Math.sin(t * TAU)],
  wave: (t) => polar(t, (a) => 1 + 0.12 * Math.sin(8 * a)),
  flower: (t) => polar(t, (a) => 0.72 + 0.28 * Math.cos(5 * a)),
  star: (t) => polar(t, (a) => 0.6 + 0.4 * ((Math.cos(5 * a) + 1) / 2) ** 2),
  heart: (t) => {
    const a = t * TAU;
    return [16 * Math.sin(a) ** 3, -(13 * Math.cos(a) - 5 * Math.cos(2 * a) - 2 * Math.cos(3 * a) - Math.cos(4 * a))];
  },
  // Turned a quarter, so the dent sits at the top, like a falling petal.
  cardioid: (t) => { const [x, y] = polar(t, (a) => 1 - Math.cos(a)); return [y, -x]; },
  trefoil: (t) => { const a = t * TAU; return [Math.sin(a) + 2 * Math.sin(2 * a), Math.cos(a) - 2 * Math.cos(2 * a)]; },
  lissajous: (t) => [Math.sin(3 * t * TAU + Math.PI / 2), Math.sin(2 * t * TAU)],
  squircle: (t) => {
    const a = t * TAU, c = Math.cos(a), s = Math.sin(a);
    return [Math.sign(c) * Math.abs(c) ** 0.5, Math.sign(s) * Math.abs(s) ** 0.5];
  },
  egg: (t) => { const a = t * TAU; return [Math.cos(a) * (1 + 0.18 * Math.sin(a)), Math.sin(a)]; },
  clover: (t) => polar(t, (a) => 0.55 + 0.45 * Math.abs(Math.cos(2 * a))),
};

function polar(t, radius) {
  const a = t * TAU;
  const r = radius(a);
  return [r * Math.cos(a), r * Math.sin(a)];
}

// Sample a shape and fit it, keeping its proportions, inside the 400 x 240 field with a margin.
function samplePoints(shape, steps) {
  const raw = [];
  for (let i = 0; i <= steps; i++) raw.push(SHAPES[shape](i / steps));
  const xs = raw.map(([x]) => x), ys = raw.map(([, y]) => y);
  const minX = Math.min(...xs), maxX = Math.max(...xs), minY = Math.min(...ys), maxY = Math.max(...ys);
  const scale = Math.min(360 / (maxX - minX), 200 / (maxY - minY));
  const offsetX = 200 - ((minX + maxX) / 2) * scale, offsetY = 120 - ((minY + maxY) / 2) * scale;
  return raw.map(([x, y]) => ({ x: offsetX + x * scale, y: offsetY + y * scale }));
}

export function start(container, ctx) {
  stop();
  const { t, config } = ctx;
  const settings = config.trace;
  const shapes = settings.shapes.filter((shape) => shape.id in SHAPES);

  container.innerHTML = `
    <section class="activity trace">
      <h1>${t("trace.title")}</h1>
      <p class="exercise-intro">${t("trace.intro")}</p>
      <p class="trace-name" aria-live="polite"></p>
      <div class="trace-slider" role="slider" tabindex="0" aria-label="${t("trace.sliderLabel")}"
           aria-valuemin="0" aria-valuemax="100">
        <svg class="trace-field" viewBox="0 0 400 240" aria-hidden="true" focusable="false">
          <path class="trace-shape"></path>
          <path class="trace-done"></path>
          <circle class="trace-marker" r="14"></circle>
        </svg>
      </div>
      <p class="trace-loops" aria-live="polite"></p>
      <div class="exercise-actions">
        <button type="button" class="button new-shape">${t("trace.newShape")}</button>
      </div>
    </section>`;

  const svg = container.querySelector(".trace-field");
  const outline = container.querySelector(".trace-shape");
  const done = container.querySelector(".trace-done");
  const marker = container.querySelector(".trace-marker");
  const slider = container.querySelector(".trace-slider");
  const name = container.querySelector(".trace-name");
  const loopsText = container.querySelector(".trace-loops");
  const current = { shape: -1, points: [], last: 0, index: 0, travelled: 0, loops: 0, dragging: false,
    glass: null };
  run = current;

  function render() {
    const p = current.points[current.index];
    marker.setAttribute("cx", p.x);
    marker.setAttribute("cy", p.y);
    // The trail runs from where this loop began up to the finger, and starts again at each loop
    // (owner, 2026-10-07). The trail path is the shape drawn twice, so a trail can cross the start.
    const start = (current.index - current.travelled + current.last) % current.last;
    done.style.strokeDasharray = `${current.travelled} ${current.last * 2}`;
    done.style.strokeDashoffset = String(-start);
    const percent = Math.round((current.index / current.last) * 100);
    slider.setAttribute("aria-valuenow", String(percent));
    slider.setAttribute("aria-valuetext", t("trace.position", { percent }));
  }

  function showShape(position) {
    if (current.glass) current.glass.stop();
    current.shape = position % shapes.length;
    const shape = shapes[current.shape];
    current.points = samplePoints(shape.id, settings.samples);
    current.last = current.points.length - 1;
    current.index = 0;
    current.travelled = 0;
    current.loops = 0;
    current.glass = ctx.audio.glass(shape.note);
    const d = current.points.map((p, i) => `${i ? "L" : "M"}${p.x.toFixed(1)} ${p.y.toFixed(1)}`).join(" ");
    outline.setAttribute("d", d);
    done.setAttribute("d", d + " " + d.replace(/^M/, "L"));
    done.setAttribute("pathLength", String(current.last * 2));
    name.textContent = t("trace.shapeName", { name: t(`trace.shape.${shape.id}`) });
    loopsText.textContent = "";
    render();
  }

  // Move by a number of sample steps; a full loop forward is noted, gently.
  function move(steps) {
    const last = current.last;
    if (steps !== 0) current.glass.move(Math.abs(steps) / settings.glassFullSpeedSteps);
    current.index = (current.index + steps + last) % last;
    current.travelled += steps;
    if (current.travelled >= last) {
      current.travelled -= last;
      current.loops += 1;
      ctx.audio.play("loop");
      loopsText.textContent = t(current.loops === 1 ? "trace.oneLoop" : "trace.loops", { count: current.loops });
    } else if (current.travelled < 0) {
      current.travelled = 0;
    }
    render();
  }

  // The nearest sample to a pointer, searched only near the marker, so a crossing in a shape
  // cannot make the marker jump to another part of it.
  function nearest(clientX, clientY) {
    const box = svg.getBoundingClientRect();
    const x = ((clientX - box.left) / box.width) * 400;
    const y = ((clientY - box.top) / box.height) * 240;
    let best = 0;
    let bestDistance = Infinity;
    for (let offset = -settings.searchWindow; offset <= settings.searchWindow; offset++) {
      const p = current.points[(current.index + offset + current.last) % current.last];
      const distance = (p.x - x) ** 2 + (p.y - y) ** 2;
      if (distance < bestDistance) { bestDistance = distance; best = offset; }
    }
    return best;
  }

  svg.addEventListener("pointerdown", (event) => {
    current.dragging = true;
    svg.setPointerCapture(event.pointerId);
    move(nearest(event.clientX, event.clientY));
  });
  svg.addEventListener("pointermove", (event) => {
    if (current.dragging) move(nearest(event.clientX, event.clientY));
  });
  const endDrag = () => { current.dragging = false; };
  svg.addEventListener("pointerup", endDrag);
  svg.addEventListener("pointercancel", endDrag);

  slider.addEventListener("keydown", (event) => {
    const step = Math.round((settings.keyStepPercent / 100) * current.last);
    const keys = { ArrowRight: step, ArrowUp: step, ArrowLeft: -step, ArrowDown: -step };
    if (event.key in keys) {
      event.preventDefault();
      move(keys[event.key]);
    }
  });

  container.querySelector(".new-shape").addEventListener("click", () => showShape(current.shape + 1));
  showShape(0);
}

export function stop() {
  if (run && run.glass) run.glass.stop();
  run = null;
}
