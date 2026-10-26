"""Build the public, one-page English CV using ReportLab and installed Arial fonts."""
import json
import os
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[1]
profile = json.loads((ROOT / "site" / "profile.json").read_text(encoding="utf-8"))
font_dir = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
pdfmetrics.registerFont(TTFont("CVArial", str(font_dir / "arial.ttf")))
pdfmetrics.registerFont(TTFont("CVArialBold", str(font_dir / "arialbd.ttf")))
pdfmetrics.registerFontFamily("CVArial", normal="CVArial", bold="CVArialBold")

ink = colors.HexColor("#171d23")
muted = colors.HexColor("#535e68")
link = "#244f80"
styles = {
    "name": ParagraphStyle("name", fontName="CVArialBold", fontSize=24, leading=28, textColor=ink, spaceAfter=5),
    "subtitle": ParagraphStyle("subtitle", fontName="CVArialBold", fontSize=11, leading=15, textColor=ink, spaceAfter=7),
    "contact": ParagraphStyle("contact", fontName="CVArial", fontSize=9, leading=13, textColor=muted, spaceAfter=2),
    "section": ParagraphStyle("section", fontName="CVArialBold", fontSize=10.5, leading=14, textColor=ink, spaceBefore=11, spaceAfter=6, keepWithNext=True),
    "body": ParagraphStyle("body", fontName="CVArial", fontSize=10, leading=13.6, textColor=ink, spaceAfter=5),
    "entry": ParagraphStyle("entry", fontName="CVArialBold", fontSize=10, leading=13.6, textColor=ink, spaceAfter=3, keepWithNext=True),
    "bullet": ParagraphStyle("bullet", fontName="CVArial", fontSize=9.7, leading=13.3, textColor=ink, leftIndent=10, firstLineIndent=-8, spaceAfter=3),
    "small": ParagraphStyle("small", fontName="CVArial", fontSize=9, leading=12.2, textColor=muted, spaceAfter=4),
}
story = []


def p(text, style="body"):
    story.append(Paragraph(text, styles[style]))


def a(url, label):
    return f'<a href="{escape(url)}" color="{link}">{escape(label)}</a>'


def bullet(text):
    p("• " + text, "bullet")


p(escape(profile["name"]), "name")
p("JUNIOR IT SUPPORT  |  Windows · Linux · Networking", "subtitle")
p("Pruszcz Gdański, Poland · " + a("mailto:krzysztof.c.tech@gmail.com", "krzysztof.c.tech@gmail.com"), "contact")
p(a("https://blackecki.github.io/portfolio/", "Portfolio & case studies") + " · " + a("https://github.com/Blackecki", "GitHub / Blackecki") + " · " + a("https://www.linkedin.com/in/krzysztofczarnecki/", "LinkedIn / krzysztofczarnecki"), "contact")
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=.6, color=colors.HexColor("#aeb8c0")))

p("PROFILE", "section")
p("Programming-track graduate with INF.03 and hands-on Windows/Linux experience from a home lab. Configured Pi-hole, installed coreboot on a ThinkPad and built Python tools for hashing and encryption. Seeking a first IT support role, with a focus on systems, networking and security.")

p("SELECTED PROJECTS", "section")
p("Home lab &amp; firmware installation", "entry")
bullet("Configured Pi-hole on a Raspberry Pi; used Windows/Linux virtual environments to practise system setup and troubleshoot network and service issues.")
bullet("Installed coreboot on a personal ThinkPad using a Raspberry Pi, following the Skulls project's flashing instructions.")
p("Cryplab — Python cryptography learning tool · " + a("https://github.com/Blackecki/Cryplab", "Source code"), "entry")
bullet("Implemented SHA-256 hashing for text and files, with chunked file reads, plus AES-256-GCM text encryption using the cryptography library.")
bullet("Added random nonce generation, Base64 output and key export to the command-line workflow.")
p("Retro Forum — Next.js web application · " + a("https://github.com/Blackecki/retro-forum", "Source code"), "entry")
bullet("Developed login handling with bcrypt password checks, JWT sessions and per-IP and per-account attempt limits, backed by Prisma/SQLite.")
p("Incident analysis — Google course exercises · " + a("https://blackecki.github.io/portfolio/", "Read case studies"), "entry")
bullet("Documented phishing triage, DNS/ICMP failures and SYN flood scenarios; separated evidence from hypotheses and explained escalation and follow-up steps.")

p("TECHNICAL SKILLS", "section")
p("<b>Systems:</b> Windows, Linux, virtual machines, software installation, hardware/software troubleshooting.<br/><b>Networks:</b> TCP/IP, DNS, DHCP, HTTP/HTTPS, LAN diagnostics, Pi-hole.<br/><b>Code &amp; tools:</b> Python, SQL, Git, Linux terminal; C# and Nmap fundamentals.")

p("EXPERIENCE", "section")
p("H2B, Gdańsk · School placements", "entry")
p("March-April 2024; March-April 2025", "small")
p("Handled documents, printing and day-to-day administrative tasks during school placements.")
p("<b>Additional experience:</b> warehouse and merchandising work, including preparing reports.")

p("EDUCATION AND TRAINING", "section")
p("Pomorskie Szkoły Rzemiosł · Technical secondary school · 2026", "entry")
p("Programming track completed. <b>INF.03 passed:</b> creating and administering websites and databases.")
p("Google Cybersecurity Professional Certificate", "entry")
p(escape(profile["course_status"]).capitalize() + ". Linux, SQL, Python, network security and incident analysis.")

p("LANGUAGES AND ADDITIONAL INFORMATION", "section")
p("Polish: native · English: C1 · Category B driving licence<br/>Open to on-site work and occasional business travel.")

target = ROOT / "docs" / "assets" / "krzysztof-czarnecki-cv.pdf"
target.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(str(target), pagesize=A4, leftMargin=40, rightMargin=40,
                        topMargin=31, bottomMargin=30, title=profile["name"] + " - Junior IT Support CV",
                        author=profile["name"], subject="Junior IT Support - Windows, Linux and Networking")
doc.build(story)
print(f"Built {target.relative_to(ROOT)}")
