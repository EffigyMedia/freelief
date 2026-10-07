"""Repository rules that hold for every file that ships, whatever the slice."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import freelief  # noqa: E402

TEXT_SUFFIXES = {".html", ".js", ".css", ".json", ".webmanifest", ".svg"}

# REQ-025: Freelief never says it is clinically proven, treats, cures or diagnoses.
FORBIDDEN_CLAIMS = re.compile(
    r"clinically[- ]proven|proven to|\b(treats?|treatment|cures?|diagnos\w*|therapy for)\b",
    re.IGNORECASE)

# REQ-015 and REQ-019: no file that ships loads anything from another origin.
EXTERNAL_LOAD = re.compile(
    r"""(<script[^>]+src=|<link[^>]+href=|@import\s|url\(|fetch\(|importScripts\()\s*["']?https?://""",
    re.IGNORECASE)


def shipped_text():
    for path in freelief.shipped_files():
        if path.suffix in TEXT_SUFFIXES:
            yield path, path.read_text("utf-8")


def test_version_has_one_valid_home():
    assert freelief.read_version() is not None, "version.js must hold FREELIEF_VERSION = \"X.Y.Z\""


def test_no_forbidden_health_claims():
    hits = [f"{p.relative_to(freelief.ROOT)}: {m.group(0)!r}"
            for p, text in shipped_text() for m in FORBIDDEN_CLAIMS.finditer(text)]
    assert not hits, "forbidden claim wording (REQ-025): " + "; ".join(hits)


def test_nothing_loads_from_another_origin():
    hits = [str(p.relative_to(freelief.ROOT)) for p, text in shipped_text() if EXTERNAL_LOAD.search(text)]
    assert not hits, "external load in shipped files (REQ-015, REQ-019): " + ", ".join(hits)


def test_license_is_mit():
    text = (freelief.ROOT / "LICENSE").read_text("utf-8")
    assert text.startswith("MIT License"), "LICENSE must be the MIT license (REQ-031)"
