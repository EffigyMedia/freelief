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
CLAIM_EXEMPT_STRINGS = {"about.selfHelp1"}
CLAIM_EXEMPT_FILES = set()


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



def test_the_design_version_has_a_change_log_entry():
    # AUD-045 and AUD-126: Document Control named version 1.3 while the Change Log ended at 1.2.
    text = (freelief.ROOT / "docs" / "Design_Document.md").read_text("utf-8")
    version = re.search(r"^- \*\*Version:\*\* (\d+\.\d+),", text, re.M)
    assert version, "Document Control states no version"
    log = text.split("\n## 15. Change Log\n", 1)
    assert len(log) == 2, "the design has no Change Log"
    assert f"- **v{version.group(1)} — " in log[1], (
        f"the Change Log has no entry for design version {version.group(1)}")

# AUD-067: the plain word in about.privacy2 for each setting that settings.js stores.
PRIVACY_WORDS = {
    "rhythm": "rhythm",
    "sounds": "sound",
    "theme": "colors",
    "awakeMinutes": "screen stays on",
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


# AUD-007 (owner, 2026-10-08): every crisis number is pinned here as well as in the data file, so a
# change to a number needs two edits, and a wrong or tampered number fails the suite. Change a pin
# only together with data/crisis-lines.json and a source checked in that session (AGENTS.md).
CRISIS_PINS = {
    "US": {"emergency": "911", "lines": {"988 Suicide & Crisis Lifeline": ("988", "988", "https://chat.988lifeline.org/")}},
    "CA": {"emergency": "911", "lines": {"9-8-8 Suicide Crisis Helpline": ("988", "988", None)}},
    "GB": {"emergency": "999", "lines": {"Samaritans": ("116 123", None, None)}},
    "IE": {"emergency": "112 or 999", "lines": {"Samaritans": ("116 123", None, None)}},
    "AU": {"emergency": "000", "lines": {"Lifeline": ("13 11 14", "0477 13 11 14", None)}},
}


DIRECTORY_PIN = "https://findahelpline.com/"


def test_every_crisis_number_is_pinned():
    data = json.loads((freelief.ROOT / "data" / "crisis-lines.json").read_text("utf-8"))
    found = {code: {"emergency": region["emergency"],
                    "lines": {line["name"]: (line.get("call"), line.get("text"), line.get("web"))
                              for line in region["lines"]}}
             for code, region in data["regions"].items()}
    assert found == CRISIS_PINS, "a crisis number differs from its pin; check the source, then change both"
    # The directory is the one curated route for everyone outside the pinned regions (AUD-076).
    assert data["directory"]["url"] == DIRECTORY_PIN, "the directory link differs from its pin"


def test_the_copies_of_the_directory_link_and_the_fallback_rhythm_match_their_source():
    # AUD-099: the static fallback and config.json hold copies; they must not drift from the source.
    data = json.loads((freelief.ROOT / "data" / "crisis-lines.json").read_text("utf-8"))
    config = json.loads((freelief.ROOT / "config.json").read_text("utf-8"))
    url = data["directory"]["url"]
    assert config["crisis"]["directoryUrl"] == url, "config.json's directory link differs from the crisis data"
    page = (freelief.ROOT / "index.html").read_text("utf-8")
    fallback = page[page.index('id="fallback"'):]
    assert f'href="{url}"' in fallback, "the static fallback's directory link differs from the crisis data"
    rhythm = config["breathing"]["rhythms"][config["breathing"]["defaultRhythm"]]
    words = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}
    assert f"count to {words[rhythm['in']]}" in fallback and f"count to {words[rhythm['out']]}" in fallback, \
        "the fallback's breathing counts differ from the default rhythm"


def test_every_activity_is_on_the_menu_and_has_the_quiet_footer():
    # AUD-100: a new screen goes into four lists. The router and the worker are tested elsewhere.
    app = (freelief.ROOT / "app.js").read_text("utf-8")
    menu = (freelief.ROOT / "screens" / "menu.js").read_text("utf-8")
    routes = re.findall(r'^  (\w+): \(\) => import\([`"]\./(?:exercises|activities)/', app, re.M)
    assert routes, "app.js ROUTES lists no exercise or activity"
    quiet = re.search(r"QUIET_FOOTER = new Set\(\[([^\]]*)\]\)", app).group(1)
    items = re.findall(r'route: "(\w+)"', menu)
    for route in routes:
        assert route in items, f"{route} is not on the menu (screens/menu.js ITEMS)"
        assert f'"{route}"' in quiet, f"{route} does not have the quiet footer (app.js QUIET_FOOTER)"


def test_the_design_names_every_setting_that_is_stored():
    # AUD-092: the design's definition of Settings must list what settings.js stores.
    source = (freelief.ROOT / "settings.js").read_text("utf-8")
    keys = re.findall(r"^\s*(\w+)\s*:", re.search(r"\bdefaults\s*=\s*\{([^}]+)\};", source).group(1), re.M)
    design = (freelief.ROOT / "docs" / "Design_Document.md").read_text("utf-8")
    row = re.search(r"^\| \*\*Settings\*\* \|(.*)$", design, re.M).group(1)
    words = dict(PRIVACY_WORDS, sounds="sound", theme="theme", helpRegion="region", openOn="opens",
                 awakeMinutes="screen stays on")
    absent = [k for k in keys if words[k].lower() not in row.lower()]
    assert not absent, f"the design's Settings definition does not name: {absent}"


def test_agents_md_repeats_no_line():
    # AUD-117: a bad edit once doubled a line and dropped the rule after "They **must not**".
    text = (freelief.ROOT / "AGENTS.md").read_text("utf-8")
    lines = [l.strip() for l in text.splitlines() if len(l.strip()) > 40]
    # A doubled line may be a copy, or the start of the line above it with its end cut off.
    repeated = sorted({b for a, b in zip(lines, lines[1:]) if a.startswith(b)}
                      | {l for l in lines if lines.count(l) > 1})
    assert not repeated, f"AGENTS.md repeats a line: {repeated[:3]}"


def test_run_serves_only_shipped_files_and_only_to_this_machine():
    # AUD-118: the folder holds .git and input/excluded; a page on another host name must not reach it.
    import http.client
    import http.server
    import threading
    shipped = {p.relative_to(freelief.ROOT).as_posix() for p in freelief.shipped_files()}
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), freelief.run_handler(shipped))
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()

    def get(path, host=f"localhost:{freelief.PORT}"):
        connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
        connection.request("GET", path, headers={"Host": host})
        status = connection.getresponse().status
        connection.close()
        return status

    try:
        assert get("/") == 200 and get("/app.js") == 200 and get("/config.json?x=1") == 200
        assert get("/.git/HEAD") == 404, "git metadata is not served"
        assert get("/input/") == 404 and get("/docs/Design_Document.md") == 404 and get("/AGENTS.md") == 404
        assert get("/app.js", host="evil.example:8000") == 403, "a foreign Host is refused"
    finally:
        server.shutdown()
        server.server_close()


def test_doctor_reports_a_broken_config_instead_of_crashing():
    # AUD-119: a malformed config.json gives NOT READY and exit 1, not a traceback.
    import shutil
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        copy = Path(temp) / "app"
        shutil.copytree(freelief.ROOT, copy, ignore=shutil.ignore_patterns(".venv", "output", "input", ".git"))
        (copy / "config.json").write_text("{ not json", "utf-8")
        result = subprocess.run([sys.executable, str(copy / "tools" / "freelief.py"), "doctor"],
                                cwd=copy, capture_output=True, text=True)
        assert result.returncode == 1
        assert "Traceback" not in result.stdout + result.stderr, result.stderr[-800:]
        assert "NOT READY" in result.stdout


def test_bench_reads_the_baseline_load_it_compares_against():
    # AUD-134: a run is compared with the baseline only near the baseline's own load, so the load
    # must be recorded where bench reads it.
    import bench
    assert bench.BASELINE["load_percent"] is not None, "baseline.md has no 'Baseline load' line"
    assert bench.BASELINE["load_percent"] + bench.COMPARABLE_MARGIN_POINTS <= 40


# AUD-142 and AUD-143: names the owner retired. A shipped string or an issue template that still
# uses one points a person or a volunteer at a screen that is gone.
RETIRED_NAMES = ["Visualizer", "Trace a shape", "Sort colors", "Standards and research", "colour sort"]


def test_no_shipped_string_or_template_names_a_retired_screen():
    texts = {"strings/en.json": (freelief.ROOT / "strings" / "en.json").read_text("utf-8")}
    for template in (freelief.ROOT / ".github" / "ISSUE_TEMPLATE").glob("*.md"):
        texts[template.relative_to(freelief.ROOT).as_posix()] = template.read_text("utf-8")
    found = [f"{name} in {path}" for path, text in texts.items() for name in RETIRED_NAMES
             if name.lower() in text.lower()]
    assert not found, found


def test_the_accessibility_template_lists_the_same_screens_as_the_app():
    # AUD-143: the issue template and the in-app checklist are twins; they list the same screens.
    import json
    app = json.loads((freelief.ROOT / "strings" / "en.json").read_text("utf-8"))["feedback.template.accessibility"]
    template = (freelief.ROOT / ".github" / "ISSUE_TEMPLATE" / "accessibility-check.md").read_text("utf-8")
    in_app = re.findall(r"^\[ \] (.+)$", app, re.M)
    on_github = re.findall(r"^- \[ \] (.+)$", template, re.M)
    assert in_app and in_app == on_github, (in_app, on_github)


def test_the_test_server_serves_only_shipped_files_and_only_to_this_machine():
    # AUD-129: harness.serve(ROOT), which every browser test and the bench use, has the same two
    # refusals as `run`.
    import http.client
    from harness import serve
    url = serve(freelief.ROOT)
    port = int(url.rstrip("/").rsplit(":", 1)[1])

    def get(path, host=f"localhost:{port}"):
        connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
        connection.request("GET", path, headers={"Host": host})
        status = connection.getresponse().status
        connection.close()
        return status

    assert get("/") == 200 and get("/app.js") == 200 and get("/activities/calm.js?v=1") == 200
    assert get("/.git/HEAD") == 404 and get("/.venv/pyvenv.cfg") == 404 and get("/AGENTS.md") == 404
    assert get("/app.js", host="evil.example") == 403, "a foreign Host is refused"
