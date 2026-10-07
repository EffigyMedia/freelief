// Crisis lines by region. The region comes from the device language setting, never from
// location (REQ-005). Lines are curated and dated in data/crisis-lines.json (REQ-022).

let data = null;

export async function loadCrisisLines() {
  const response = await fetch("data/crisis-lines.json");
  data = await response.json();
}

// The two-letter region of the device, such as "GB" from "en-GB", or null when none is set.
export function deviceRegion(languages = navigator.languages || [navigator.language]) {
  for (const tag of languages) {
    try {
      const region = new Intl.Locale(tag).maximize().region;
      if (region) return region.toUpperCase();
    } catch {
      // An unreadable language tag is skipped.
    }
  }
  return null;
}

// The lines for one region, the other curated regions, and the international directory.
export function linesFor(regionCode) {
  const regions = data.regions;
  const own = regionCode && regions[regionCode] ? { code: regionCode, ...regions[regionCode] } : null;
  const others = Object.entries(regions)
    .filter(([code]) => code !== regionCode)
    .map(([code, region]) => ({ code, ...region }));
  return { own, others, directory: data.directory };
}
