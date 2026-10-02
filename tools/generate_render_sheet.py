#!/usr/bin/env python3
"""Generate an annual render sheet inside rez env aswf. Requires Pillow >= 10.1."""

import argparse
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


SCENES = (("McUsd", "McUsd"), ("chess_set", "OpenChessSet"),
          ("entry", "ALab"), ("island", "Moana Island"))


def font(size):
    for path in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                 "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def centered(draw, box, text, text_font, color="#272727"):
    left, top, right, bottom = draw.textbbox((0, 0), text, font=text_font)
    x = box[0] + (box[2] - box[0] - right + left) // 2 - left
    y = box[1] + (box[3] - box[1] - bottom + top) // 2 - top
    draw.text((x, y), text, font=text_font, fill=color)


def generate(checkout, output):
    versions = {package: os.environ[f"REZ_{package}_VERSION"] for package in
                ("ASWF", "OPENUSD", "OPENMOONRAY", "CYCLES")}
    year = versions["ASWF"]
    labels = ("Storm " + versions["OPENUSD"],
              "MoonRay " + versions["OPENMOONRAY"],
              "Cycles " + versions["CYCLES"])
    image_root = checkout / "renderers"
    if not image_root.is_dir():
        raise ValueError(f"Missing image directory: {image_root}")
    folders = ("Storm" if (image_root / "Storm").is_dir() else "GL",
               "Moonray", "Cycles")

    margin, gap, label_width, tile_width, tile_height = 42, 14, 170, 760, 428
    title_height, heading_height = 82, 42
    width = 2 * margin + label_width + gap + 3 * tile_width + 2 * gap
    top = margin + title_height + heading_height + gap
    height = top + 4 * tile_height + 3 * gap + margin
    sheet = Image.new("RGB", (width, height), "#f4f1ea")
    draw = ImageDraw.Draw(sheet)
    centered(draw, (margin, margin, width - margin, margin + title_height),
             f"USD Render Benchmark: ASWF CY{year}", font(36), "#171717")
    image_left = margin + label_width + gap
    for column, label in enumerate(labels):
        x = image_left + column * (tile_width + gap)
        centered(draw, (x, margin + title_height, x + tile_width, top - gap),
                 label, font(22))
    for row, (scene, label) in enumerate(SCENES):
        y = top + row * (tile_height + gap)
        centered(draw, (margin, y, margin + label_width, y + tile_height),
                 label, font(24))
        for column, folder in enumerate(folders):
            x = image_left + column * (tile_width + gap)
            box = (x, y, x + tile_width, y + tile_height)
            draw.rounded_rectangle(box, radius=4, fill="white",
                                   outline="#d4d0c7", width=2)
            source = image_root / folder / f"{scene}.jpg"
            if source.exists():
                with Image.open(source) as original:
                    scaled = ImageOps.contain(original.convert("RGB"),
                                              (tile_width - 20, tile_height - 20),
                                              Image.Resampling.LANCZOS)
                sheet.paste(scaled, (x + (tile_width - scaled.width) // 2,
                                     y + (tile_height - scaled.height) // 2))
            else:
                centered(draw, box, "Skipped", font(22), "#999999")
    sheet.save(output, quality=94, subsampling=1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path, nargs="?", default=Path("."))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        generate(args.checkout, args.output or args.checkout / "render_sheet.jpg")
    except KeyError as error:
        parser.error(f"Missing {error.args[0]}; run this tool inside rez env aswf")


if __name__ == "__main__":
    main()
