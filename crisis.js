// Crisis lines by region. The region comes from the device language setting, or from a region the
// person chooses in Settings, and never from location (REQ-005). Lines are curated and dated in
// data/crisis-lines.json (REQ-022).

let data = null;

// A failed load is not fatal (AUD-002): the help dialog still shows the emergency-number line and
// the directory link from config.json, with no curated lines.
export async function loadCrisisLines() {
  try {
    const response = await fetch("data/crisis-lines.json");
    if (!response.ok) throw new Error(`crisis lines: HTTP ${response.status}`);
    data = await response.json();
  } catch (error) {
    // Kept for a field report of "no lines in urgent help" (AUD-084).
    console.error("Freelief could not load the crisis lines:", error);
    data = null;
  }
}

// The two-letter region of the device, such as "GB" from "en-GB", or null when none is set. Only a
// region the person set counts: a bare "en" is not guessed to be the US (AUD-026), because a wrong
// emergency number is worse than the general route.
export function deviceRegion(languages = navigator.languages || [navigator.language]) {
  for (const tag of languages) {
    try {
      const region = new Intl.Locale(tag).region;
      if (region) return region.toUpperCase();
    } catch {
      // An unreadable language tag is skipped.
    }
  }
  return null;
}

// The region to show first: the one chosen in Settings, or "auto" for the device's own.
export function activeRegion(setting) {
  return setting && setting !== "auto" ? setting : deviceRegion();
}

// Every curated region as { code, country }, in alphabetical order of the country name.
export function regionList() {
  if (!data) return [];
  return Object.entries(data.regions)
    .map(([code, region]) => ({ code, country: region.country }))
    .sort((a, b) => a.country.localeCompare(b.country));
}

// The lines for one region (null when it is not curated) and the international directory.
export function linesFor(regionCode) {
  if (!data) return { own: null, directory: null };
  const regions = data.regions;
  const own = regionCode && Object.hasOwn(regions, regionCode) ? { code: regionCode, ...regions[regionCode] } : null;
  return { own, directory: data.directory };
}
