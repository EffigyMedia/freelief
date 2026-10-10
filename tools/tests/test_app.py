"""Slice 1 in a real browser: breathing at launch, urgent help, keyboard, reduced motion."""

import re
from urllib.parse import urlparse

from harness import ROOT, base_url, open_app, wait_until


def test_breath_guide_starts_at_launch_with_a_clean_console():
    # REQ-018: the guide starts at once, with nothing before it.
    with open_app() as (page, errors, _):
        assert page.locator(".guide").is_visible()
        wait_until(page, "document.querySelector('.phase').textContent.trim().length > 0", 1000)
        assert page.locator(".phase").inner_text() == "Breathe in"
        assert not errors, f"console errors: {errors}"


def test_the_main_screen_shows_the_self_help_line():
    # REQ-006: the main screen (the menu since 2026-10-07) shows the self-help line.
    with open_app(route=None) as (page, _, _):
        assert page.evaluate("document.querySelector('main').dataset.shown") == "menu"
        assert page.locator(".self-help").is_visible(), "the self-help line must show (REQ-006)"


def test_breathing_moves_from_in_to_out():
    with open_app() as (page, _, _):
        # The default is 4 in, 6 out, so the out-breath starts at 4 s.
        wait_until(page, "document.querySelector('.phase').textContent === 'Breathe out'", 6000)


def test_no_request_leaves_the_origin():
    # REQ-015: nothing is sent anywhere.
    # Every screen is visited, not only the help dialog (AUD-027).
    with open_app() as (page, _, requests):
        page.locator(".help-open").click()
        page.wait_for_timeout(300)
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        for route in ("menu", "breathe", "bubbles", "trace", "unblock", "ripple", "mandala", "calm", "settings", "about", "feedback"):
            page.evaluate(f"location.hash = '{route}'")
            wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 5000)
        page.wait_for_timeout(300)
        origin = urlparse(base_url()).netloc
        foreign = [url for url in requests if urlparse(url).netloc not in (origin, "")]
        assert not foreign, f"requests to another origin: {foreign}"


def test_help_opens_and_closes_by_keyboard():
    # REQ-009: every control by keyboard. Help is the third line of the header (owner, 2026-10-09),
    # so it is the sixth stop on Tab, after the five round buttons: the order follows what is seen.
    with open_app() as (page, _, _):
        for _ in range(6):
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
        # Tab order: urgent help, sound, the Settings gear, the three sound-bar buttons, Back to
        # menu, then the screen's controls.
        assert page.evaluate("document.querySelector('.nav-back').compareDocumentPosition("
                             "document.querySelector('.pause')) & Node.DOCUMENT_POSITION_FOLLOWING")
        for _ in range(8):
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
        first = dialog.locator(".region-lines > section.region")
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
        select = page.locator("#help-country")
        codes = [c for c in select.locator("option").evaluate_all("os => os.map(o => o.value)") if c]
        assert len(codes) == 5
        for code in codes:
            select.select_option(code)
            assert page.locator(".region-lines section.region").get_attribute("data-region") == code
            lines = page.locator(".region-lines li.line")
            assert lines.count() >= 1, code
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
        small = page.evaluate("""() => [...document.querySelectorAll('button, a, summary, select')]
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
        page.evaluate("location.hash = 'trace'")
        wait_until(page, "document.querySelector('main').dataset.shown === 'trace'", 3000)
        assert not [e for e in errors if "could not" in e], errors

def test_a_region_saved_in_settings_opens_urgent_help_and_the_list_changes_it_for_this_visit():
    # Owner, 2026-10-07: a default region in Settings, and a country list in place of the long list.
    with open_app(locale="en-US") as (page, _, _):
        page.evaluate("location.hash = 'settings'")
        wait_until(page, "document.querySelector('main').dataset.shown === 'settings'", 3000)
        assert page.locator("#help-region").input_value() == "auto"
        page.locator("#help-region").select_option("GB")
        page.reload()
        page.wait_for_selector("html[data-ready='true']")
        page.locator(".help-open").click()
        assert page.locator("#help-country").input_value() == "GB"
        assert page.locator(".region-lines section.region").get_attribute("data-region") == "GB"
        assert "999" in page.locator(".emergency").inner_text()
        page.locator("#help-country").select_option("AU")
        assert page.locator(".region-lines section.region").get_attribute("data-region") == "AU"
        page.locator("#help-country").select_option("")
        assert page.locator(".emergency").inner_text() == "If you are in immediate danger, call your local emergency number."
        assert page.locator(".region-lines section.region").count() == 0
        assert page.locator(".directory a").count() == 1
        page.locator(".help-back").click()
        page.locator(".help-open").click()
        assert page.locator("#help-country").input_value() == "GB", "the list changes one visit, not the setting"
        page.locator(".help-back").click()
        page.evaluate("location.hash = 'settings'")
        wait_until(page, "document.querySelector('main').dataset.shown === 'settings'", 3000)
        page.locator("#help-region").select_option("auto")
        page.locator(".help-open").click()
        assert page.locator("#help-country").input_value() == "US", "Automatic follows the device"


def test_the_country_list_is_reached_and_used_by_keyboard():
    with open_app(locale="en-GB") as (page, _, _):
        page.locator(".help-open").click()
        page.keyboard.press("Tab")
        for _ in range(5):
            if page.evaluate("document.activeElement.id") == "help-country":
                break
            page.keyboard.press("Tab")
        assert page.evaluate("document.activeElement.id") == "help-country"
        assert page.locator("label[for='help-country']").inner_text() == "Country"
        page.keyboard.press("ArrowDown")
        chosen = page.locator("#help-country").input_value()
        assert chosen != "GB", "the arrow key moved to the next country"
        assert page.locator(".region-lines section.region").get_attribute("data-region") == chosen


def test_a_language_with_no_region_gets_the_general_route_not_a_guess():
    # AUD-026: a bare "en" must not become the US and "call 911".
    own, emergency, directory_links = _help_region("en")
    assert own is None
    assert emergency == "If you are in immediate danger, call your local emergency number."
    assert directory_links == 1


def test_a_web_chat_says_it_needs_the_internet():
    # AUD-052: calls and texts work offline; a chat does not.
    import json as _json
    data = _json.loads((ROOT / "data" / "crisis-lines.json").read_text("utf-8"))
    with_web = [code for code, region in data["regions"].items() if any(line.get("web") for line in region["lines"])]
    assert with_web, "no region has a web chat to check"
    with open_app() as (page, _, _):
        page.locator(".help-open").click()
        page.locator("#help-country").select_option(with_web[0])
        assert "needs an internet connection" in page.locator(".region-lines").inner_text()
