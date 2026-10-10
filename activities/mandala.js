// Mandala coloring (REQ-033, owner 2026-10-07): choose a soft color, then tap a part of the mandala
// to fill it. No score, no failure, no timer, and no end: a new mandala starts blank. The shapes
// are drawn from formulas in config.json, so no image ships. Every part is a focusable button with
// a name ("Ring 2, shape 3 of 8, blank"), so the task works with a keyboard and a screen reader.
// Arrow keys move between parts: left and right around a ring, up and down between rings.

let run = null;

const polar = (r, a) => [r * Math.cos(a - Math.PI / 2), r * Math.sin(a - Math.PI / 2)];
const pt = ([x, y]) => `${x.toFixed(2)} ${y.toFixed(2)}`;

// One path per part of a ring. "petal" is a pointed leaf from the inner to the outer radius;
// "band" is a sector of the ring; "dot" is a circle in the middle of the ring; "scallop" is a
// sector with a rounded outer edge; "diamond" has four straight sides, widest at the middle.
function ringPaths(ring) {
  const step = (2 * Math.PI) / ring.count;
  return [...Array(ring.count).keys()].map((i) => {
    const a = (i + (ring.offset || 0)) * step;
    if (ring.shape === "scallop") {
      const [a0, a1] = [a - step / 2, a + step / 2];
      const edge = ring.inner + (ring.outer - ring.inner) * 0.6;
      return `M${pt(polar(ring.inner, a0))} L${pt(polar(edge, a0))} `
        + `Q${pt(polar(ring.outer * 1.04, a0))} ${pt(polar(ring.outer, a))} `
        + `Q${pt(polar(ring.outer * 1.04, a1))} ${pt(polar(edge, a1))} `
        + `L${pt(polar(ring.inner, a1))} A${ring.inner} ${ring.inner} 0 0 0 ${pt(polar(ring.inner, a0))}Z`;
    }
    if (ring.shape === "diamond") {
      const middle = (ring.inner + ring.outer) / 2;
      const half = step * (ring.width || 0.45);
      return `M${pt(polar(ring.inner, a))} L${pt(polar(middle, a - half))} L${pt(polar(ring.outer, a))} `
        + `L${pt(polar(middle, a + half))}Z`;
    }
    if (ring.shape === "band") {
      const [a0, a1] = [a - step / 2, a + step / 2];
      return `M${pt(polar(ring.inner, a0))} L${pt(polar(ring.outer, a0))} `
        + `A${ring.outer} ${ring.outer} 0 0 1 ${pt(polar(ring.outer, a1))} `
        + `L${pt(polar(ring.inner, a1))} A${ring.inner} ${ring.inner} 0 0 0 ${pt(polar(ring.inner, a0))}Z`;
    }
    if (ring.shape === "dot") {
      const r = (ring.outer - ring.inner) / 2;
      const [x, y] = polar(ring.inner + r, a);
      return `M${pt([x - r, y])} a${r} ${r} 0 1 0 ${2 * r} 0 a${r} ${r} 0 1 0 ${-2 * r} 0Z`;
    }
    const middle = ring.inner + (ring.outer - ring.inner) * 0.55;
    const half = step * (ring.width || 0.45);
    return `M${pt(polar(ring.inner, a))} Q${pt(polar(middle, a - half))} ${pt(polar(ring.outer, a))} `
      + `Q${pt(polar(middle, a + half))} ${pt(polar(ring.inner, a))}Z`;
  });
}

export function start(container, ctx) {
  stop();
  const { t, escape, config, audio } = ctx;
  const settings = config.mandala;
  const current = { design: -1, color: settings.palette[0].name, fills: [], rings: [], focus: [0, 0] };
  run = current;

  container.innerHTML = `
    <section class="activity mandala">
      <h1>${t("mandala.title")}</h1>
      <p class="visually-hidden" id="mandala-intro">${t("mandala.intro")}</p>
      <fieldset class="mandala-palette">
        <legend>${t("mandala.colorLegend")}</legend>
        ${settings.palette.map((swatch, i) => `<label class="swatch">
          <input type="radio" name="mandala-color" value="${escape(swatch.name)}" ${i === 0 ? "checked" : ""}>
          <span class="visually-hidden">${t(`mandala.color.${swatch.name}`)}</span></label>`).join("")}
      </fieldset>
      <svg class="mandala-art" viewBox="-102 -102 204 204" role="group"
           aria-label="${t("mandala.artLabel")}" aria-describedby="mandala-intro"></svg>
      <p class="mandala-status" aria-live="polite"></p>
      <div class="exercise-actions">
        <button type="button" class="button new-mandala">${t("mandala.new")}</button>
      </div>
    </section>`;

  const art = container.querySelector(".mandala-art");
  const status = container.querySelector(".mandala-status");
  const colorOf = (name) => settings.palette.find((swatch) => swatch.name === name);

  function partName(ring, index) {
    const fill = current.fills[ring][index];
    const color = fill ? t(`mandala.color.${fill}`) : t("mandala.blank");
    if (current.rings[ring].center) return t("mandala.center", { color });
    return t("mandala.part", { ring, index: index + 1, total: current.rings[ring].count, color });
  }

  function draw() {
    const [fr, fi] = current.focus;
    art.replaceChildren();
    current.rings.forEach((ring, r) => {
      const paths = ring.center
        ? [`M${-ring.outer} 0 a${ring.outer} ${ring.outer} 0 1 0 ${2 * ring.outer} 0 a${ring.outer} ${ring.outer} 0 1 0 ${-2 * ring.outer} 0Z`]
        : ringPaths(ring);
      paths.forEach((d, i) => {
        const part = document.createElementNS("http://www.w3.org/2000/svg", "path");
        part.setAttribute("d", d);
        part.setAttribute("class", "mandala-part");
        part.setAttribute("role", "button");
        part.setAttribute("aria-label", partName(r, i));
        part.setAttribute("tabindex", r === fr && i === fi ? "0" : "-1");
        part.dataset.ring = String(r);
        part.dataset.index = String(i);
        const fill = current.fills[r][i];
        if (fill) part.style.fill = colorOf(fill).color;
        part.addEventListener("click", () => paint(r, i));
        part.addEventListener("keydown", (event) => key(event, r, i));
        art.append(part);
      });
    });
  }

  const partAt = (r, i) => art.querySelector(`[data-ring="${r}"][data-index="${i}"]`);

  function moveTo(r, i) {
    current.focus = [r, i];
    art.querySelectorAll(".mandala-part").forEach((p) => p.setAttribute("tabindex", "-1"));
    const part = partAt(r, i);
    part.setAttribute("tabindex", "0");
    part.focus();
  }

  function key(event, r, i) {
    const rings = current.rings;
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      paint(r, i);
      return;
    }
    const around = { ArrowRight: 1, ArrowLeft: -1 }[event.key];
    const across = { ArrowUp: 1, ArrowDown: -1 }[event.key];
    if (around !== undefined) {
      event.preventDefault();
      moveTo(r, (i + around + rings[r].count) % rings[r].count);
    } else if (across !== undefined) {
      event.preventDefault();
      const to = Math.min(rings.length - 1, Math.max(0, r + across));
      // Keep the same direction around the circle when moving to a ring with a different count.
      moveTo(to, Math.round((i / rings[r].count) * rings[to].count) % rings[to].count);
    } else if (event.key === "Home" || event.key === "End") {
      event.preventDefault();
      moveTo(event.key === "Home" ? 0 : rings.length - 1, 0);
    }
  }

  function paint(r, i) {
    current.fills[r][i] = current.color;
    current.focus = [r, i];
    // The part just filled is the tab stop, so Tab back into the art returns to it.
    art.querySelectorAll(".mandala-part[tabindex='0']").forEach((p) => p.setAttribute("tabindex", "-1"));
    partAt(r, i).setAttribute("tabindex", "0");
    audio.chime(colorOf(current.color).note); // each color has its own note (owner, 2026-10-08)
    ctx.haptic("fill");
    const part = partAt(r, i);
    part.style.fill = colorOf(current.color).color;
    part.setAttribute("aria-label", partName(r, i));
    status.textContent = partName(r, i);
  }

  function newMandala() {
    current.design = (current.design + 1) % settings.designs.length;
    current.rings = settings.designs[current.design];
    current.fills = current.rings.map((ring) => Array(ring.center ? 1 : ring.count).fill(null));
    current.focus = [0, 0];
    status.textContent = "";
    draw();
  }

  // The page's CSP refuses inline style attributes, so each swatch takes its color from script.
  container.querySelectorAll("input[name=mandala-color]").forEach((input) => {
    input.style.setProperty("--swatch", colorOf(input.value).color);
    input.addEventListener("change", () => {
      current.color = input.value;
      audio.chime(colorOf(input.value).note); // choosing a color sounds its note
    });
  });
  container.querySelector(".new-mandala").addEventListener("click", newMandala);
  newMandala();
}

export function stop() {
  run = null;
}
