"""Render icons/icon-192.png and icons/icon-512.png from icons/icon.svg.

The PNGs ship (home-screen install needs them), so they are committed beside the SVG.
Run with the project venv:  .venv/Scripts/python tools/make_icons.py
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SVG = (ROOT / "icons" / "icon.svg").read_text("utf-8")


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        for size in (192, 512):
            page = browser.new_page(viewport={"width": size, "height": size})
            page.set_content(f'<style>html,body{{margin:0}}svg{{display:block;width:{size}px;'
                             f'height:{size}px}}</style>{SVG}')
            page.screenshot(path=str(ROOT / "icons" / f"icon-{size}.png"))
            page.close()
        browser.close()
    print("[ OK ] icons/icon-192.png and icons/icon-512.png written")


if __name__ == "__main__":
    main()
