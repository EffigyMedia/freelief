"""Automated accessibility checks with axe (REQ-016): WCAG 2.2 A and AA, plus AAA contrast."""

from axe_playwright_python.sync_playwright import Axe

from harness import open_app

AXE = Axe()
OPTIONS = {
    "runOnly": {"type": "tag",
                "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]},
    "rules": {"color-contrast-enhanced": {"enabled": True}},
    "resultTypes": ["violations"],
}


def _violations(page):
    results = AXE.run(page, options=OPTIONS)
    return [f"{v['id']}: {v['help']} ({len(v['nodes'])} node(s))" for v in results.response["violations"]]


def _check(color_scheme):
    with open_app(color_scheme=color_scheme) as (page, _, _):
        page.wait_for_timeout(200)
        problems = _violations(page)
        page.locator(".help-open").click()
        page.locator("details.others summary").click()
        problems += [f"[help dialog] {p}" for p in _violations(page)]
        assert not problems, f"{color_scheme}: " + "; ".join(problems)


def test_axe_dark_theme():
    _check("dark")


def test_axe_light_theme():
    _check("light")
