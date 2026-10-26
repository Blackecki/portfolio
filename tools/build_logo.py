"""Draw the Blackecki identity as SVG paths. No image-generation service is used.

Requires fonttools and the installed Windows Bahnschrift font. Exported SVGs
contain outlines only: recipients do not need the font or this script.
"""
from pathlib import Path
import json
import math
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".preview" / "logo-runtime"))
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

OUT = ROOT / "brand"
OUT.mkdir(exist_ok=True)
FONT = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / "bahnschrift.ttf"
font = instantiateVariableFont(TTFont(FONT), {"wght": 600, "wdth": 100}, inplace=False)
glyphs = font.getGlyphSet()
cmap = font.getBestCmap()
letters = "blackecki"
tracking = -12

# Optical spacing supplements the font's advance widths for this fixed wordmark.
pairs = {"bl": -7, "la": -15, "ac": -7, "ck": -12, "ke": -9, "ec": -7, "ki": -5}
cursor = 0
placements = []
bounds = BoundsPen(glyphs)
for i, letter in enumerate(letters):
    name = cmap[ord(letter)]
    placements.append((name, cursor))
    glyphs[name].draw(TransformPen(bounds, (1, 0, 0, 1, cursor, 0)))
    cursor += font["hmtx"][name][0] + tracking
    if i + 1 < len(letters):
        cursor += pairs.get(letters[i:i + 2], 0)
xmin, ymin, xmax, ymax = bounds.bounds
scale = 60 / (ymax - ymin)
word_width = (xmax - xmin) * scale
width = math.ceil(122 + word_width + 17)

# Original B outline. The two pointed counters reference a terminal prompt.
MARK = (
    "M17 8H55L75 28V38L65 48L79 62V72L63 88H17Z "
    "M33 23V43H49L59 33L49 23Z "
    "M33 56V76H54L64 66L54 56Z"
)


def word_paths(x=122, bottom=78):
    pen = SVGPathPen(glyphs)
    for name, offset in placements:
        glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale,
                                          x + (offset - xmin) * scale,
                                          bottom + ymin * scale)))
    return pen.getCommands()


WORD = word_paths()


def svg(body, w, h, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="title">\n'
            f'<title id="title">{title}</title>\n{body}\n</svg>\n')


def lockup(mark_color, text_color):
    return (f'<path d="{MARK}" fill="{mark_color}" fill-rule="evenodd"/>\n'
            f'<path d="{WORD}" fill="{text_color}"/>')


variants = {
    "blackecki-logo-on-light.svg": svg(lockup("#4169a5", "#17233a"), width, 96, "Blackecki"),
    "blackecki-logo-on-dark.svg": svg(lockup("#b4c7ff", "#f4f7fc"), width, 96, "Blackecki"),
    "blackecki-logo-black.svg": svg(lockup("#111111", "#111111"), width, 96, "Blackecki"),
    "blackecki-logo-white.svg": svg(lockup("#ffffff", "#ffffff"), width, 96, "Blackecki"),
    "blackecki-mark.svg": svg(f'<path d="{MARK}" fill="#4169a5" fill-rule="evenodd"/>', 96, 96, "Blackecki B symbol"),
    "blackecki-mark-white.svg": svg(f'<path d="{MARK}" fill="#ffffff" fill-rule="evenodd"/>', 96, 96, "Blackecki B symbol"),
    "blackecki-avatar.svg": svg('<rect width="96" height="96" fill="#17233a"/>\n'
        f'<path d="{MARK}" transform="translate(10.56 10.56) scale(.78)" fill="#b4c7ff" fill-rule="evenodd"/>',
        96, 96, "Blackecki avatar with circular crop clearance"),
    "blackecki-favicon.svg": svg('<rect width="96" height="96" rx="8" fill="#17233a"/>\n'
        f'<path d="{MARK}" fill="#b4c7ff" fill-rule="evenodd"/>', 96, 96, "Blackecki browser icon"),
}
for filename, content in variants.items():
    (OUT / filename).write_text(content, encoding="utf-8")

# Export metadata is consumed by render_logo.cjs for the transparent PNGs.
(OUT / "assets.json").write_text(json.dumps({"wordmark": letters, "width": width,
    "height": 96, "files": list(variants), "colors": {"navy": "#17233a", "blue": "#4169a5", "lightBlue": "#b4c7ff"}}, indent=2), encoding="utf-8")
print(f"Built {len(variants)} outlined SVG assets in {OUT}")
