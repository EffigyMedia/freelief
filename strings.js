// The single source of all user-facing text. Text lives in strings/<lang>.json; this module only
// loads it and fills {placeholders}. English is the only language in the first version (REQ-017).

let table = {};

export async function loadStrings(lang = "en") {
  const response = await fetch(`strings/${lang}.json`);
  table = await response.json();
}

// A list of strings, such as the calming statements.
export function list(key) {
  const value = table[key];
  return Array.isArray(value) ? value : [];
}

export function t(key, values = {}) {
  const text = table[key];
  if (text === undefined) {
    console.warn(`missing string: ${key}`);
    return key;
  }
  return text.replace(/\{(\w+)\}/g, (_, name) => values[name] ?? `{${name}}`);
}
