"""Repository rules that hold for every file that ships, whatever the slice."""

import json
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


# The only text allowed to use claim words, each for a stated reason. Anything else fails.
# - The disclaimer says what Freelief does NOT do ("does not diagnose or treat"). REQ-006.
# - Research citations quote the titles of published papers as they are. REQ-024.
CLAIM_EXEMPT_STRINGS = {"about.selfHelp1"}
CLAIM_EXEMPT_FILES = {"data/research.json"}


def shipped_text():
    for path in freelief.shipped_files():
        if path.suffix in TEXT_SUFFIXES:
            yield path, path.read_text("utf-8")


def claim_text():
    """Shipped text that must make no health claim, with the stated exemptions taken out."""
    import json
    for path, text in shipped_text():
        relative = path.relative_to(freelief.ROOT).as_posix()
        if relative in CLAIM_EXEMPT_FILES:
            continue
        if relative.startswith("strings/") and relative.endswith(".json"):
            table = json.loads(text)
            text = json.dumps({k: v for k, v in table.items() if k not in CLAIM_EXEMPT_STRINGS})
        yield path, text


def test_version_has_one_valid_home():
    assert freelief.read_version() is not None, "version.js must hold FREELIEF_VERSION = \"X.Y.Z\""


def test_no_forbidden_health_claims():
    hits = [f"{p.relative_to(freelief.ROOT)}: {m.group(0)!r}"
            for p, text in claim_text() for m in FORBIDDEN_CLAIMS.finditer(text)]
    assert not hits, "forbidden claim wording (REQ-025): " + "; ".join(hits)


def test_nothing_loads_from_another_origin():
    hits = [str(p.relative_to(freelief.ROOT)) for p, text in shipped_text() if EXTERNAL_LOAD.search(text)]
    assert not hits, "external load in shipped files (REQ-015, REQ-019): " + ", ".join(hits)


def test_license_is_mit():
    text = (freelief.ROOT / "LICENSE").read_text("utf-8")
    assert text.startswith("MIT License"), "LICENSE must be the MIT license (REQ-031)"


def test_the_claim_exemptions_still_say_not():
    # An exempt string earns its exemption only by denying the claim. If it stops saying "not",
    # the exemption would hide a real claim.
    import json
    table = json.loads((freelief.ROOT / "strings" / "en.json").read_text("utf-8"))
    for key in CLAIM_EXEMPT_STRINGS:
        assert key in table, f"exempt key {key} no longer exists; remove it from the exemptions"
        hits = FORBIDDEN_CLAIMS.findall(table[key])
        if hits:
            assert re.search(r"\b(not|no)\b", table[key]), f"{key} uses claim words without a denial"

BRITISH = re.compile(r"\b(colour|centre|licence|behaviour|favourite|grey|organis|recognis|visualis)", re.I)


def test_user_facing_text_uses_american_spelling():
    # Owner, 2026-10-07: American spelling across the app. Code identifiers are not user-facing.
    strings = json.loads((freelief.ROOT / "strings" / "en.json").read_text("utf-8"))
    texts = [v for v in strings.values() if isinstance(v, str)]
    texts += [v for v in strings.values() if isinstance(v, list) for v in v]
    texts += [(freelief.ROOT / name).read_text("utf-8") for name in ("index.html", "manifest.webmanifest")]
    found = sorted({m.group(0) for text in texts for m in BRITISH.finditer(text)})
    assert not found, f"British spelling in user-facing text: {found}"


def test_no_exercise_or_activity_touches_settings_or_storage():
    # AGENTS.md and AUD-066: exercises and activities get settings through ctx from the shell.
    offenders = []
    for folder in ("exercises", "activities"):
        for path in (freelief.ROOT / folder).glob("*.js"):
            text = path.read_text("utf-8")
            if "settings.js" in text or "localStorage" in text or "sessionStorage" in text:
                offenders.append(path.name)
    assert not offenders, f"touches settings or storage directly: {offenders}"
