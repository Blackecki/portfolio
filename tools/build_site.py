"""Render the small static portfolio. Python standard library only."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site" / "pages"
DESTINATION = ROOT / "docs"
profile = json.loads((ROOT / "site" / "profile.json").read_text(encoding="utf-8"))

for source in sorted(SOURCE.rglob("*.html")):
    rendered = source.read_text(encoding="utf-8")
    for key, value in profile.items():
        rendered = rendered.replace("{{" + key + "}}", html.escape(str(value), quote=True))
    if re.search(r"\{\{[^}]+\}\}", rendered):
        raise ValueError(f"Unresolved template value in {source}")
    target = DESTINATION / source.relative_to(SOURCE)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered, encoding="utf-8")
    print(f"Built {target.relative_to(ROOT)}")
