"""Automated accessibility checks with axe (REQ-016): WCAG 2.2 A and AA, plus AAA contrast,
on every screen, on the states a person reaches inside them, and on the urgent-help dialog for every
region, in both themes."""

from axe_playwright_python.sync_playwright import Axe

from harness import open_app, wait_until
from test_unblock import SETTINGS as UNBLOCK, block, solve

AXE = Axe()
OPTIONS = {
    "runOnly": {"type": "tag",
                "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]},
    "rules": {"color-contrast-enhanced": {"enabled": True}},
    "resultTypes": ["violations"],
}
SCREENS = ["breathe", "menu", "bubbles", "garden", "unblock", "ripple", "mandala", "calm", "settings", "about", "feedback"]


def _violations(page):
    results = AXE.run(page, options=OPTIONS)
    return [f"{v['id']}: {v['help']} ({len(v['nodes'])} node(s))" for v in results.response["violations"]]


def _go(page, screen):
    page.evaluate(f"location.hash = '{screen}'")
    wait_until(page, f"document.querySelector('main').dataset.shown === '{screen}'", 2000)
    page.wait_for_timeout(150)


def _unblock_chosen(page):
    _go(page, "unblock")
    block(page, "A").focus()
    page.keyboard.press("Enter")
    page.locator(".unblock-slide").wait_for(state="visible")


def _unblock_solved(page):
    _go(page, "unblock")
    for name, steps in solve(UNBLOCK["boards"][0]["rows"]):
        block(page, name).focus()
        across = block(page, name).evaluate("e => e.classList.contains('across')")
        key = ("ArrowRight" if steps > 0 else "ArrowLeft") if across else ("ArrowDown" if steps > 0 else "ArrowUp")
        for _ in range(abs(steps)):
            page.keyboard.press(key)
    page.wait_for_timeout(500)
    assert page.locator(".unblock-block.key.free").count() == 1, "the board was not solved"


def _garden_chosen(page):
    _go(page, "garden")
    page.locator(".garden-item.stone").first.focus()
    page.keyboard.press("Enter")
    assert page.locator(".garden-item[aria-pressed=true]").count() == 1, "no item was chosen"


def _calm_full_screen(page):
    _go(page, "calm")
    page.locator(".full-screen").click()
    wait_until(page, "document.querySelector('.calm-stage, .stage')?.classList.contains('full')", 2000)


def _calm_black(page):
    _go(page, "calm")
    page.locator(".black-screen").click()
    page.locator(".black-cover").wait_for()


def _settings_reset_question(page):
    _go(page, "settings")
    page.locator(".reset-settings").click()
    page.locator(".reset-confirm").wait_for(state="visible")


def _feedback_problem(page):
    _go(page, "feedback")
    page.locator("input[name=kind][value=problem]").check()


# AUD-152: the states a person reaches by a tap or a key, each checked like a screen.
STATES = {
    "unblock, a block chosen": _unblock_chosen,
    "unblock, the board solved": _unblock_solved,
    "garden, an item chosen": _garden_chosen,
    "kaleidoscope, full screen": _calm_full_screen,
    "kaleidoscope, black screen": _calm_black,
    "settings, the reset question": _settings_reset_question,
    "feedback, a problem or an idea": _feedback_problem,
}


def _check(color_scheme):
    problems = []
    with open_app(color_scheme=color_scheme) as (page, _, _):
        for screen in SCREENS:
            _go(page, screen)
            problems += [f"[{screen}] {p}" for p in _violations(page)]
    for name, reach in STATES.items():
        with open_app(color_scheme=color_scheme) as (page, _, _):
            reach(page)
            problems += [f"[{name}] {p}" for p in _violations(page)]
    with open_app(color_scheme=color_scheme, route="menu") as (page, _, _):
        page.locator(".help-open").click()
        problems += [f"[help dialog] {p}" for p in _violations(page)]
        # Every curated region, and "Another country" (the empty value), in the dialog.
        values = page.locator("#help-country option").evaluate_all("os => os.map(o => o.value)")
        assert len(values) > 2 and "" in values, f"the country list is missing: {values}"
        for value in values:
            page.locator("#help-country").select_option(value)
            page.wait_for_timeout(100)
            problems += [f"[help dialog, region '{value or 'another country'}'] {p}" for p in _violations(page)]
    assert not problems, f"{color_scheme}: " + "; ".join(problems)


def test_axe_dark_theme():
    _check("dark")


def test_axe_light_theme():
    _check("light")
