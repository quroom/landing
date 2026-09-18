"""Render checked-in build-note SVG sources to 1200×630 PNG files.

The SVG files are the editable originals. They follow
codex-document/build-note-cover-standard.md. This authoring script requires
Playwright with Chromium and adds no production runtime dependency.
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIR = ROOT / "landing/static/landing/images/build-notes"
SOURCE_DIR = IMAGE_DIR / "sources"


def build() -> None:
    sources = sorted(SOURCE_DIR.glob("*.svg"))
    if not sources:
        raise SystemExit(f"No SVG sources found in {SOURCE_DIR}")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 630})
        for source in sources:
            target = IMAGE_DIR / f"{source.stem}.png"
            page.goto(source.as_uri())
            page.screenshot(path=target)
            print(f"{target.relative_to(ROOT)}: {target.stat().st_size:,} bytes")
        browser.close()


if __name__ == "__main__":
    build()
