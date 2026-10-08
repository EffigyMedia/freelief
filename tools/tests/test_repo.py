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


def test_every_research_source_is_recorded_in_sources_md():
    # AUD-063: docs/research/sources.md is the written record behind data/research.json. Each source
    # must appear there under its id and with its DOI link, so the two cannot drift apart again.
    research = json.loads((freelief.ROOT / "data" / "research.json").read_text("utf-8"))
    record = (freelief.ROOT / "docs" / "research" / "sources.md").read_text("utf-8")
    cited = {sid for technique in research["techniques"] for sid in technique["sources"]}
    assert cited, "data/research.json cites no source"
    missing = [sid for sid in sorted(cited | set(research["sources"]))
               if f"[{sid}]" not in record or research["sources"][sid]["url"] not in record]
    assert not missing, f"sources missing from docs/research/sources.md (id or DOI link): {missing}"


def _design_without_history():
    # The Decision Log and the Change Log keep superseded figures on purpose, as history.
    text = (freelief.ROOT / "docs" / "Design_Document.md").read_text("utf-8")
    text = re.sub(r"\n## 12\. Decision Log\n.*?(?=\n## 13\.)", "\n", text, flags=re.S)
    return re.sub(r"\n## 15\. Change Log\n.*", "\n", text, flags=re.S)


def test_the_design_size_limit_equals_req_028():
    # AUD-065: the design stated 150 KB after REQ-028 was raised to 250 KB.
    record = (freelief.ROOT / "docs" / "fragments" / "REQ-028.md").read_text("utf-8")
    heading = re.search(r"^### REQ-028\b.*$", record, re.M)
    assert heading, "REQ-028.md has no requirement heading"
    limit = re.search(r"under\s+(\d+(?:\.\d+)?)\s*KB", heading.group(0))
    assert limit, "the REQ-028 heading states no 'under N KB' figure"
    figures = re.findall(r"(?:under|REQ-028\s*\()\s*(\d+(?:\.\d+)?)\s*KB", _design_without_history())
    assert figures, "the design states no size limit outside its history"
    wrong = sorted({f for f in figures if f != limit.group(1)})
    assert not wrong, f"design size figures {wrong} differ from REQ-028 ({limit.group(1)} KB)"


# AUD-067: the plain word in about.privacy2 for each setting that settings.js stores.
PRIVACY_WORDS = {
    "rhythm": "rhythm",
    "sounds": "sound",
    "theme": "colors",
    "calmMode": "Visualizer",
    "helpRegion": "country",
    "haptics": "vibration",
    "openOn": "opens",
}


def test_the_privacy_text_names_everything_settings_stores():
    source = (freelief.ROOT / "settings.js").read_text("utf-8")
    block = re.search(r"\bdefaults\s*=\s*\{([^}]+)\};", source)
    assert block, "settings.js has no defaults object"
    keys = re.findall(r"^\s*(\w+)\s*:", block.group(1), re.M)
    assert keys, "the defaults object in settings.js holds no key"
    unmapped = [k for k in keys if k not in PRIVACY_WORDS]
    assert not unmapped, f"stored settings with no privacy word; add them to PRIVACY_WORDS and about.privacy2: {unmapped}"
    privacy = json.loads((freelief.ROOT / "strings" / "en.json").read_text("utf-8"))["about.privacy2"]
    absent = [f"{k} ({PRIVACY_WORDS[k]!r})" for k in keys if PRIVACY_WORDS[k].lower() not in privacy.lower()]
    assert not absent, f"about.privacy2 does not name: {absent}"


CSP = ("default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; "
       "connect-src 'self'; worker-src 'self'; manifest-src 'self'; base-uri 'self'; form-action 'none'")


def test_the_content_security_policy_is_exactly_the_reviewed_one():
    # AUD-031: a weakened policy fails here, not silently.
    html = (freelief.ROOT / "index.html").read_text("utf-8")
    found = re.findall(r'http-equiv="Content-Security-Policy" content="([^"]+)"', html)
    assert found == [CSP], found


# Every address written in shipped code, except the ones listed here with their reason (AUD-031).
URL_ALLOWED = {
    "http://www.w3.org/2000/svg",   # the SVG namespace, not a request
    "https://findahelpline.com/",   # the static fallback's directory link, which the person chooses
}


def test_shipped_code_names_no_other_address():
    hits = []
    for path in freelief.ROOT.rglob("*"):
        rel = path.relative_to(freelief.ROOT).as_posix()
        if path.suffix not in {".js", ".html", ".css"} or rel.split("/")[0] in {"tools", "docs", ".venv", "output", "input", ".github"}:
            continue
        for url in re.findall(r"https?://[^\"' )<>`]+", path.read_text("utf-8")):
            if url not in URL_ALLOWED:
                hits.append(f"{rel}: {url}")
    assert not hits, "an address in shipped code that is not on the allow-list: " + "; ".join(hits)


def test_every_committed_shipped_change_came_with_a_version_bump():
    # AUD-010: an installed app keeps its cache until the version changes, so a shipped file changed
    # after the last bump would never reach it. Commit each shipped change with a bump.
    late = freelief.changed_since_version_bump()
    assert not late, "shipped files changed after the last version bump: " + ", ".join(late)


def test_the_crisis_date_check_finds_an_old_date():
    import datetime
    far_future = datetime.date(2100, 1, 1)
    stale = freelief.stale_crisis_checks(30, today=far_future)
    assert any(item.startswith("directory") for item in stale), stale
    assert len(stale) > 1
    assert freelief.stale_crisis_checks(10**6) == []
