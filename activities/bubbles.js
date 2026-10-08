// The bubble field (REQ-012): soft bubbles drift slowly; a tap or a key press pops one, and a new
// one appears a moment later. No score, no failure, no timer. Each bubble is a real button, so
// touch, keyboard and screen reader all reach it. Movement can be paused (WCAG 2.2.2) and stops
// under reduced motion (REQ-010).

let run = null;

export function start(container, ctx) {
  stop();
  const { t, config, motion, audio } = ctx;
  const settings = config.bubbles;
  const still = motion.reducedMotion();

  container.innerHTML = `
    <section class="activity bubbles">
      <h1>${t("bubbles.title")}</h1>
      <p class="visually-hidden">${t("bubbles.intro")}</p>
      <ul class="bubble-field" aria-label="${t("bubbles.fieldLabel")}"></ul>
      <div class="exercise-actions">
        <button type="button" class="button motion-toggle" aria-pressed="false"
                ${still ? "hidden" : ""}>${t("bubbles.pauseMotion")}</button>
      </div>
    </section>`;

  const field = container.querySelector(".bubble-field");
  const toggle = container.querySelector(".motion-toggle");
  const current = { timers: [], paused: false };
  run = current;

  const random = (min, max) => min + Math.random() * (max - min);
  // A timer drops its own id when it fires, so the list holds only pending timers (AUD-038).
  function later(callback, ms) {
    const id = setTimeout(() => {
      current.timers = current.timers.filter((pending) => pending !== id);
      callback();
    }, ms);
    current.timers.push(id);
  }

  // The field is a grid of slots, one bubble per slot, so no bubble ever covers another one's
  // touch target. A bubble sits at a random place inside its slot, with room left to drift.
  const slotCount = settings.columns * settings.rows;
  const used = new Set();

  function freeSlot() {
    const free = [...Array(slotCount).keys()].filter((slot) => !used.has(slot));
    return free.length ? free[Math.floor(Math.random() * free.length)] : -1;
  }

  function addBubble() {
    if (run !== current) return;
    const slot = freeSlot();
    if (slot < 0) return;
    used.add(slot);
    const slotWidth = (field.clientWidth || 320) / settings.columns;
    const slotHeight = (field.clientHeight || 320) / settings.rows;
    const room = Math.min(slotWidth - settings.driftX, slotHeight - settings.driftY);
    const size = Math.round(Math.max(settings.minSize, Math.min(room, random(settings.minSize, settings.maxSize))));
    const item = document.createElement("li");
    item.dataset.slot = String(slot);
    const bubble = document.createElement("button");
    bubble.type = "button";
    bubble.className = "bubble";
    bubble.setAttribute("aria-label", t("bubbles.bubbleLabel"));
    bubble.style.width = `${size}px`;
    bubble.style.height = `${size}px`;
    const column = slot % settings.columns;
    const row = Math.floor(slot / settings.columns);
    item.style.left = `${column * slotWidth + random(0, Math.max(0, slotWidth - size - settings.driftX))}px`;
    item.style.top = `${row * slotHeight + settings.driftY + random(0, Math.max(0, slotHeight - size - settings.driftY))}px`;
    if (!still) {
      bubble.classList.add("drifting");
      bubble.style.animationDuration = `${random(settings.driftSecondsMin, settings.driftSecondsMax)}s`;
      bubble.style.animationDelay = `${-random(0, settings.driftSecondsMax)}s`;
      if (current.paused) bubble.classList.add("held");
    }
    bubble.addEventListener("click", () => pop(item, bubble));
    item.append(bubble);
    field.append(item);
  }

  function pop(item, bubble) {
    if (bubble.classList.contains("popping")) return;
    audio.pop();
    ctx.haptic("pop");
    // Keep keyboard focus in the field: hand it to the next bubble before this one leaves.
    const hadFocus = document.activeElement === bubble;
    const items = [...field.children];
    const neighbour = items[items.indexOf(item) + 1] || items[items.indexOf(item) - 1];
    bubble.classList.add("popping");
    const remove = () => {
      used.delete(Number(item.dataset.slot));
      item.remove();
      if (hadFocus && neighbour && neighbour.isConnected) neighbour.querySelector("button").focus();
    };
    if (still) remove();
    else later(remove, settings.popMs);
    later(addBubble, settings.respawnMs);
    if (hadFocus && still && neighbour) neighbour.querySelector("button").focus();
  }

  toggle.addEventListener("click", () => {
    current.paused = !current.paused;
    toggle.setAttribute("aria-pressed", String(current.paused));
    toggle.textContent = t(current.paused ? "bubbles.resumeMotion" : "bubbles.pauseMotion");
    field.querySelectorAll(".bubble").forEach((b) => b.classList.toggle("held", current.paused));
  });

  for (let i = 0; i < settings.count; i++) addBubble();
}

export function stop() {
  if (run) {
    run.timers.forEach(clearTimeout);
    run = null;
  }
}
