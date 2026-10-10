// The single source of all user-facing text. Text lives in strings/<lang>.json; this module only
// loads it and fills {placeholders}. English is the only language in the first version (REQ-017).

let table = {};

export async function loadStrings(lang = "en") {
  const response = await fetch(`strings/${lang}.json`);
  if (!response.ok) throw new Error(`strings: HTTP ${response.status}`);
  table = await response.json();
}

// A list of strings.
export function list(key) {
  const value = table[key];
  return Array.isArray(value) ? value : [];
}

// Every data value written into HTML goes through this, even committed config and data (AUD-033).
export function escape(text) {
  return String(text).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
}

export function t(key, values = {}) {
  const text = table[key];
  if (text === undefined) {
    console.warn(`missing string: ${key}`);
    // A key can hold a data value, such as a color name, so it is escaped like data (AUD-033).
    return escape(key);
  }
  return text.replace(/\{(\w+)\}/g, (_, name) => values[name] ?? `{${name}}`);
}
