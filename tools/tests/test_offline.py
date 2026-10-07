"""The installable offline app (REQ-008): the cache list is complete and the app runs offline."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import freelief  # noqa: E402
from harness import ROOT, open_app, wait_until  # noqa: E402

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
    with open_app(service_workers="allow") as (page, _, _):
        page.evaluate("navigator.serviceWorker.ready")
        page.reload()
        wait_until(page, "navigator.serviceWorker.controller !== null", 5000)
        page.context.set_offline(True)
        page.reload()
        page.wait_for_selector("html[data-ready='true']", timeout=5000)
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
