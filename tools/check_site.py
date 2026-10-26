"""Check generated pages and source links without network access."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "docs"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = set()
        self.references = []
        self.h1_count = 0
        self.language = None
        self.viewport = False
        self.errors = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.errors.append(f"Duplicate id: {attrs['id']}")
            self.ids.add(attrs["id"])
        if tag == "html":
            self.language = attrs.get("lang")
        if tag == "h1":
            self.h1_count += 1
        if tag == "meta" and attrs.get("name") == "viewport":
            self.viewport = True
        if tag in ("a", "link", "script", "img"):
            value = attrs.get("href", attrs.get("src"))
            if value is not None:
                self.references.append(value)


pages = {path.resolve(): Page(path) for path in SITE.rglob("*.html")}
errors = []
references = 0
for path, page in pages.items():
    prefix = str(path.relative_to(ROOT))
    errors.extend(f"{prefix}: {error}" for error in page.errors)
    if page.h1_count != 1 or not page.language or not page.viewport:
        errors.append(f"{prefix}: missing or duplicate page structure")
    if re.search(r"\{\{[^}]+\}\}", path.read_text(encoding="utf-8")):
        errors.append(f"{prefix}: unresolved template variable")
    for ref in page.references:
        references += 1
        url = urlsplit(ref)
        if url.netloc == "github.com" and url.path.startswith("/Blackecki/portfolio/blob/main/"):
            original = ROOT / unquote(url.path.removeprefix("/Blackecki/portfolio/blob/main/"))
            if not original.is_file():
                errors.append(f"{prefix}: missing source file {original.name}")
        if url.scheme or url.netloc:
            continue
        if not ref or ref == "#":
            errors.append(f"{prefix}: empty link")
            continue
        if url.path.startswith("/"):
            errors.append(f"{prefix}: root-relative link breaks project-site hosting: {ref}")
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if not target.is_relative_to(SITE.resolve()):
            errors.append(f"{prefix}: link leaves published directory: {ref}")
        elif not target.is_file():
            errors.append(f"{prefix}: missing target: {ref}")
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f"{prefix}: missing anchor: {ref}")

if errors:
    raise SystemExit("\n".join(errors))
print(f"PASS: {len(pages)} pages; {references} references; local links, anchors and source files verified.")
