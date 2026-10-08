// Feedback (REQ-030). The page fills in a message the person can read and change, then hands it
// to GitHub (a new-issue link) or to their own email app. Freelief itself sends nothing. The
// email choice stays hidden until config.json names a public project address.

function browserName() {
  const brands = navigator.userAgentData?.brands?.filter((b) => !/not.?a.?brand/i.test(b.brand));
  if (brands?.length) return brands.map((b) => `${b.brand} ${b.version}`).join(", ");
  const ua = navigator.userAgent;
  const match = ua.match(/(Firefox|Edg|Chrome|Version)\/(\d+)/);
  if (!match) return null;
  const name = { Edg: "Edge", Version: "Safari" }[match[1]] || match[1];
  return `${name} ${match[2]}`;
}

function deviceName() {
  const ua = navigator.userAgent;
  const platform = navigator.userAgentData?.platform
    || (/iPhone|iPad/.test(ua) ? "iOS" : /Android/.test(ua) ? "Android"
      : /Windows/.test(ua) ? "Windows" : /Mac/.test(ua) ? "macOS" : /Linux/.test(ua) ? "Linux" : null);
  const mobile = navigator.userAgentData?.mobile ?? /Mobi|iPhone|Android/.test(ua);
  return platform ? `${platform}${mobile ? " (phone or tablet)" : ""}` : null;
}

export function start(container, ctx) {
  const { t, config } = ctx;
  const project = config.project;
  const unknown = t("feedback.unknown");
  const facts = {
    version: self.FREELIEF_VERSION,
    browser: browserName() || unknown,
    device: deviceName() || unknown,
  };

  container.innerHTML = `
    <section class="page feedback">
      <h1>${t("feedback.title")}</h1>
      <p>${t("feedback.intro")}</p>
      <fieldset>
        <legend>${t("feedback.kind")}</legend>
        <label class="choice"><input type="radio" name="kind" value="accessibility" checked>
          <span>${t("feedback.kind.accessibility")}</span></label>
        <label class="choice"><input type="radio" name="kind" value="problem">
          <span>${t("feedback.kind.problem")}</span></label>
      </fieldset>
      <label class="field-label" for="feedback-message">${t("feedback.messageLabel")}</label>
      <textarea id="feedback-message" class="message" rows="14"></textarea>
      <p class="feedback-safety">${t("feedback.danger")}</p>
      <div class="send-choice">
        <button type="button" class="button primary copy-message">${t("feedback.copy")}</button>
        <p class="copy-status hint" aria-live="polite"></p>
        <a class="button github" rel="noopener" aria-describedby="github-note">${t("feedback.github")}</a>
        <p id="github-note" class="hint">${t("feedback.githubNote")}</p>
      </div>
      <div class="send-choice email-choice" ${project.feedbackEmail ? "" : "hidden"}>
        <a class="button email" aria-describedby="email-note">${t("feedback.email")}</a>
        <p id="email-note" class="hint">${t("feedback.emailNote")}</p>
      </div>
    </section>`;

  const message = container.querySelector(".message");
  const github = container.querySelector(".github");
  const email = container.querySelector(".email");
  let kind = "accessibility";
  let lastTemplate = "";

  // The GitHub link carries only the kind's template and a title, never the person's words: a
  // web address is kept in browser history and reaches GitHub as soon as it opens (AUD-055). The
  // person copies the message and pastes it into the issue. The email link opens the person's own
  // mail app, so it carries the message as the text box shows it.
  function updateLinks() {
    const title = t(`feedback.title.${kind}`, { version: facts.version });
    const issue = new URL(project.newIssueUrl);
    issue.searchParams.set("template", project.issueTemplates[kind]);
    issue.searchParams.set("title", title);
    github.href = issue.toString();
    if (project.feedbackEmail) {
      email.href = `mailto:${project.feedbackEmail}?subject=${encodeURIComponent(title)}&body=${encodeURIComponent(message.value)}`;
    }
  }

  // Switching the kind refills the box only if the person has not changed it, so no typed words are lost.
  function fillTemplate() {
    if (message.value === lastTemplate) {
      lastTemplate = t(`feedback.template.${kind}`, facts);
      message.value = lastTemplate;
    }
    updateLinks();
  }

  container.querySelectorAll("input[name=kind]").forEach((input) => input.addEventListener("change", () => {
    kind = input.value;
    fillTemplate();
  }));
  message.addEventListener("input", updateLinks);

  // Copy the message. Where the browser refuses, select it, so the person can copy it themselves.
  const copyStatus = container.querySelector(".copy-status");
  container.querySelector(".copy-message").addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(message.value);
      copyStatus.textContent = t("feedback.copied");
    } catch {
      message.focus();
      message.select();
      copyStatus.textContent = t("feedback.copyFailed");
    }
  });
  fillTemplate();
}

export function stop() {}
