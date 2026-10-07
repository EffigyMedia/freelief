"""Draw draft app icons to output/previews/icons/ for the owner to choose from.

Each draft is an SVG (the source) and PNGs at 512 and 48 pixels (to judge it as a home-screen icon
and as a browser-tab icon). The ensō is a brush stroke built as a filled shape: a circle swept
through most of a turn, with a width that swells and tapers like a brush, and a slight wobble.

Run with the project venv:  .venv/Scripts/python tools/icon_drafts.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "tests"))
from harness import ROOT, browser  # noqa: E402

OUT = ROOT / "output" / "previews" / "icons"
NIGHT = "#0f1626"
MIST = "#dfe8f4"
ACCENT = "#8fb8de"


def enso_path(cx=256, cy=256, r=150, start_deg=-18, sweep_deg=316, max_width=46, steps=240):
    """A filled brush-stroke circle: thick at the start, a long taper to a dry, thin end.

    The opening sits at the upper right (about half past one), as in brushed ensō. An opening
    straight up reads as a power button."""
    outer, inner = [], []
    for i in range(steps + 1):
        t = i / steps
        angle = math.radians(start_deg + sweep_deg * t)
        # The brush lands fast, swells, then lifts slowly.
        width = max_width * (min(1.0, t / 0.06) ** 0.6) * (1 - t) ** 0.55 + 3
        wobble = 4 * math.sin(t * math.pi * 3.0) + 2 * math.sin(t * math.pi * 7.0)
        radius = r + wobble
        cos, sin = math.cos(angle), math.sin(angle)
        outer.append((cx + (radius + width / 2) * cos, cy + (radius + width / 2) * sin))
        inner.append((cx + (radius - width / 2) * cos, cy + (radius - width / 2) * sin))
    points = outer + inner[::-1]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in points) + " Z"


def svg(body, background=NIGHT):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">'
            f'<rect width="512" height="512" fill="{background}"/>{body}</svg>\n')


DRAFTS = {
    "a-enso": svg(f'<path d="{enso_path()}" fill="{MIST}"/>'),
    "b-enso-breath": svg(
        f'<defs><radialGradient id="g"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0.9"/>'
        f'<stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient></defs>'
        f'<circle cx="256" cy="256" r="70" fill="url(#g)"/>'
        f'<path d="{enso_path()}" fill="{MIST}"/>'),
    "c-stones": svg(
        f'<ellipse cx="256" cy="352" rx="118" ry="44" fill="{ACCENT}" fill-opacity="0.55"/>'
        f'<ellipse cx="256" cy="276" rx="88" ry="36" fill="{ACCENT}" fill-opacity="0.75"/>'
        f'<ellipse cx="256" cy="212" rx="58" ry="28" fill="{MIST}"/>'
        f'<circle cx="256" cy="146" r="16" fill="{MIST}" fill-opacity="0.85"/>'),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    page = browser().new_page()
    tiles = []
    for name, source in DRAFTS.items():
        (OUT / f"{name}.svg").write_text(source, "utf-8")
        for size in (512, 48):
            page.set_viewport_size({"width": size, "height": size})
            page.set_content(f"<style>html,body{{margin:0}}svg{{display:block;width:{size}px;"
                             f"height:{size}px}}</style>{source}")
            page.screenshot(path=str(OUT / f"{name}-{size}.png"))
        tiles.append(source)
    # One sheet to compare: each draft large, with a tab-sized copy, and a rounded home-screen mask.
    cells = "".join(
        f'<figure><div class="big">{s}</div><div class="row"><div class="tab">{s}</div>'
        f'<span>{n}</span></div></figure>' for n, s in zip(DRAFTS, tiles))
    page.set_viewport_size({"width": 1020, "height": 420})
    page.set_content(
        "<style>body{margin:0;padding:20px;background:#e9e6df;font:16px system-ui;display:flex;gap:24px}"
        "figure{margin:0}.big svg{width:300px;height:300px;border-radius:66px;display:block}"
        ".row{display:flex;gap:12px;align-items:center;margin-top:12px}"
        ".tab svg{width:32px;height:32px;display:block;border-radius:6px}</style>" + cells)
    page.screenshot(path=str(OUT / "sheet.png"))
    page.close()
    print(f"[ OK ] drafts written to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
