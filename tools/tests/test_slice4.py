"""Slice 4 in a real browser: About and disclaimer, Standards and research, Feedback."""

import json
from urllib.parse import parse_qs, urlparse

from harness import ROOT, base_url, open_app, wait_until

STRINGS = json.loads((ROOT / "strings" / "en.json").read_text("utf-8"))
RESEARCH = json.loads((ROOT / "data" / "research.json").read_text("utf-8"))
CONFIG = json.loads((ROOT / "config.json").read_text("utf-8"))
VERSION = (ROOT / "version.js").read_text("utf-8").split('"')[1]


def go(page, route):
    page.evaluate(f"location.hash = '{route}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 3000)


def test_footer_links_reach_every_page_from_every_screen():
    with open_app() as (page, errors, _):
        for screen in ("breathe", "ground", "settings"):
            go(page, screen)
            hrefs = page.locator(".footer-link").evaluate_all("els => els.map(e => e.getAttribute('href'))")
            assert hrefs == ["#about", "#standards", "#feedback"], screen
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


def test_standards_claims_nothing_until_verified():
    # REQ-029: with no verified check, no standard is shown as met.
    with open_app() as (page, _, _):
        go(page, "standards")
        assert page.locator(".standards-none").inner_text() == STRINGS["standards.none"]
        assert page.locator(".standards-list").count() == 0


def test_a_verified_standard_is_listed_with_date_and_tester():
    fake = {"verified": [{"name": "WCAG 2.2", "level": "AA", "checked": "2027-01-15",
                          "tester": "a volunteer using NVDA"}]}
    with open_app(service_workers="block") as (page, _, _):
        page.route("**/data/standards.json", lambda route: route.fulfill(json=fake))
        go(page, "standards")
        item = page.locator(".standards-list li").inner_text()
        assert item == "WCAG 2.2, level AA, checked 2027-01-15 by a volunteer using NVDA"
        assert page.locator(".standards-none").count() == 0


def test_every_technique_cites_dated_sources():
    # REQ-024: every technique cites at least one source.
    with open_app() as (page, _, _):
        go(page, "standards")
        sections = page.locator("section.technique")
        assert sections.count() == len(RESEARCH["techniques"])
        for technique in RESEARCH["techniques"]:
            section = page.locator(f"section.technique[data-technique='{technique['id']}']")
            links = section.locator(".sources a")
            assert links.count() == len(technique["sources"]) >= 1
            for i, source_id in enumerate(technique["sources"]):
                assert links.nth(i).get_attribute("href") == RESEARCH["sources"][source_id]["url"]
        assert "limited" in page.locator("section.technique[data-technique='grounding']").inner_text()


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
        assert query["body"] == [message.input_value()]
        message.fill("The breathing screen works well with NVDA.")
        assert _link_query(page)["body"] == ["The breathing screen works well with NVDA."]
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
        logo = page.locator("img.maker-logo")
        assert logo.get_attribute("alt") == "Effigy Media"
        assert page.evaluate("document.querySelector('img.maker-logo').naturalWidth") > 0, "the logo loads"
        link = page.locator(".maker a")
        assert link.get_attribute("href") == "https://www.effigymedia.com"
        assert "Effigy Media" in page.locator(".maker").inner_text()