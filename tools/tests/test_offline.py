"""The installable offline app (REQ-008): the cache list is complete and the app runs offline."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import freelief  # noqa: E402
from harness import ROOT, browser, open_app, serve, wait_until  # noqa: E402

NOT_CACHED = {"sw.js"}  # the browser fetches the worker script itself


def cached_files():
    source = (ROOT / "sw.js").read_text("utf-8")
    block = re.search(r"const FILES = \[(.*?)\];", source, re.DOTALL).group(1)
    return {f for f in re.findall(r'"([^"]+)"', block) if f != "./"}


def test_cache_list_matches_the_shipped_files():
    shipped = {p.relative_to(ROOT).as_posix() for p in freelief.shipped_files()} - NOT_CACHED
    listed = cached_files()
    assert not shipped - listed, f"shipped but not cached: {sorted(shipped - listed)}"
    assert not listed - shipped, f"cached but missing: {sorted(listed - shipped)}"


def test_the_app_works_offline_after_one_visit():
    with open_app(service_workers="allow") as (page, errors, _):
        page.evaluate("navigator.serviceWorker.ready")
        page.reload()
        wait_until(page, "navigator.serviceWorker.controller !== null", 5000)
        page.context.set_offline(True)
        page.reload()
        try:
            page.wait_for_selector("html[data-ready='true']", timeout=10000)
        except Exception as error:
            state = page.evaluate("""(async () => ({ ready: document.documentElement.dataset.ready,
                keys: await caches.keys(),
                entries: (await (await caches.open('freelief-' + self.FREELIEF_VERSION)).keys()).length }))()""")
            raise AssertionError(f"offline launch did not finish: {state}; console: {errors}") from error
        assert page.locator(".guide").is_visible()
        page.locator(".help-open").click()
        assert page.locator("dialog.help li.line").count() >= 1
        page.keyboard.press("Escape")
        # Closing the dialog steps back one history entry; let it finish before navigating.
        wait_until(page, "!(history.state && history.state.freeliefHelp)", 2000)
        page.wait_for_timeout(200)
        # Screens other than breathing load on first visit (RLG-006); offline they come from the cache.
        for route in ("trace", "calm", "standards"):
            page.evaluate(f"location.hash = '{route}'")
            wait_until(page, f"document.querySelector('main').dataset.shown === '{route}'", 5000)


def test_the_manifest_makes_the_app_installable():
    import json
    manifest = json.loads((ROOT / "manifest.webmanifest").read_text("utf-8"))
    sizes = {icon["sizes"] for icon in manifest["icons"]}
    assert {"192x192", "512x512"} <= sizes
    assert manifest["display"] == "standalone"
    assert manifest["orientation"] == "portrait", "owner, 2026-10-07: portrait only once installed"
    for icon in manifest["icons"]:
        assert (ROOT / icon["src"]).is_file(), icon["src"]


FOREIGN_CACHE = "effigy-arcade-core-v9"


def test_a_deleted_cache_repairs_itself_and_works_offline_again():
    # AUD-001: another app on the shared origin deletes every cache it does not own.
    with open_app(service_workers="allow") as (page, _, _):
        page.evaluate("navigator.serviceWorker.ready")
        page.reload()
        wait_until(page, "navigator.serviceWorker.controller !== null", 5000)
        page.evaluate("caches.keys().then(keys => Promise.all(keys.map(k => caches.delete(k))))")
        assert page.evaluate("caches.keys()") == []
        page.reload()  # online: the page notices and asks the worker to repair the cache
        wait_until(page, f"caches.has('freelief-' + self.FREELIEF_VERSION)", 8000)
        wait_until(page, "caches.open('freelief-' + self.FREELIEF_VERSION)"
                         ".then(c => c.keys()).then(k => k.length >= 30)", 8000)
        page.context.set_offline(True)
        page.reload()
        page.wait_for_selector("html[data-ready='true']", timeout=5000)
        assert page.locator(".guide").is_visible()
        assert page.locator(".help-open").is_visible()


def test_an_update_keeps_other_apps_caches_and_drops_only_old_freelief_ones():
    # AUD-014 and the design's update test: a new version replaces Freelief's cache, deletes the old
    # Freelief cache, and never touches another app's cache on the shared origin.
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        app = Path(temp) / "app"
        shutil.copytree(ROOT, app, ignore=shutil.ignore_patterns(
            ".git", ".venv", "output", "input", "docs", "tools", "__pycache__", ".claude", ".github"))
        url = serve(app)
        context = browser().new_context(service_workers="allow")
        try:
            page = context.new_page()
            page.goto(url)
            page.evaluate("navigator.serviceWorker.ready")
            page.reload()
            wait_until(page, "navigator.serviceWorker.controller !== null", 5000)
            old = page.evaluate("'freelief-' + self.FREELIEF_VERSION")
            page.evaluate(f"caches.open('{FOREIGN_CACHE}')")
            (app / "version.js").write_text('self.FREELIEF_VERSION = "9.9.9";\n', "utf-8")
            try:
                page.evaluate("navigator.serviceWorker.getRegistration().then(r => r.update())")
            except Exception:
                pass  # the takeover reloads the page; that is expected
            wait_until(page, "caches.has('freelief-9.9.9')", 8000)
            wait_until(page, f"caches.has('{old}').then(present => !present)", 8000)
            wait_until(page, "document.readyState === 'complete'", 5000)
            keys = page.evaluate("caches.keys()")
            assert FOREIGN_CACHE in keys, keys
            assert "freelief-9.9.9" in keys and old not in keys, keys
        finally:
            context.close()

def test_precache_bypasses_the_http_cache():
    # AUD-013: a new version must not store an old file from the browser's HTTP cache.
    source = (ROOT / "sw.js").read_text("utf-8")
    assert 'new Request(file, { cache: "reload" })' in source

def test_an_old_cache_never_leaks_into_the_running_version():
    # Owner, 2026-10-07: "Can't load". The worker answered from every cache, so an old version's
    # cache could serve old files to a new version. Plant a stale version.js in an older cache.
    with open_app(service_workers="allow", route=None) as (page, _, _):
        page.evaluate("navigator.serviceWorker.ready")
        page.reload()
        wait_until(page, "navigator.serviceWorker.controller !== null", 5000)
        current = page.evaluate("self.FREELIEF_VERSION")
        # Remove version.js from the current cache, so a lookup across every cache can only find the
        # stale copy. The worker must miss its own cache and fetch the current file instead.
        page.evaluate("""(async () => {
            const own = await caches.open('freelief-' + self.FREELIEF_VERSION);
            for (const key of await own.keys()) if (key.url.endsWith('/version.js')) await own.delete(key);
            const old = await caches.open('freelief-0.0.0-stale');
            await old.put(new Request('version.js'), new Response('self.FREELIEF_VERSION = "0.0.0";',
                { headers: { 'Content-Type': 'text/javascript' } }));
        })()""")
        page.reload()
        page.wait_for_selector("html[data-ready='true']", timeout=5000)
        assert page.evaluate("self.FREELIEF_VERSION") == current, "a stale cache must not be read"


def test_an_update_reloads_the_page_onto_the_new_version_before_any_touch():
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        app = Path(temp) / "app"
        shutil.copytree(ROOT, app, ignore=shutil.ignore_patterns(
            ".git", ".venv", "output", "input", "docs", "tools", "__pycache__", ".claude", ".github"))
        url = serve(app)
        context = browser().new_context(service_workers="allow")
        try:
            page = context.new_page()
            page.goto(url)
            page.evaluate("navigator.serviceWorker.ready")
            page.reload()
            wait_until(page, "navigator.serviceWorker.controller !== null", 5000)
            (app / "version.js").write_text('self.FREELIEF_VERSION = "9.9.8";\n', "utf-8")
            page.reload()  # the browser checks the worker on navigation, installs it, and it takes over
            wait_until(page, "self.FREELIEF_VERSION === '9.9.8'", 10000)
            page.wait_for_selector("html[data-ready='true']", timeout=5000)
        finally:
            context.close()

def test_settings_shows_the_version_and_update_now_refreshes_only_freelief():
    # Owner, 2026-10-07: "a force update to the settings and a build version shown there".
    with open_app(service_workers="allow", route="settings") as (page, _, _):
        version = page.evaluate("self.FREELIEF_VERSION")
        assert page.locator(".version-line").inner_text() == f"Version {version}"
        page.evaluate("navigator.serviceWorker.ready")
        page.evaluate(f"Promise.all([caches.open('{FOREIGN_CACHE}'), caches.open('freelief-0.0.0-old')])")
        page.context.set_offline(True)
        page.locator(".update-now").click()
        assert page.locator(".update-status").inner_text() == "You need an internet connection to update."
        page.context.set_offline(False)
        with page.expect_navigation(timeout=8000):
            page.locator(".update-now").click()
        wait_until(page, "document.documentElement.dataset.ready === 'true'", 8000)
        wait_until(page, f"caches.has('freelief-' + self.FREELIEF_VERSION)", 8000)
        keys = page.evaluate("caches.keys()")
        assert FOREIGN_CACHE in keys, "another app's cache survives"
        assert "freelief-0.0.0-old" not in keys, keys


def test_update_now_on_a_captive_connection_keeps_the_offline_copy():
    # AUD-056: the device reports that it is online, but the network does not give Freelief back:
    # a captive portal answers every address with its own page. A route cannot stand in for this,
    # because the browser fetches the worker script outside the page, so the served copy changes.
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        app = Path(temp) / "app"
        shutil.copytree(ROOT, app, ignore=shutil.ignore_patterns(
            ".git", ".venv", "output", "input", "docs", "tools", "__pycache__", ".claude", ".github"))
        url = serve(app)
        context = browser().new_context(service_workers="allow")
        try:
            page = context.new_page()
            page.goto(url + "#settings")
            page.evaluate("navigator.serviceWorker.ready")
            page.reload()
            wait_until(page, "navigator.serviceWorker.controller !== null", 5000)
            page.wait_for_selector("html[data-ready='true']", timeout=5000)
            own = page.evaluate("'freelief-' + self.FREELIEF_VERSION")
            (app / "sw.js").write_text("<html><body>Sign in to the Wi-Fi</body></html>", "utf-8")
            page.locator(".update-now").click()
            wait_until(page, "document.querySelector('.update-status')?.textContent.startsWith('Could not')", 8000)
            assert page.locator(".update-status").inner_text() == "Could not update. This version still works offline."
            assert page.evaluate(f"caches.has('{own}')"), "the offline copy is kept"
            assert page.evaluate("navigator.serviceWorker.getRegistration().then(r => Boolean(r))")
            context.set_offline(True)
            page.reload()
            page.wait_for_selector("html[data-ready='true']", timeout=5000)
            assert page.locator(".help-open").is_visible(), "it still works offline"
        finally:
            context.close()
