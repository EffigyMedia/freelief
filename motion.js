// Reduced-motion detection. Every animation asks this module before it moves (REQ-010).

const query = window.matchMedia("(prefers-reduced-motion: reduce)");

export function reducedMotion() {
  return query.matches;
}

export function onMotionChange(callback) {
  query.addEventListener("change", () => callback(query.matches));
}
