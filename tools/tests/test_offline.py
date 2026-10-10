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
        # Every screen is checked (AUD-027); ROUTES in app.js is the list.
        for route in ("menu", "breathe", "bubbles", "garden", "unblock", "ripple", "mandala", "calm", "settings", "about", "feedback"):
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


def _app_copy(temp):
    import shutil
    app = Path(temp) / "app"
    shutil.copytree(ROOT, app, ignore=shutil.ignore_patterns(
        ".git", ".venv", "output", "input", "docs", "tools", "__pycache__", ".claude", ".github"))
    return app


def test_after_a_touch_a_new_version_waits_and_the_session_keeps_its_own_files():
    # AUD-057: an update after the person has touched the app must not mix versions. The page keeps
    # the version it started with, a lazy screen still loads, and the next open gets the new version.
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        app = _app_copy(temp)
        url = serve(app)
        context = browser().new_context(service_workers="allow")
        try:
            page = context.new_page()
            page.goto(url + "#menu")
            page.evaluate("navigator.serviceWorker.ready")
            page.reload()
            wait_until(page, "navigator.serviceWorker.controller !== null", 5000)
            page.wait_for_selector("html[data-ready='true']", timeout=5000)
            old = page.evaluate("self.FREELIEF_VERSION")
            page.locator(".menu-item").first.click()  # a touch
            (app / "version.js").write_text('self.FREELIEF_VERSION = "9.9.7";\n', "utf-8")
            mandala = app / "activities" / "mandala.js"
            mandala.write_text(mandala.read_text("utf-8").replace("export function start", "export function start_renamed"), "utf-8")
            page.evaluate("navigator.serviceWorker.getRegistration().then(r => r.update())")
            wait_until(page, "navigator.serviceWorker.getRegistration().then(r => Boolean(r.waiting))", 10000)
            page.wait_for_timeout(500)
            assert page.evaluate("self.FREELIEF_VERSION") == old, "the page was not reloaded under the person"
            page.evaluate("location.hash = 'mandala'")
            wait_until(page, "document.querySelector('main').dataset.shown === 'mandala'", 5000)
            assert page.locator(".mandala-part").count() > 0, "the old version's screen loads from its own cache"
            page.close()
            fresh = context.new_page()  # the next open
            fresh.goto(url + "#menu")
            wait_until(fresh, "self.FREELIEF_VERSION === '9.9.7'", 10000)
        finally:
            context.close()



def _installed(context, url):
    page = context.new_page()
    page.goto(url + "#menu")
    page.evaluate("navigator.serviceWorker.ready")
    page.reload()
    wait_until(page, "navigator.serviceWorker.controller !== null", 5000)
    page.wait_for_selector("html[data-ready='true']", timeout=5000)
    return page


def _deploy(app, version, broken_mandala=True):
    (app / "version.js").write_text(f'self.FREELIEF_VERSION = "{version}";\n', "utf-8")
    if broken_mandala:
        mandala = app / "activities" / "mandala.js"
        mandala.write_text(mandala.read_text("utf-8").replace("export function start", "export function start_renamed"), "utf-8")


def test_a_second_window_does_not_take_the_version_from_a_window_in_use():
    # AUD-057, re-checked in round UNT-082: page A is touched, a new version waits, and page B opens
    # fresh. The new version must not take over while A is open, so A keeps its own cache and files.
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        app = _app_copy(temp)
        url = serve(app)
        context = browser().new_context(service_workers="allow")
        try:
            a = _installed(context, url)
            old = a.evaluate("self.FREELIEF_VERSION")
            a.locator("h1").first.click()  # a touch that opens no screen
            _deploy(app, "9.9.7")
            a.evaluate("navigator.serviceWorker.getRegistration().then(r => r.update())")
            wait_until(a, "navigator.serviceWorker.getRegistration().then(r => Boolean(r.waiting))", 10000)
            b = context.new_page()  # a second window opens fresh
            b.goto(url + "#menu")
            b.wait_for_selector("html[data-ready='true']", timeout=5000)
            # Under Playwright a takeover that the waiting worker allowed completes only once the
            # worker runs again, so wake every worker before the check. Without this, the old
            # worker's takeover never shows and the test cannot fail.
            for worker in context.service_workers:
                worker.evaluate("[self.registration.waiting && self.registration.waiting.state, self.registration.active && self.registration.active.state]")
            b.wait_for_timeout(3000)
            assert a.evaluate(f"caches.has('freelief-{old}')"), "the old cache was deleted under page A"
            a.evaluate("location.hash = 'mandala'")
            wait_until(a, "document.querySelector('main').dataset.shown === 'mandala'", 5000)
            assert a.locator(".mandala-part").count() > 0, "page A loads its screens from its own version"
            a.close()
            b.close()
            c = context.new_page()  # every window closed: the next open gets the new version
            c.goto(url + "#menu")
            wait_until(c, "self.FREELIEF_VERSION === '9.9.7'", 10000)
        finally:
            context.close()


def test_update_now_beside_another_window_asks_to_close_it():
    # AUD-057: the person asked, but another window may be in use, so Settings says what to do.
    import json as _json
    strings = _json.loads((ROOT / "strings" / "en.json").read_text("utf-8"))
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        app = _app_copy(temp)
        url = serve(app)
        context = browser().new_context(service_workers="allow")
        try:
            a = _installed(context, url)
            other = context.new_page()
            other.goto(url + "#menu")
            other.wait_for_selector("html[data-ready='true']", timeout=5000)
            other.locator(".menu-item").first.click()
            _deploy(app, "9.9.6", broken_mandala=False)
            a.evaluate("location.hash = 'settings'")
            wait_until(a, "document.querySelector('main').dataset.shown === 'settings'", 5000)
            a.locator(".update-now").click()
            wait_until(a, f"document.querySelector('.update-status').textContent === {_json.dumps(strings['settings.updateOtherWindows'])}", 10000)
            assert other.evaluate("self.FREELIEF_VERSION") != "9.9.6"
        finally:
            context.close()


def test_a_newer_deploy_is_never_stored_in_the_running_versions_cache():
    # AUD-120: a cache miss or a repair fetches from the network. When a newer version is deployed,
    # the old worker must not store the new files under its own cache name.
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        app = _app_copy(temp)
        url = serve(app)
        context = browser().new_context(service_workers="allow")
        try:
            page = _installed(context, url)
            page.locator(".menu-item").first.click()  # a touch, so no new version takes over
            page.evaluate("location.hash = 'menu'")
            old = page.evaluate("self.FREELIEF_VERSION")
            has_calm = f"caches.open('freelief-{old}').then(c => c.match('activities/calm.js')).then(Boolean)"
            page.evaluate(f"caches.open('freelief-{old}').then(c => c.delete('activities/calm.js'))")
            assert not page.evaluate(has_calm)
            _deploy(app, "9.9.8", broken_mandala=False)
            page.evaluate("location.hash = 'calm'")  # a miss, fetched from the network
            wait_until(page, "document.querySelector('main').dataset.shown === 'calm'", 5000)
            page.evaluate("navigator.serviceWorker.controller.postMessage('heal')")
            page.wait_for_timeout(1500)
            assert not page.evaluate(has_calm), "a file of the newer deploy went into the old cache"
            _deploy(app, old, broken_mandala=False)  # the network serves this version again
            page.evaluate("navigator.serviceWorker.controller.postMessage('heal')")
            wait_until(page, has_calm, 8000)
        finally:
            context.close()

def test_a_screen_that_cannot_load_falls_back_and_fixes_the_address():
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        app = _app_copy(temp)
        (app / "activities" / "ripple.js").unlink()
        url = serve(app)
        context = browser().new_context(service_workers="block")
        try:
            page = context.new_page()
            page.goto(url + "#menu")
            page.wait_for_selector("html[data-ready='true']", timeout=5000)
            page.evaluate("location.hash = 'ripple'")
            wait_until(page, "document.querySelector('main').dataset.shown === 'menu'", 5000)
            assert page.evaluate("location.hash") == "#menu", "the address names the screen shown"
            page.locator(".menu-item[href='#ripple']").click()
            wait_until(page, "document.querySelector('main').dataset.shown === 'menu'", 5000)
        finally:
            context.close()


def test_a_cache_fault_falls_back_to_the_network_and_a_repair_reply_is_heard():
    # AUD-059: a rejecting Cache Storage must not answer every request with a network error.
    source = (ROOT / "sw.js").read_text("utf-8")
    assert "}).catch(() => fetch(event.request))" in source
    # AUD-060: the page listens for the worker's repair reply.
    shell = (ROOT / "app.js").read_text("utf-8")
    assert "event.data.heal === false" in shell
    with open_app(service_workers="allow", route="menu") as (page, errors, _):
        page.evaluate("navigator.serviceWorker.ready")
        page.reload()
        wait_until(page, "navigator.serviceWorker.controller !== null", 5000)
        page.wait_for_selector("html[data-ready='true']", timeout=5000)
        assert not [e for e in errors if "repair" in e], "a working repair reports nothing"


def test_an_update_gets_past_the_http_cache_and_works_offline():
    # AUD-013 and AUD-009: under GitHub Pages' caching (max-age=600) a new version must reach the
    # device, replace the changed files, and then run offline.
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        app = _app_copy(temp)
        url = serve(app, cache_control="max-age=600")
        context = browser().new_context(service_workers="allow")
        try:
            page = context.new_page()
            page.goto(url + "#menu")
            page.evaluate("navigator.serviceWorker.ready")
            page.reload()
            wait_until(page, "navigator.serviceWorker.controller !== null", 5000)
            page.evaluate("location.hash = 'about'")
            wait_until(page, "document.querySelector('main').dataset.shown === 'about'", 5000)
            (app / "version.js").write_text('self.FREELIEF_VERSION = "9.9.5";\n', "utf-8")
            strings = app / "strings" / "en.json"
            strings.write_text(strings.read_text("utf-8").replace('"About Freelief"', '"About Freelief 9.9.5"'), "utf-8")
            page.reload()  # before any touch, the new version takes over and the page reloads once
            wait_until(page, "self.FREELIEF_VERSION === '9.9.5'", 15000)
            page.wait_for_selector("html[data-ready='true']", timeout=5000)
            context.set_offline(True)
            page.reload()
            page.wait_for_selector("html[data-ready='true']", timeout=5000)
            assert page.evaluate("self.FREELIEF_VERSION") == "9.9.5"
            page.evaluate("location.hash = 'about'")
            wait_until(page, "document.querySelector('main').dataset.shown === 'about'", 5000)
            assert "About Freelief 9.9.5" in page.locator("main h1").inner_text(), "the changed file, not the HTTP-cached one"
        finally:
            context.close()


def test_the_offline_copy_is_asked_to_be_kept_without_holding_up_the_start():
    # AUD-080: best-effort storage can be evicted on a full phone. Freelief asks to keep it, where the
    # browser decides without a question, and the call never delays the start.
    probe = """
window.__persist = 0;
Object.defineProperty(navigator, 'storage', { configurable: true, value: {
  persisted: () => Promise.resolve(false),
  persist: () => { window.__persist += 1; return new Promise(() => {}); },
  estimate: () => Promise.resolve({}),
} });"""
    with open_app(init_script=probe) as (page, errors, _):
        assert page.evaluate("document.documentElement.dataset.ready") == "true", "a call that never ends does not block"
        wait_until(page, "window.__persist === 1", 2000)
        assert not errors, errors


def test_an_update_found_while_breathing_runs_waits_for_the_next_open():
    # AUD-107: with "Start breathing at once", a reload would restart the breath being followed.
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
            page.evaluate("localStorage.setItem('freelief.settings.v2', JSON.stringify({ openOn: 'breathe' }))")
            page.evaluate("navigator.serviceWorker.ready")
            page.reload()
            wait_until(page, "navigator.serviceWorker.controller !== null", 5000)
            old = page.evaluate("self.FREELIEF_VERSION")
            (app / "version.js").write_text('self.FREELIEF_VERSION = "9.9.7";\n', "utf-8")
            page.reload()  # the new version installs; breathing runs at once, so it must wait
            page.wait_for_selector("html[data-ready='true']", timeout=5000)
            assert page.evaluate("document.querySelector('main').dataset.screen") == "breathe"
            page.evaluate("window.__still = true")
            page.wait_for_timeout(4000)
            assert page.evaluate("window.__still === true"), "the page did not reload under the breathing"
            assert page.evaluate("self.FREELIEF_VERSION") == old
        finally:
            context.close()
