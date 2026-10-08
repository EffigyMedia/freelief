// The shell: the page frame, the screen router, the footer and the "Need urgent help?" control.
// It holds no exercise logic and no literal text (AGENTS.md, Architecture).

import { loadStrings, t, list } from "./strings.js";
import { loadCrisisLines, deviceRegion, linesFor } from "./crisis.js";
import { initSettings, getSetting, onSettingChange } from "./settings.js";
import * as audio from "./audio.js";
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
  sort: () => import("./activities/sort.js"),
  ripple: () => import("./activities/ripple.js"),
  calm: () => import("./activities/calm.js"),
  settings: () => import("./screens/settings.js"),
  about: () => import("./screens/about.js"),
  standards: () => import("./screens/standards.js"),
  feedback: () => import("./screens/feedback.js"),
};
const DEFAULT_ROUTE = "menu";

let config = null;
let current = null;
let main = null;
let backLink = null;
let nav = null;

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
  return element("li", { class: "line" }, [
    element("h3", { text: line.name }),
    element("p", { class: "line-hours", text: line.hours }),
    actions,
    element("p", { class: "line-checked", text: t("help.checked", { date: line.checked }) }),
  ]);
}

function regionBlock(region, headingLevel) {
  return element("section", { class: "region", "data-region": region.code }, [
    element(headingLevel, { text: region.country }),
    element("ul", { class: "lines" }, region.lines.map(lineCard)),
  ]);
}

function buildHelpDialog() {
  const { own, others, directory } = linesFor(deviceRegion());
  const dialog = element("dialog", { class: "help", id: "help", "aria-labelledby": "help-title" });
  // The way out sits at the top and stays there while the content scrolls (owner, on the phone:
  // a Close button at the bottom of a long list was not found).
  const back = element("button", { type: "button", class: "button help-back", text: t("help.back") });
  back.addEventListener("click", () => dialog.close());
  const header = element("div", { class: "help-header" }, [
    element("h2", { id: "help-title", text: t("help.title") }),
    back,
  ]);

  const body = [
    element("p", { text: t("help.intro") }),
    element("p", { class: "emergency", text: own
      ? t("help.emergency", { number: own.emergency })
      : t("help.emergencyUnknown") }),
  ];
  if (own) body.push(regionBlock(own, "h3"));
  // With no crisis data, the directory link still comes from config.json (AUD-002).
  const directoryUrl = directory ? directory.url : config.crisis.directoryUrl;
  body.push(element("p", { class: "directory" }, [
    element("a", { class: "button", href: directoryUrl, rel: "noopener", text: t("help.directory") }),
    directory
      ? element("span", { class: "directory-note", text: t("help.directoryNote", { note: directory.note }) })
      : null,
  ]));
  if (others.length) {
    body.push(element("details", { class: "others" }, [
      element("summary", { text: t("help.otherCountries") }),
      ...others.map((region) => regionBlock(region, "h3")),
    ]));
  }
  dialog.append(header, element("div", { class: "help-body" }, body));
  return dialog;
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
  const header = element("header", { class: "top" }, [
    // Plain text, not a link: "Need urgent help?" stays the first stop for the Tab key.
    element("p", { class: "brand", text: t("app.name") }),
    element("div", { class: "top-actions" }, [helpButton, gear]),
  ]);
  main = element("main", { id: "screen" });
  // Every screen goes back to the menu, from the top of the screen (owner, 2026-10-07).
  backLink = element("a", { class: "button nav-link nav-back", href: "#menu", text: t("nav.backMenu") });
  nav = element("nav", { class: "screen-nav", "aria-label": t("nav.label") }, [backLink]);
  const footerLinks = element("ul", { class: "footer-links" }, [
    ["#about", "footer.about"], ["#standards", "footer.standards"], ["#feedback", "footer.feedback"],
  ].map(([href, key]) => element("li", {}, [element("a", { class: "footer-link", href, text: t(key) })])));
  const footer = element("footer", { class: "bottom" }, [
    element("p", { class: "tagline", text: t("app.tagline") }),
    element("p", { class: "self-help", text: t("footer.selfHelp") }),
    element("nav", { "aria-label": t("footer.label") }, [footerLinks]),
  ]);
  const dialog = buildHelpDialog();
  // The phone's back gesture closes the dialog instead of leaving the app: opening it adds a
  // history entry, and going back closes it.
  helpButton.addEventListener("click", () => {
    dialog.showModal();
    history.pushState({ freeliefHelp: true }, "");
  });
  window.addEventListener("popstate", () => { if (dialog.open) dialog.close(); });
  dialog.addEventListener("close", () => { if (history.state?.freeliefHelp) history.back(); });
  document.body.replaceChildren(header, nav, main, footer, dialog);
}

function routeName() {
  const name = location.hash.replace(/^#/, "");
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
  let screen;
  try {
    screen = await ROUTES[name]();
  } catch (error) {
    // A screen that cannot load (offline with a damaged cache) falls back to breathing, which is
    // always loaded, so the person is never left on a blank or frozen screen.
    console.error(`Freelief could not load the ${name} screen:`, error);
    if (name !== DEFAULT_ROUTE) return show(DEFAULT_ROUTE, { moveFocus });
    throw error;
  }
  if (request !== showing) return;
  current = screen;
  // A screen may load data first (Standards and research), so wait for it before focusing.
  await current.start(main, {
    t, list, config, motion, audio, rhythm: getSetting("rhythm"), soundsOn: getSetting("sounds"),
  });
  if (request !== showing) return;
  main.dataset.shown = name;
  nav.hidden = name === "menu";
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
  applyTheme(getSetting("theme"));
  onSettingChange((name, value) => { if (name === "theme") applyTheme(value); });
  document.title = t("app.name");
  buildShell();
  await show(routeName(), { moveFocus: false });
  window.addEventListener("hashchange", () => show(routeName(), { moveFocus: true }));
  document.documentElement.dataset.ready = "true";
  performance.mark("freelief-ready");
}

// Another app on the shared origin may have deleted Freelief's offline cache (AUD-001). On each
// launch while online, ask the worker to fetch any file the cache is missing.
async function healOfflineCache() {
  if (!navigator.onLine) return;
  const registration = await navigator.serviceWorker.ready;
  if (registration.active) registration.active.postMessage("heal");
}

// When a new version's worker takes over before the person has touched anything, reload once, so
// they get the new version at once and never a page built from two versions. Once they have
// touched or typed, never interrupt them: the new version then applies at the next open.
if ("serviceWorker" in navigator) {
  const hadController = Boolean(navigator.serviceWorker.controller);
  let interacted = false;
  let reloaded = false;
  const touched = () => { interacted = true; };
  window.addEventListener("pointerdown", touched, { capture: true, once: true });
  window.addEventListener("keydown", touched, { capture: true, once: true });
  navigator.serviceWorker.addEventListener("controllerchange", () => {
    if (hadController && !interacted && !reloaded) {
      reloaded = true;
      location.reload();
    }
  });
}

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("sw.js")
    .then(healOfflineCache)
    .catch(() => {
      // Offline support is lost, but the app still works online.
    });
}

boot().catch((error) => {
  // Keep the reason, so a field report can be debugged; the fallback stays on screen.
  console.error("Freelief could not start:", error);
  document.documentElement.dataset.ready = "fallback";
  document.documentElement.classList.remove("hide-fallback");
});
