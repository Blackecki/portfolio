"""Render the small static portfolio. Python standard library only."""
import html
import hashlib
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site" / "pages"
DESTINATION = ROOT / "docs"
profile = json.loads((ROOT / "site" / "profile.json").read_text(encoding="utf-8"))
theme_picker = (ROOT / "site" / "partials" / "theme-picker.html").read_text(encoding="utf-8")
BASE = "https://blackecki.github.io/portfolio/"
person = json.loads((ROOT / "site" / "person.json").read_text(encoding="utf-8"))
person["name"] = profile["name"]
site_node = {"@type": "WebSite", "@id": BASE + "#website", "url": BASE,
             "name": profile["name"] + " — IT Support Portfolio", "publisher": {"@id": person["@id"]}}
urls = []

for source in sorted(SOURCE.rglob("*.html")):
    rendered = source.read_text(encoding="utf-8")
    rendered = rendered.replace('<html lang="en">', '<html lang="en" data-theme="midnight">', 1)
    relative = source.relative_to(SOURCE)
    asset_prefix = "../" * (len(relative.parts) - 1)
    rendered = rendered.replace("</header>", theme_picker + "</header>", 1)
    rendered = rendered.replace('<link rel="stylesheet"', f'<script src="{asset_prefix}assets/theme.js"></script>\n<link rel="stylesheet"', 1)
    for key, value in profile.items():
        rendered = rendered.replace("{{" + key + "}}", html.escape(str(value), quote=True))
    canonical = BASE + ("" if relative.as_posix() == "index.html" else relative.as_posix())
    urls.append(canonical)
    title = html.unescape(re.search(r"<title>(.*?)</title>", rendered, re.S).group(1))
    description = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', rendered).group(1))
    page_node = {"@type": "ProfilePage" if relative.as_posix() == "about.html" else "WebPage",
                 "@id": canonical + "#webpage", "url": canonical, "name": title,
                 "description": description, "inLanguage": "en", "isPartOf": {"@id": site_node["@id"]},
                 "about": {"@id": person["@id"]}}
    if relative.as_posix() == "about.html":
        page_node["mainEntity"] = {"@id": person["@id"]}
    structured = json.dumps({"@context": "https://schema.org", "@graph": [person, site_node, page_node]},
                            ensure_ascii=False, indent=2).replace("</", "<\\/")
    metadata = '\n'.join([
        f'<link rel="canonical" href="{canonical}">',
        f'<link rel="alternate" type="application/ld+json" href="{asset_prefix}profile.json" title="Profile data">',
        f'<link rel="alternate" type="text/plain" href="{asset_prefix}llms.txt" title="Profile summary">',
        '<meta name="robots" content="index, follow">',
        f'<meta name="author" content="{html.escape(profile["name"], quote=True)}">',
        f'<meta property="og:title" content="{html.escape(title, quote=True)}">',
        f'<meta property="og:description" content="{html.escape(description, quote=True)}">',
        f'<meta property="og:url" content="{canonical}">',
        '<meta property="og:type" content="profile">' if relative.as_posix() == "about.html" else '<meta property="og:type" content="website">',
        f'<script type="application/ld+json">\n{structured}\n</script>'
    ])
    rendered = rendered.replace("</head>", metadata + "\n</head>", 1)
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

(DESTINATION / "profile.json").write_text(
    json.dumps({"@context": "https://schema.org", **person}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(DESTINATION / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>{xml_escape(url)}</loc></url>\n' for url in sorted(urls)) + '</urlset>\n', encoding="utf-8")
summary = (ROOT / "site" / "llms.txt").read_text(encoding="utf-8")
for key, value in profile.items():
    summary = summary.replace("{{" + key + "}}", str(value))
(DESTINATION / "llms.txt").write_text(summary, encoding="utf-8")
print("Built profile.json, sitemap.xml and llms.txt")
