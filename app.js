// The shell: the page frame, the screen router, the footer and the "Need urgent help?" control.
// It holds no exercise logic and no literal text (AGENTS.md, Architecture).

import { loadStrings, t, list } from "./strings.js";
import { loadCrisisLines, activeRegion, linesFor, regionList } from "./crisis.js";
import { initSettings, getSetting, setSetting, onSettingChange } from "./settings.js";
import { initHaptics, pulse as haptic } from "./haptics.js";
import { keepAwake } from "./wakelock.js";
import * as audio from "./audio.js";
import * as background from "./background.js";
import * as motion from "./motion.js";
import * as menu from "./screens/menu.js";

// The screens the router knows. The menu is the default and the first screen (REQ-018, changed by
// the owner 2026-10-07), so it loads with the shell. Every other screen loads on its first visit
// (RLG-006): the browser then parses only what the first screen needs before it draws. The service
// worker caches them all, so a later visit works offline.
const ROUTES = {
  menu: () => Promise.resolve(menu),
  breathe: () => import("./exercises/breathe.js"),
  bubbles: () => import("./activities/bubbles.js"),
  trace: () => import("./activities/trace.js"),
  unblock: () => import("./activities/unblock.js"),
  ripple: () => import("./activities/ripple.js"),
  mandala: () => import("./activities/mandala.js"),
  calm: () => import("./activities/calm.js"),
  settings: () => import("./screens/settings.js"),
  about: () => import("./screens/about.js"),
  standards: () => import("./screens/standards.js"),
  feedback: () => import("./screens/feedback.js"),
};
const DEFAULT_ROUTE = "menu";
// On these screens the footer shows only its calm line, so the exercise has the room (design review,
// owner 2026-10-08). The menu and the info pages keep the full footer and its links.
const QUIET_FOOTER = new Set(["breathe", "bubbles", "trace", "unblock", "ripple", "mandala", "calm"]);

let config = null;
let current = null;
let main = null;
let backLink = null;
let nav = null;
let footer = null;
let soundBar = null;

async function loadConfig() {
  const response = await fetch("config.json");
  if (!response.ok) throw new Error(`config: HTTP ${response.status}`);
  return response.json();
}

function element(tag, attributes = {}, children = []) {
  const node = document.createElement(tag);
  for (const [name, value] of Object.entries(attributes)) {
    if (name === "text") node.textContent = value;
    else node.setAttribute(name, value);
  }
  for (const child of [].concat(children)) if (child) node.append(child);
  return node;
}

// ---- urgent help -------------------------------------------------------------------------

const dial = (number) => number.replace(/[^\d+]/g, "");

function lineCard(line) {
  const actions = element("div", { class: "line-actions" });
  if (line.call) actions.append(element("a", { class: "button", href: `tel:${dial(line.call)}`, text: t("help.call", { number: line.call }) }));
  if (line.text) actions.append(element("a", { class: "button", href: `sms:${dial(line.text)}`, text: t("help.text", { number: line.text }) }));
  if (line.web) actions.append(element("a", { class: "button", href: line.web, rel: "noopener", text: t("help.chat") }));
  // Calls and texts work offline; a web chat does not, so it says so (AUD-052).
  const webNote = line.web ? element("p", { class: "line-checked", text: t("help.chatNote") }) : null;
  return element("li", { class: "line" }, [
    element("h4", { text: line.name }),
    element("p", { class: "line-hours", text: line.hours }),
    actions,
    webNote,
    element("p", { class: "line-checked", text: t("help.checked", { date: line.checked }) }),
  ]);
}

function regionBlock(region, headingLevel) {
  return element("section", { class: "region", "data-region": region.code }, [
    element(headingLevel, { text: region.country }),
    element("ul", { class: "lines" }, region.lines.map(lineCard)),
  ]);
}

// The dialog opens on the region chosen in Settings, or the device's own. A country list replaces
// the long list of every region (owner, 2026-10-07); a choice in it holds for this visit only.
function buildHelpDialog() {
  const dialog = element("dialog", { class: "help", id: "help", "aria-labelledby": "help-title" });
  // The way out sits at the top and stays there while the content scrolls (owner, on the phone:
  // a Close button at the bottom of a long list was not found).
  const back = element("button", { type: "button", class: "button help-back", text: t("help.back") });
  back.addEventListener("click", () => dialog.close());
  const header = element("div", { class: "help-header" }, [
    element("h2", { id: "help-title", text: t("help.title") }),
    back,
  ]);

  // A new country changes the emergency number, so a screen reader hears it (web-interface-review).
  const emergency = element("p", { class: "emergency", "aria-live": "polite" });
  // The emergency number is the first thing to tap, not only to read (design review, 2026-10-08).
  // The numbers come from the region's own emergency text, so "112 or 999" gives two buttons.
  const emergencyCalls = element("div", { class: "emergency-calls" });
  const lines = element("div", { class: "region-lines" });
  const regions = regionList();
  const select = element("select", { id: "help-country", class: "country-select" }, [
    ...regions.map((region) => element("option", { value: region.code, text: region.country })),
    element("option", { value: "", text: t("help.otherCountry") }),
  ]);
  const picker = regions.length
    ? element("p", { class: "country-picker" }, [
      element("label", { for: "help-country", text: t("help.country") }), select])
    : null;

  // The region shown now. Opening help on the same region again draws nothing, so the dialog opens
  // with the least work: it is the never-break response of REQ-027 (AUD-115).
  let shown;
  function showRegion(code) {
    if (code === shown) return;
    shown = code;
    const { own } = linesFor(code);
    emergency.textContent = own
      ? t("help.emergency", { number: own.emergency })
      : t("help.emergencyUnknown");
    emergencyCalls.replaceChildren(...(own ? (own.emergency.match(/\d+/g) || []) : []).map((number) =>
      element("a", { class: "button primary emergency-call", href: `tel:${number}`, text: t("help.call", { number }) })));
    lines.replaceChildren(...(own ? [regionBlock(own, "h3")] : []));
    select.value = own ? own.code : "";
  }
  select.addEventListener("change", () => showRegion(select.value));

  // With no crisis data, the directory link still comes from config.json (AUD-002).
  const { directory } = linesFor(null);
  const directoryUrl = directory ? directory.url : config.crisis.directoryUrl;
  const body = [
    element("p", { text: t("help.intro") }),
    picker,
    emergency,
    emergencyCalls,
    lines,
    element("p", { class: "directory" }, [
      element("a", { class: "button", href: directoryUrl, rel: "noopener", text: t("help.directory") }),
      directory
        ? element("span", { class: "directory-note", text: t("help.directoryNote", { note: directory.note }) })
        : null,
    ]),
  ];
  dialog.append(header, element("div", { class: "help-body" }, body));
  showRegion(activeRegion(getSetting("helpRegion")));
  return { dialog, showRegion };
}

// ---- frame and router --------------------------------------------------------------------

function buildShell() {
  const helpButton = element("button", {
    type: "button", class: "button help-open", "aria-haspopup": "dialog", text: t("help.open"),
  });
  // Settings is a gear, always at the top right (owner, 2026-10-07). The icon is inline SVG, so no
  // file ships, and the link carries the accessible name.
  const gear = element("a", { class: "gear", href: "#settings", "aria-label": t("nav.settings") });
  gear.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M19.4 13.5a7.6 7.6 0 0 0 0-3l2-1.6-2-3.4-2.4 1a7.4 7.4 0 0 0-2.6-1.5L14 2.5h-4l-.4 2.5A7.4 7.4 0 0 0 7 6.5l-2.4-1-2 3.4 2 1.6a7.6 7.6 0 0 0 0 3l-2 1.6 2 3.4 2.4-1a7.4 7.4 0 0 0 2.6 1.5l.4 2.5h4l.4-2.5a7.4 7.4 0 0 0 2.6-1.5l2.4 1 2-3.4-2-1.6Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>';
  // Sound on or off, one tap from every screen (owner, 2026-10-08): a speaker, crossed out when
  // off. It is a toggle button with a fixed name, so a screen reader says "Sound, pressed".
  const soundButton = element("button", {
    type: "button", class: "sound-toggle", "aria-label": t("nav.sound"),
    "aria-pressed": String(getSetting("sounds")),
  });
  soundButton.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><g class="sound-waves" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M15.5 9a4 4 0 0 1 0 6"/><path d="M18 6.5a7.5 7.5 0 0 1 0 11"/></g><g class="sound-cross" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M15.5 9.5l5 5"/><path d="M20.5 9.5l-5 5"/></g></svg>';
  soundButton.addEventListener("click", () => setSetting("sounds", !getSetting("sounds")));
  onSettingChange((name, value) => {
    // Only a choice on the Visualizer starts a sound; Off or Stop ends it from anywhere. A reset in
    // Settings changes the stored choice and leaves what plays alone (AUD-114).
    if (name === "calmMode" && (value === "off" || main.dataset.screen === "calm")) background.play(value);
    if (name === "natureSound") background.setNature(value);
    if (name !== "sounds") return;
    soundButton.setAttribute("aria-pressed", String(value));
    audio.applySound(value);
    // While sound is off every sound is silent, so the background starts again when it returns.
    background.restart();
    showSoundBar();
    current?.soundChanged?.(value);
  });
  const header = element("header", { class: "top" }, [
    // Plain text, not a link: "Need urgent help?" stays the first stop for the Tab key.
    element("p", { class: "brand", translate: "no", text: t("app.name") }),
    element("div", { class: "top-actions" }, [helpButton, soundButton, gear]),
  ]);
  // The sound bar (RLG-045, owner 2026-10-09): while music or nature plays, every screen but the
  // Visualizer says what plays, with a Stop button. Stop is the same as Off in the Visualizer.
  const soundBarText = element("p", { class: "sound-bar-text", id: "sound-bar-text" });
  const stopButton = element("button", {
    type: "button", class: "button sound-bar-stop", "aria-describedby": "sound-bar-text", text: t("soundBar.stop"),
  });
  stopButton.addEventListener("click", () => {
    setSetting("calmMode", "off");
    // The bar goes away, so focus moves to the screen's heading rather than being lost.
    const heading = main.querySelector("h1");
    if (heading) {
      heading.setAttribute("tabindex", "-1");
      heading.focus();
    }
  });
  // It sits in the header, so it is inside a landmark and stays in sight as the page scrolls.
  soundBar = element("div", { class: "sound-bar", hidden: "" }, [soundBarText, stopButton]);
  header.append(soundBar);
  background.onChange(showSoundBar);
  main = element("main", { id: "screen" });
  // Every screen goes back to the menu, from the top of the screen (owner, 2026-10-07).
  backLink = element("a", { class: "button nav-link nav-back", href: "#menu", text: t("nav.backMenu") });
  nav = element("nav", { class: "screen-nav", "aria-label": t("nav.label") }, [backLink]);
  const footerLinks = element("ul", { class: "footer-links" }, [
    ["#about", "footer.about"], ["#standards", "footer.standards"], ["#feedback", "footer.feedback"],
  ].map(([href, key]) => element("li", {}, [element("a", { class: "footer-link", href, text: t(key) })])));
  footer = element("footer", { class: "bottom" }, [
    element("p", { class: "tagline", text: t("app.tagline") }),
    element("p", { class: "self-help", text: t("footer.selfHelp") }),
    element("nav", { "aria-label": t("footer.label") }, [footerLinks]),
  ]);
  const { dialog, showRegion } = buildHelpDialog();
  // The phone's back gesture closes the dialog instead of leaving the app: opening it adds a
  // history entry, and going back closes it.
  helpButton.addEventListener("click", () => {
    showRegion(activeRegion(getSetting("helpRegion")));
    // Nothing plays over the crisis lines (AUD-074): sound waits until help closes, and the
    // background loops stop, so nothing queues up meanwhile (AUD-113).
    audio.applySound(false);
    background.hold();
    dialog.showModal();
    // A modal dialog blocks taps on the page, but on a phone a swipe on the backdrop still scrolls
    // the page under it (owner report). The page does not scroll while help is open.
    document.documentElement.classList.add("help-is-open");
    history.pushState({ freeliefHelp: true }, "");
  });
  window.addEventListener("popstate", () => { if (dialog.open) dialog.close(); });
  dialog.addEventListener("close", () => {
    document.documentElement.classList.remove("help-is-open");
    if (getSetting("sounds")) {
      audio.applySound(true);
      background.restart();
    }
    if (history.state?.freeliefHelp) history.back();
  });
  document.body.replaceChildren(header, nav, main, footer, dialog);
}

function showSoundBar() {
  const mode = background.current();
  const nature = t(`soundBar.nature.${background.natureSound()}`);
  soundBar.hidden = mode === "off" || !getSetting("sounds") || main.dataset.screen === "calm";
  if (!soundBar.hidden) soundBar.querySelector(".sound-bar-text").textContent = t(`soundBar.${mode}`, { nature });
}

function routeName() {
  const name = location.hash.replace(/^#/, "");
  // With no address, Freelief opens where Settings says: the menu, or breathing (owner, 2026-10-08).
  if (!name) return getSetting("openOn") === "breathe" ? "breathe" : DEFAULT_ROUTE;
  // Own names only: a hash such as #constructor is not a screen (AUD-005).
  return Object.hasOwn(ROUTES, name) ? name : DEFAULT_ROUTE;
}

let showing = 0;

async function show(name, { moveFocus }) {
  if (current) current.stop();
  current = null;
  const request = ++showing;
  main.dataset.screen = name;
  delete main.dataset.shown;
  // A screen with its own tones lowers the background sound under them (RLG-045).
  audio.duck(config.calm.duckRoutes.includes(name));
  showSoundBar();
  let screen;
  try {
    screen = await ROUTES[name]();
  } catch (error) {
    // A screen that cannot load (offline with a damaged cache) falls back to the menu, which loads
    // with the shell, so the person is never left on a blank or frozen screen.
    console.error(`Freelief could not load the ${name} screen:`, error);
    if (name !== DEFAULT_ROUTE) {
      // The address names the screen shown, so the failed screen's link works again (AUD-057).
      history.replaceState(history.state, "", `#${DEFAULT_ROUTE}`);
      return show(DEFAULT_ROUTE, { moveFocus });
    }
    throw error;
  }
  if (request !== showing) return;
  current = screen;
  // The old screen goes first, so a slow or failed start never leaves a frozen copy of it (AUD-008).
  main.replaceChildren();
  // A screen may load data first (Standards and research), so wait for it before focusing.
  try {
    await current.start(main, {
      t, list, config, motion, audio, haptic, keepAwake, rhythm: getSetting("rhythm"), soundsOn: getSetting("sounds"),
      // Activities never touch Settings themselves (AUD-066): the shell hands over the Visualizer's
      // sound choice and saves a new one.
      calmMode: getSetting("calmMode"), saveCalmMode: (mode) => setSetting("calmMode", mode),
      // The Visualizer starts the background sound it last chose, unless something already plays.
      startBackground: () => { if (background.current() === "off") background.play(getSetting("calmMode")); },
    });
  } catch (error) {
    // A screen that fails as it starts falls back to the menu, as a screen that cannot load does.
    console.error(`Freelief could not start the ${name} screen:`, error);
    if (request !== showing) return;
    current = null;
    if (name !== DEFAULT_ROUTE) {
      history.replaceState(history.state, "", `#${DEFAULT_ROUTE}`);
      return show(DEFAULT_ROUTE, { moveFocus });
    }
    throw error;
  }
  if (request !== showing) return;
  main.dataset.shown = name;
  nav.hidden = name === "menu";
  footer.classList.toggle("quiet", QUIET_FOOTER.has(name));
  if (moveFocus) {
    // Tell keyboard and screen-reader users where they are: focus the new screen's heading.
    const heading = main.querySelector("h1");
    if (heading) {
      heading.setAttribute("tabindex", "-1");
      heading.focus();
    }
  }
}

function applyTheme(theme) {
  if (theme === "system") delete document.documentElement.dataset.theme;
  else document.documentElement.dataset.theme = theme;
}

// If config.json, the strings or a module cannot load, the static fallback in index.html stays on
// screen: a breathing line, the emergency instruction and the directory link (AUD-002). The shell
// replaces it only once it can draw everything.
async function boot() {
  const [loaded] = await Promise.all([loadConfig(), loadStrings("en"), loadCrisisLines()]);
  config = loaded;
  initSettings(config);
  audio.initAudio(config);
  background.initBackground(config, getSetting("natureSound"));
  // A browser plays nothing before the first tap or key press. If the Visualizer was opened before
  // one, its sound starts at that first gesture, so the sound bar never names a silent sound.
  const firstGesture = () => {
    window.removeEventListener("pointerdown", firstGesture, true);
    window.removeEventListener("keydown", firstGesture, true);
    if (background.current() !== "off") background.restart();
  };
  window.addEventListener("pointerdown", firstGesture, true);
  window.addEventListener("keydown", firstGesture, true);
  initHaptics(config);
  applyTheme(getSetting("theme"));
  onSettingChange((name, value) => { if (name === "theme") applyTheme(value); });
  document.title = t("app.name");
  buildShell();
  // Listen before the first screen, so a first screen that fails still leaves working links (AUD-008).
  window.addEventListener("hashchange", () => show(routeName(), { moveFocus: true }));
  await show(routeName(), { moveFocus: false });
  // Silence while Freelief is out of sight, for example during a call to a line (AUD-074).
  document.addEventListener("visibilitychange", () => {
    const helpOpen = document.querySelector("dialog.help")?.open;
    if (document.visibilityState === "hidden") {
      audio.applySound(false);
      background.hold();
    } else if (getSetting("sounds") && !helpOpen) {
      audio.applySound(true);
      background.restart();
    }
  });
  document.documentElement.dataset.ready = "true";
  performance.mark("freelief-ready");
  keepOfflineCopy();
}

// Ask the browser to keep the offline copy under storage pressure (AUD-080), so Freelief still
// opens offline on a full phone. Chromium and Safari decide without a question. Firefox asks the
// person, and Freelief opens with no question or notice (REQ-018), so it is not asked there. The
// call never holds up the start.
function keepOfflineCopy() {
  if (!navigator.storage?.persist || /Firefox\//.test(navigator.userAgent)) return;
  navigator.storage.persisted()
    .then((kept) => (kept ? true : navigator.storage.persist()))
    .catch(() => {});
}

// Another app on the shared origin may have deleted Freelief's offline cache (AUD-001). On each
// launch while online, ask the worker to fetch any file the cache is missing.
async function healOfflineCache() {
  if (!navigator.onLine) return;
  // The worker replies whether the repair worked (AUD-060). A failure is logged for a field report;
  // the app still runs, and the next online launch tries again.
  navigator.serviceWorker.addEventListener("message", (event) => {
    if (event.data && event.data.heal === false) console.warn("Freelief could not repair its offline copy.");
  });
  const registration = await navigator.serviceWorker.ready;
  if (registration.active) registration.active.postMessage("heal");
}

// A new version waits after it installs (sw.js). Before the person has touched anything, the page
// lets it take over and reloads once, so they get the new version at once and never a page built
// from two versions. Once they have touched or typed, the new version waits for the next open, and
// this page keeps the version it started with, files and all (AUD-057).
if ("serviceWorker" in navigator) {
  const hadController = Boolean(navigator.serviceWorker.controller);
  let interacted = false;
  let reloaded = false;
  const touched = () => { interacted = true; };
  window.addEventListener("pointerdown", touched, { capture: true, once: true });
  window.addEventListener("keydown", touched, { capture: true, once: true });
  // A breathing screen that runs counts as in use, even before a touch: with "Start breathing at
  // once" a reload would restart the breath the person is following (AUD-107).
  const inUse = () => interacted || document.querySelector("main")?.dataset.screen === "breathe";
  const offerTakeover = (worker) => {
    if (worker && hadController && !inUse()) worker.postMessage("skip");
  };
  navigator.serviceWorker.addEventListener("controllerchange", () => {
    if (hadController && !inUse() && !reloaded) {
      reloaded = true;
      location.reload();
    }
  });
  // The update check fetches sw.js and the version.js it imports past the HTTP cache, so a new version
  // is seen at once under GitHub Pages' ten-minute caching (AUD-013).
  navigator.serviceWorker.register("sw.js", { updateViaCache: "none" })
    .then((registration) => {
      // A browser that blocks workers (a test, a strict setting) gives no registration.
      if (!registration) return undefined;
      offerTakeover(registration.waiting);
      registration.addEventListener("updatefound", () => {
        const worker = registration.installing;
        worker?.addEventListener("statechange", () => {
          if (worker.state === "installed") offerTakeover(worker);
        });
      });
      return healOfflineCache();
    })
    .catch((error) => {
      // Offline support is lost, but the app still works online. The reason is kept for a field
      // report (AUD-085).
      console.error("Freelief could not install its offline copy:", error);
    });
}

// The static fallback in index.html, kept before the shell replaces the page, so a failure after
// the shell is built can still put it back (AUD-002).
const staticFallback = document.getElementById("fallback");

boot().catch((error) => {
  // Keep the reason, so a field report can be debugged; the fallback is shown.
  console.error("Freelief could not start:", error);
  if (staticFallback && !staticFallback.isConnected) document.body.replaceChildren(staticFallback);
  document.documentElement.dataset.ready = "fallback";
  document.documentElement.classList.remove("hide-fallback");
});
