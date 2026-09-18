"""Rebuild original diagram PNGs without an image-generation API.

Run with Python, Pillow and Noto Sans CJK installed.
Uses the Korean face (index 1), Bold titles and Regular body text.
Runtime has no new dependencies.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from landing.build_note_images import COVERS  # noqa: E402

FONTS = Path("/usr/share/fonts/opentype/noto")
OUT = ROOT / "landing/static/landing/images/build-notes"


def build():
    OUT.mkdir(parents=True, exist_ok=True)

    def font(size, weight="Regular"):
        face = "Bold" if weight == "SemiBold" else "Regular"
        return ImageFont.truetype(str(FONTS / f"NotoSansCJK-{face}.ttc"), size, index=1)

    for key, title, subtitle, steps in set(COVERS.values()):
        image = Image.new("RGB", (1200, 630), "#f7f8fa")
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((64, 54, 72, 78), radius=4, fill="#2563eb")
        draw.text(
            (88, 54),
            "QUROOM  /  BUILD NOTES",
            font=font(22, "SemiBold"),
            fill="#2563eb",
        )
        draw.text((60, 125), title, font=font(64, "SemiBold"), fill="#142037")
        draw.text((64, 214), subtitle, font=font(28), fill="#647086")
        for index, step in enumerate(steps):
            x = 64 + index * 278
            draw.rounded_rectangle(
                (x, 320, x + 238, 487),
                radius=16,
                fill="#172b4d" if index == 3 else "#ffffff",
                outline="#172b4d" if index == 3 else "#e0e5ec",
                width=1,
            )
            draw.text(
                (x + 24, 346),
                f"0{index + 1}",
                font=font(21, "SemiBold"),
                fill="#9ebdf6" if index == 3 else "#647086",
            )
            draw.text(
                (x + 24, 405),
                step,
                font=font(34, "SemiBold"),
                fill="#ffffff" if index == 3 else "#17243b",
            )
            if index < 3:
                draw.line((x + 246, 399, x + 268, 399), fill="#2563eb", width=3)
                draw.polygon(
                    ((x + 268, 399), (x + 260, 393), (x + 260, 405)), fill="#2563eb"
                )
        draw.line((64, 541, 1136, 541), fill="#e0e5ec", width=1)
        draw.text((64, 565), "큐룸", font=font(22, "SemiBold"), fill="#17243b")
        draw.text((124, 566), "개발과 운영의 기록", font=font(21), fill="#647086")
        draw.text((1136, 566), "quroom.kr", font=font(21), fill="#647086", anchor="ra")
        path = OUT / f"{key}.png"
        image.save(path, optimize=True)
        print(f"{path.relative_to(ROOT)}: {path.stat().st_size:,} bytes")


if __name__ == "__main__":
    build()
