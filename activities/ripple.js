// The ripple pond (REQ-032, owner 2026-10-07): still water; a touch makes soft rings spread from
// that point, and a finger drawn across the water leaves a trail of them. No score, no failure, no
// timer. The pond is one real button, so a key press or a screen reader's activation also makes a
// ripple, at a random place. Under reduced motion the rings only fade; they do not spread (REQ-010).

let run = null;

export function start(container, ctx) {
  stop();
  const { t, config, motion, audio } = ctx;
  const settings = config.ripple;
  const still = motion.reducedMotion();

  container.innerHTML = `
    <section class="activity ripple">
      <h1>${t("ripple.title")}</h1>
      <p class="visually-hidden" id="ripple-intro">${t("ripple.intro")}</p>
      <button type="button" class="pond" aria-label="${t("ripple.pondLabel")}"
              aria-describedby="ripple-intro"></button>
    </section>`;

  const pond = container.querySelector(".pond");
  const current = { timers: [], last: null, fromPointer: false };
  run = current;

  function ripple(x, y) {
    if (run !== current) return;
    const sets = pond.querySelectorAll(".ripple-set");
    if (sets.length >= settings.maxRipples) sets[0].remove();
    const set = document.createElement("span");
    set.className = "ripple-set";
    set.style.left = `${x}px`;
    set.style.top = `${y}px`;
    for (let i = 0; i < settings.rings; i++) {
      const ring = document.createElement("span");
      ring.className = still ? "ripple-ring still" : "ripple-ring";
      ring.style.animationDuration = `${settings.lifeSeconds}s`;
      ring.style.animationDelay = `${i * settings.ringGapSeconds}s`;
      set.append(ring);
    }
    pond.append(set);
    const life = settings.lifeSeconds + settings.rings * settings.ringGapSeconds;
    current.timers.push(setTimeout(() => set.remove(), life * 1000));
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
}

export function stop() {
  if (run) {
    run.timers.forEach(clearTimeout);
    run = null;
  }
}
