// The shell: the page frame, the screen router, the footer and the "Need urgent help?" control.
// It holds no exercise logic and no literal text (AGENTS.md, Architecture).

import { loadStrings, t } from "./strings.js";
import { loadCrisisLines, deviceRegion, linesFor } from "./crisis.js";
import * as motion from "./motion.js";
import * as breathe from "./exercises/breathe.js";

async function loadConfig() {
  const response = await fetch("config.json");
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
  const close = element("button", { type: "button", class: "button close", text: t("help.close") });
  close.addEventListener("click", () => dialog.close());

  const body = [
    element("h2", { id: "help-title", text: t("help.title") }),
    element("p", { text: t("help.intro") }),
    element("p", { class: "emergency", text: own
      ? t("help.emergency", { number: own.emergency })
      : t("help.emergencyUnknown") }),
  ];
  if (own) body.push(regionBlock(own, "h3"));
  body.push(element("p", { class: "directory" }, [
    element("a", { class: "button", href: directory.url, rel: "noopener", text: t("help.directory") }),
    element("span", { class: "directory-note", text: t("help.directoryNote", { note: directory.note }) }),
  ]));
  const details = element("details", { class: "others" }, [
    element("summary", { text: t("help.otherCountries") }),
    ...others.map((region) => regionBlock(region, "h3")),
  ]);
  body.push(details, close);
  dialog.append(...body);
  return dialog;
}

function buildShell() {
  const helpButton = element("button", {
    type: "button", class: "button help-open", "aria-haspopup": "dialog", text: t("help.open"),
  });
  const header = element("header", { class: "top" }, [
    element("p", { class: "brand", text: t("app.name") }),
    helpButton,
  ]);
  const main = element("main", { id: "screen" });
  const footer = element("footer", { class: "bottom" }, [
    element("p", { class: "tagline", text: t("app.tagline") }),
    element("p", { class: "self-help", text: t("footer.selfHelp") }),
  ]);
  const dialog = buildHelpDialog();
  helpButton.addEventListener("click", () => dialog.showModal());
  document.body.replaceChildren(header, main, footer, dialog);
  return main;
}

async function boot() {
  const [config] = await Promise.all([loadConfig(), loadStrings("en"), loadCrisisLines()]);
  document.title = t("app.name");
  const main = buildShell();
  breathe.start(main, { t, config, motion, rhythm: config.breathing.defaultRhythm });
  document.documentElement.dataset.ready = "true";
  performance.mark("freelief-ready");
}

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("sw.js").catch(() => {
    // Offline support is lost, but the app still works online.
  });
}

boot();
