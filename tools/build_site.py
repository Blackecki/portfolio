"""Render the small static portfolio. Python standard library only."""
import html
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site" / "pages"
DESTINATION = ROOT / "docs"
profile = json.loads((ROOT / "site" / "profile.json").read_text(encoding="utf-8"))
theme_picker = (ROOT / "site" / "partials" / "theme-picker.html").read_text(encoding="utf-8")

for source in sorted(SOURCE.rglob("*.html")):
    rendered = source.read_text(encoding="utf-8")
    relative = source.relative_to(SOURCE)
    asset_prefix = "../" * (len(relative.parts) - 1)
    rendered = rendered.replace("</header>", theme_picker + "</header>", 1)
    rendered = rendered.replace('<link rel="stylesheet"', f'<script src="{asset_prefix}assets/theme.js"></script>\n<link rel="stylesheet"', 1)
    for key, value in profile.items():
        rendered = rendered.replace("{{" + key + "}}", html.escape(str(value), quote=True))
    if re.search(r"\{\{[^}]+\}\}", rendered):
        raise ValueError(f"Unresolved template value in {source}")
    target = DESTINATION / source.relative_to(SOURCE)
    # Refresh changed CSS, scripts and CVs without relying on a visitor's cache.
    def version_asset(match):
        asset = (target.parent / match.group(2)).resolve()
        version = hashlib.sha256(asset.read_bytes()).hexdigest()[:10]
        return f'{match.group(1)}{match.group(2)}?v={version}{match.group(3)}'
    rendered = re.sub(r'((?:href|src)=")((?:\.\./)*assets/[^"?]+)(")', version_asset, rendered)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered, encoding="utf-8")
    print(f"Built {target.relative_to(ROOT)}")
