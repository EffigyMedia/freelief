// The shell: the page frame, the screen router, the footer and the "Need urgent help?" control.
// It holds no exercise logic and no literal text (AGENTS.md, Architecture).

import { loadStrings, t, list } from "./strings.js";
import { loadCrisisLines, deviceRegion, linesFor } from "./crisis.js";
import { initSettings, getSetting, onSettingChange } from "./settings.js";
import * as audio from "./audio.js";
import * as motion from "./motion.js";
import * as breathe from "./exercises/breathe.js";
import * as ground from "./exercises/ground.js";
import * as statements from "./exercises/statements.js";
import * as bubbles from "./activities/bubbles.js";
import * as trace from "./activities/trace.js";
import * as sort from "./activities/sort.js";
import * as menu from "./screens/menu.js";
import * as settingsScreen from "./screens/settings.js";
import * as about from "./screens/about.js";
import * as standards from "./screens/standards.js";
import * as feedback from "./screens/feedback.js";

// The screens the router knows. Breathing is the default and the first screen (REQ-018).
const ROUTES = {
  breathe, ground, statements, bubbles, trace, sort, menu, settings: settingsScreen, about, standards, feedback,
};
const DEFAULT_ROUTE = "breathe";

let config = null;
let current = null;
let main = null;
let moreLink = null;
let backLink = null;

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
  const header = element("header", { class: "top" }, [
    element("p", { class: "brand", text: t("app.name") }),
    helpButton,
  ]);
  main = element("main", { id: "screen" });
  // Every exercise and activity offers both ways on (owner, 2026-10-07).
  moreLink = element("a", { class: "button nav-link nav-more", href: "#menu", text: t("nav.more") });
  backLink = element("a", { class: "button nav-link nav-back", href: "#breathe", text: t("nav.back") });
  const nav = element("nav", { class: "screen-nav", "aria-label": t("nav.label") }, [moreLink, backLink]);
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
  document.body.replaceChildren(header, main, nav, footer, dialog);
}

function routeName() {
  const name = location.hash.replace(/^#/, "");
  return name in ROUTES ? name : DEFAULT_ROUTE;
}

let showing = 0;

async function show(name, { moveFocus }) {
  if (current) current.stop();
  current = ROUTES[name];
  const request = ++showing;
  main.dataset.screen = name;
  delete main.dataset.shown;
  // A screen may load data first (Standards and research), so wait for it before focusing.
  await current.start(main, {
    t, list, config, motion, audio, rhythm: getSetting("rhythm"),
  });
  if (request !== showing) return;
  main.dataset.shown = name;
  moreLink.hidden = name === "menu";
  backLink.hidden = name === "breathe";
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
});
