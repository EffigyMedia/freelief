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


def test_the_manifest_makes_the_app_installable():
    import json
    manifest = json.loads((ROOT / "manifest.webmanifest").read_text("utf-8"))
    sizes = {icon["sizes"] for icon in manifest["icons"]}
    assert {"192x192", "512x512"} <= sizes
    assert manifest["display"] == "standalone"
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
            page.evaluate("navigator.serviceWorker.getRegistration().then(r => r.update())")
            wait_until(page, "caches.has('freelief-9.9.9')", 8000)
            wait_until(page, f"caches.has('{old}').then(present => !present)", 8000)
            keys = page.evaluate("caches.keys()")
            assert FOREIGN_CACHE in keys, keys
            assert "freelief-9.9.9" in keys and old not in keys, keys
        finally:
            context.close()

def test_precache_bypasses_the_http_cache():
    # AUD-013: a new version must not store an old file from the browser's HTTP cache.
    source = (ROOT / "sw.js").read_text("utf-8")
    assert 'new Request(file, { cache: "reload" })' in source