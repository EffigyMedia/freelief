"""Slice 1 in a real browser: breathing at launch, urgent help, keyboard, reduced motion."""

import re
from urllib.parse import urlparse

from harness import base_url, open_app, wait_until


def test_breath_guide_starts_at_launch_with_a_clean_console():
    # REQ-018: the guide starts at once, with nothing before it.
    with open_app() as (page, errors, _):
        assert page.locator(".guide").is_visible()
        wait_until(page, "document.querySelector('.phase').textContent.trim().length > 0", 1000)
        assert page.locator(".phase").inner_text() == "Breathe in"
        assert page.locator(".self-help").is_visible(), "the self-help line must show (REQ-006)"
        assert not errors, f"console errors: {errors}"


def test_breathing_moves_from_in_to_out():
    with open_app() as (page, _, _):
        wait_until(page, "document.querySelector('.phase').textContent === 'Breathe out'", 6000)


def test_no_request_leaves_the_origin():
    # REQ-015: nothing is sent anywhere.
    with open_app() as (page, _, requests):
        page.locator(".help-open").click()
        page.wait_for_timeout(300)
        origin = urlparse(base_url()).netloc
        foreign = [url for url in requests if urlparse(url).netloc not in (origin, "")]
        assert not foreign, f"requests to another origin: {foreign}"


def test_help_opens_and_closes_by_keyboard():
    # REQ-009: every control by keyboard. The help control is the first stop on Tab.
    with open_app() as (page, _, _):
        page.keyboard.press("Tab")
        assert page.evaluate("document.activeElement.classList.contains('help-open')")
        page.keyboard.press("Enter")
        assert page.locator("dialog.help").evaluate("d => d.open")
        assert page.evaluate("document.querySelector('dialog.help').contains(document.activeElement)")
        page.keyboard.press("Escape")
        assert not page.locator("dialog.help").evaluate("d => d.open")
        assert page.evaluate("document.activeElement.classList.contains('help-open')"), \
            "focus must return to the help control"


def test_pause_and_resume_by_keyboard():
    with open_app() as (page, _, _):
        # Tab order: urgent help, the Settings gear, Back to menu, then the screen's own controls.
        assert page.evaluate("document.querySelector('.nav-back').compareDocumentPosition("
                             "document.querySelector('.pause')) & Node.DOCUMENT_POSITION_FOLLOWING")
        for _ in range(4):
            page.keyboard.press("Tab")
        assert page.evaluate("document.activeElement.classList.contains('pause')")
        page.keyboard.press("Space")
        pause = page.locator(".pause")
        assert pause.get_attribute("aria-pressed") == "true"
        assert pause.inner_text() == "Resume"
        page.keyboard.press("Space")
        assert pause.get_attribute("aria-pressed") == "false"


def _help_region(locale):
    with open_app(locale=locale) as (page, _, _):
        page.locator(".help-open").click()
        dialog = page.locator("dialog.help")
        first = dialog.locator(".help-body > section.region")
        own = first.get_attribute("data-region") if first.count() else None
        return own, dialog.locator(".emergency").inner_text(), dialog.locator(".directory a").count()


def test_help_shows_the_device_region_first():
    # REQ-005 and REQ-022: lines by device region, with the directory as fallback.
    assert _help_region("en-GB")[:2] == ("GB", "If you are in immediate danger, call 999.")
    assert _help_region("en-US")[:2] == ("US", "If you are in immediate danger, call 911.")
    assert _help_region("en-AU")[0] == "AU"
    assert _help_region("en-IE")[0] == "IE"
    assert _help_region("fr-CA")[0] == "CA"


def test_help_falls_back_for_an_uncurated_region():
    own, emergency, directory_links = _help_region("de-DE")
    assert own is None
    assert emergency == "If you are in immediate danger, call your local emergency number."
    assert directory_links == 1


def test_every_crisis_line_is_dated_and_dialable():
    with open_app() as (page, _, _):
        page.locator(".help-open").click()
        page.locator("details.others summary").click()
        lines = page.locator("li.line")
        assert lines.count() == 5
        for i in range(lines.count()):
            line = lines.nth(i)
            assert re.search(r"Last checked \d{4}-\d{2}-\d{2}", line.inner_text())
            assert line.locator("a[href^='tel:']").count() == 1


def test_reduced_motion_keeps_the_guide_still():
    # REQ-010: no animation when the device asks for reduced motion.
    with open_app(reduced_motion="reduce") as (page, _, _):
        page.wait_for_timeout(300)
        first = page.locator(".guide-circle").evaluate("e => getComputedStyle(e).transform")
        page.wait_for_timeout(1500)
        later = page.locator(".guide-circle").evaluate("e => getComputedStyle(e).transform")
        assert first == later, "the guide moved under reduced motion"
        wait_until(page, "document.querySelector('.guide-count').textContent !== ''", 1500)


def test_targets_are_at_least_44_pixels():
    # WCAG 2.2 target size, at the AAA size of 44 by 44 CSS pixels.
    with open_app() as (page, _, _):
        page.locator(".help-open").click()
        page.locator("details.others summary").click()
        small = page.evaluate("""() => [...document.querySelectorAll('button, a, summary')]
            .filter(e => e.offsetParent !== null)
            .map(e => [e.textContent.trim(), e.getBoundingClientRect()])
            .filter(([, r]) => r.width < 44 || r.height < 44)
            .map(([t, r]) => `${t} ${Math.round(r.width)}x${Math.round(r.height)}`)""")
        assert not small, f"targets under 44px: {small}"


def test_an_inherited_name_in_the_hash_falls_back_to_the_menu():
    # AUD-005: #constructor, #toString and #__proto__ are not screens.
    with open_app() as (page, errors, _):
        for name in ("constructor", "toString", "__proto__", "nothing-here"):
            page.evaluate(f"location.hash = '{name}'")
            wait_until(page, "document.querySelector('main').dataset.shown === 'menu'", 3000)
            assert page.locator(".menu-item").first.is_visible(), name
        page.evaluate("location.hash = 'ground'")
        wait_until(page, "document.querySelector('main').dataset.shown === 'ground'", 3000)
        assert not [e for e in errors if "could not" in e], errors