// The shape trace (REQ-013): a slow, looping shape. The person moves a marker along it with a
// finger, a mouse, or the arrow keys. The marker is a slider (role="slider"), so a screen reader
// reads its position. There is no target, no score and no timer; each full loop is only noted.

let run = null;

// A figure eight (a lemniscate), in a 400 x 240 box.
function figureEight(steps) {
  const points = [];
  for (let i = 0; i <= steps; i++) {
    const a = (i / steps) * Math.PI * 2;
    const d = 1 + Math.sin(a) ** 2;
    points.push({ x: 200 + (170 * Math.cos(a)) / d, y: 120 + (170 * Math.sin(a) * Math.cos(a)) / d });
  }
  return points;
}

export function start(container, ctx) {
  stop();
  const { t, config } = ctx;
  const settings = config.trace;
  const points = figureEight(settings.samples);
  const last = points.length - 1;
  const path = points.map((p, i) => `${i ? "L" : "M"}${p.x.toFixed(1)} ${p.y.toFixed(1)}`).join(" ");

  container.innerHTML = `
    <section class="activity trace">
      <h1>${t("trace.title")}</h1>
      <p class="exercise-intro">${t("trace.intro")}</p>
      <div class="trace-slider" role="slider" tabindex="0" aria-label="${t("trace.sliderLabel")}"
           aria-valuemin="0" aria-valuemax="100">
        <svg class="trace-field" viewBox="0 0 400 240" aria-hidden="true" focusable="false">
          <path class="trace-shape" d="${path}"></path>
          <path class="trace-done" d="${path}" pathLength="${last}"></path>
          <circle class="trace-marker" r="14"></circle>
        </svg>
      </div>
      <p class="trace-loops" aria-live="polite"></p>
    </section>`;

  const svg = container.querySelector(".trace-field");
  const done = container.querySelector(".trace-done");
  const marker = container.querySelector(".trace-marker");
  const slider = container.querySelector(".trace-slider");
  const loopsText = container.querySelector(".trace-loops");
  const current = { index: 0, travelled: 0, loops: 0, dragging: false, glass: ctx.audio.glass() };
  run = current;

  function render() {
    const p = points[current.index];
    marker.setAttribute("cx", p.x);
    marker.setAttribute("cy", p.y);
    done.style.strokeDasharray = `${current.index} ${last}`;
    const percent = Math.round((current.index / last) * 100);
    slider.setAttribute("aria-valuenow", String(percent));
    slider.setAttribute("aria-valuetext", t("trace.position", { percent }));
  }

  // Move by a number of sample steps; a full loop forward is noted, gently.
  function move(steps) {
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

  // The nearest sample to a pointer, searched only near the marker, so the crossing in the middle
  // of the eight cannot make the marker jump to the other lobe.
  function nearest(clientX, clientY) {
    const box = svg.getBoundingClientRect();
    const x = ((clientX - box.left) / box.width) * 400;
    const y = ((clientY - box.top) / box.height) * 240;
    let best = 0;
    let bestDistance = Infinity;
    for (let offset = -settings.searchWindow; offset <= settings.searchWindow; offset++) {
      const p = points[(current.index + offset + last) % last];
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
    const step = Math.round((settings.keyStepPercent / 100) * last);
    const keys = { ArrowRight: step, ArrowUp: step, ArrowLeft: -step, ArrowDown: -step };
    if (event.key in keys) {
      event.preventDefault();
      move(keys[event.key]);
    }
  });

  render();
}

export function stop() {
  if (run) run.glass.stop();
  run = null;
}
