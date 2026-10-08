"""Write preview screenshots of the app to output/previews/ (phone and desktop, dark and light).

Run with the project venv:  .venv/Scripts/python tools/previews.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "tests"))
from harness import ROOT, open_app, wait_until  # noqa: E402

OUT = ROOT / "output" / "previews"
SCREENS = ["breathe", "menu", "bubbles", "trace", "sort", "ripple", "calm", "settings", "about", "standards", "feedback"]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for scheme in ("dark", "light"):
        for name, viewport in (("phone", {"width": 390, "height": 844}),
                               ("desktop", {"width": 1280, "height": 800})):
            with open_app(color_scheme=scheme, viewport=viewport, locale="en-GB") as (page, _, _):
                for screen in SCREENS:
                    page.evaluate(f"location.hash = '{screen}'")
                    wait_until(page, f"document.querySelector('main').dataset.shown === '{screen}'")
                    page.wait_for_timeout(2500 if screen == "breathe" else 200)
                    page.screenshot(path=str(OUT / f"{name}-{scheme}-{screen}.png"))
                page.locator(".help-open").click()
                page.wait_for_timeout(200)
                page.screenshot(path=str(OUT / f"{name}-{scheme}-help.png"))
    print(f"[ OK ] previews written to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
