"""Slice 4 in a real browser: About and disclaimer, and Feedback. Standards and research was removed
on 2026-10-10 (owner, RLG-056)."""

import json
import re
from urllib.parse import parse_qs, urlparse

from harness import ROOT, base_url, open_app, wait_until

STRINGS = json.loads((ROOT / "strings" / "en.json").read_text("utf-8"))
CONFIG = json.loads((ROOT / "config.json").read_text("utf-8"))
VERSION = (ROOT / "version.js").read_text("utf-8").split('"')[1]


def go(page, route):
    page.evaluate(f"location.hash = '{route}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 3000)


def test_footer_links_reach_every_page_from_every_screen():
    with open_app() as (page, errors, _):
        # Owner, 2026-10-08: the full footer is on the menu and the info pages; an exercise shows only
        # the calm line, and the links are one tap away through Back to menu.
        for screen in ("menu", "settings", "about", "feedback"):
            go(page, screen)
            assert page.locator(".footer-link").evaluate_all("els => els.map(e => e.getAttribute('href'))")                 == ["#about", "#feedback"], screen
            assert page.locator(".footer-link").first.is_visible() and page.locator(".self-help").is_visible(), screen
        for screen in ("breathe", "bubbles", "garden", "unblock", "ripple", "mandala", "calm"):
            go(page, screen)
            assert page.locator(".tagline").is_visible(), screen
            assert page.locator(".footer-link").first.is_hidden() and page.locator(".self-help").is_hidden(), screen
        go(page, "menu")
        page.locator(".footer-link[href='#about']").click()
        wait_until(page, "document.querySelector('main').dataset.shown === 'about'")
        assert not errors, errors


def test_about_states_self_help_privacy_and_version():
    # REQ-006 (the full statement), REQ-015 (privacy), REQ-031 (open license).
    with open_app() as (page, _, _):
        go(page, "about")
        text = page.locator("main").inner_text()
        for key in ("about.selfHelp1", "about.selfHelp3", "about.privacy1", "about.open1"):
            assert STRINGS[key] in text, key
        assert f"Version {VERSION}" in text


def _link_query(page):
    return parse_qs(urlparse(page.locator("a.github").get_attribute("href")).query)


def test_feedback_prefills_an_editable_github_issue():
    # REQ-030: the person sees and can edit everything that would be sent.
    with open_app() as (page, _, requests) :
        go(page, "feedback")
        message = page.locator("textarea.message")
        assert f"Version: {VERSION}" in message.input_value()
        query = _link_query(page)
        assert query["template"] == ["accessibility-check.md"]
        # AUD-055 (owner, 2026-10-08): the person's words never go into the web address.
        message.fill("The breathing screen works well with NVDA.")
        query = _link_query(page)
        assert "body" not in query and "NVDA" not in page.locator("a.github").get_attribute("href")
        assert query["title"][0].startswith("Accessibility check: Freelief")
        page.context.grant_permissions(["clipboard-read", "clipboard-write"])
        page.locator("button.copy-message").click()
        wait_until(page, "document.querySelector('.copy-status').textContent.startsWith('Copied')", 2000)
        assert page.evaluate("navigator.clipboard.readText()") == "The breathing screen works well with NVDA."
        origin = urlparse(base_url()).netloc
        assert all(urlparse(u).netloc == origin for u in requests), "the app itself sent nothing"


def test_switching_kind_keeps_typed_words_and_refills_an_untouched_template():
    with open_app() as (page, _, _):
        go(page, "feedback")
        page.locator("input[name=kind][value=problem]").check()
        message = page.locator("textarea.message")
        assert message.input_value().startswith("Freelief problem or idea")
        assert _link_query(page)["template"] == ["problem-report.md"]
        message.fill("My own words")
        page.locator("input[name=kind][value=accessibility]").check()
        assert message.input_value() == "My own words"


def test_email_is_hidden_until_an_address_is_set():
    assert CONFIG["project"]["feedbackEmail"] == "", "update this test when the address is chosen"
    with open_app() as (page, _, _):
        go(page, "feedback")
        assert page.locator(".email-choice").is_hidden()


def test_issue_templates_exist_for_every_kind():
    for name in CONFIG["project"]["issueTemplates"].values():
        assert (ROOT / ".github" / "ISSUE_TEMPLATE" / name).is_file(), name


def test_about_credits_effigy_media_with_logo_and_website():
    # Owner, 2026-10-07: attribution with the Effigy logo and www.effigymedia.com.
    with open_app() as (page, _, _):
        go(page, "about")
        logo = page.locator("svg.maker-logo")
        assert logo.get_attribute("role") == "img" and logo.get_attribute("aria-label") == "Effigy Media"
        assert logo.locator("rect").count() == 6, "three bars across and three down; no lettering"
        box = logo.bounding_box()
        assert box["width"] > 100 and box["height"] > 40, "the logo is drawn at a visible size"
        text = page.evaluate("getComputedStyle(document.body).color")
        assert logo.evaluate("e => getComputedStyle(e).fill") == text, "the logo takes the theme's text color"
        link = page.locator(".maker a")
        assert link.get_attribute("href") == "https://www.effigymedia.com"
        assert "Alexander Steele, Effigy Media" in page.locator(".maker").inner_text()
        # Owner, 2026-10-07: the name sits on its own line, under "Freelief is made by".
        assert "Freelief is made by" + chr(10) + "Alexander Steele, Effigy Media." in page.locator(".maker").inner_text()
        first = page.locator(".maker p").first.evaluate("p => p.firstChild.textContent")
        assert first == "Freelief is made by"

def test_the_logo_is_soft_white_on_dark_and_soft_black_on_light():
    fills = {}
    for scheme in ("dark", "light"):
        with open_app(color_scheme=scheme) as (page, _, _):
            go(page, "about")
            fills[scheme] = page.locator("svg.maker-logo").evaluate("e => getComputedStyle(e).fill")
    assert fills == {"dark": "rgb(230, 236, 245)", "light": "rgb(29, 36, 51)"}, fills


def test_when_copying_is_refused_the_message_is_selected_to_copy_by_hand():
    refuse = "navigator.clipboard.writeText = () => Promise.reject(new Error('no'));"
    with open_app(init_script=refuse) as (page, errors, _):
        go(page, "feedback")
        page.locator("button.copy-message").click()
        wait_until(page, "document.querySelector('.copy-status').textContent.startsWith('Could not')", 2000)
        selected = page.evaluate("(() => { const m = document.querySelector('textarea.message'); "
                                 "return [document.activeElement === m, m.selectionEnd - m.selectionStart, m.value.length]; })()")
        assert selected[0] and selected[1] == selected[2] > 0, selected
        assert not errors, errors


def test_feedback_says_issues_are_public_and_points_a_person_in_danger_to_help():
    # AUD-006 and AUD-053: the page and both GitHub templates say it, before anything is posted.
    with open_app() as (page, _, _):
        go(page, "feedback")
        assert "public" in page.locator("#github-note").inner_text()
        assert "Need urgent help?" in page.locator(".feedback-safety").inner_text()
        assert page.locator(".feedback-safety").is_visible()
    for name in CONFIG["project"]["issueTemplates"].values():
        text = (ROOT / ".github" / "ISSUE_TEMPLATE" / name).read_text("utf-8")
        assert "issues are public" in text and "Need urgent help?" in text, name
