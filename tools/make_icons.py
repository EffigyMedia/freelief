"""Render icons/icon-192.png and icons/icon-512.png from icons/icon.svg.

The PNGs ship (home-screen install needs them), so they are committed beside the SVG.
Run with the project venv:  .venv/Scripts/python tools/make_icons.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "tests"))
from harness import browser as test_browser  # noqa: E402  the same browser as the tests (AUD-012)

ROOT = Path(__file__).resolve().parent.parent
SVG = (ROOT / "icons" / "icon.svg").read_text("utf-8")


def main() -> None:
    browser = test_browser()
    for size in (192, 512):
        page = browser.new_page(viewport={"width": size, "height": size})
        page.set_content(f'<style>html,body{{margin:0}}svg{{display:block;width:{size}px;'
                         f'height:{size}px}}</style>{SVG}')
        page.screenshot(path=str(ROOT / "icons" / f"icon-{size}.png"))
        page.close()
    print("[ OK ] icons/icon-192.png and icons/icon-512.png written")


if __name__ == "__main__":
    main()
