"""Compose the logo presentation from the deterministic SVG/PNG exports."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "brand"
canvas = Image.new("RGB", (1600, 1080), "#eceff3")
draw = ImageDraw.Draw(canvas)
regular = "C:/Windows/Fonts/segoeui.ttf"
bold = "C:/Windows/Fonts/segoeuib.ttf"


def text(x, y, value, size=22, color="#596374", strong=False):
    draw.text((x, y), value, font=ImageFont.truetype(bold if strong else regular, size), fill=color)


def place(name, x, y, width):
    img = Image.open(OUT / name).convert("RGBA")
    img = img.resize((width, round(img.height * width / img.width)), Image.Resampling.LANCZOS)
    canvas.paste(img, (x, y), img)
    return img.height


text(48, 28, "BLACKECKI / LOGO", 22, "#26334b", True)
text(1258, 29, "Projekt wektorowy", 21)
draw.rectangle((40, 92, 1560, 530), fill="#17233a")
h = place("blackecki-logo-on-dark.png", 260, 220, 1080)
text(72, 477, "Wersja na ciemne tło", 19, "#b2bfd5")
draw.rectangle((40, 554, 1015, 973), fill="#ffffff")
place("blackecki-logo-on-light.png", 126, 702, 805)
text(72, 922, "Wersja na jasne tło", 19)
draw.rectangle((1039, 554, 1560, 973), fill="#ffffff")
place("blackecki-mark.png", 1097, 659, 180)
place("blackecki-avatar.png", 1320, 682, 134)
text(1071, 922, "Znak i ikona profilu", 19)
text(48, 1010, "SVG / PNG z przezroczystym tłem / wersje jednobarwne", 21)
text(1260, 1010, "blackecki", 21, "#26334b", True)
canvas.save(OUT / "blackecki-preview.png")
print(f"Built {OUT / 'blackecki-preview.png'}")
