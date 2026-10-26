"""Build the public, one-page English CV using ReportLab and installed Arial fonts."""
import json
import os
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
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

ink = colors.HexColor("#202830")
muted = colors.HexColor("#525e68")
link = "#244f80"
styles = {
    "name": ParagraphStyle("name", fontName="CVArialBold", fontSize=21, leading=25, textColor=ink, spaceAfter=4),
    "subtitle": ParagraphStyle("subtitle", fontName="CVArial", fontSize=11, leading=15, textColor=ink, spaceAfter=7),
    "contact": ParagraphStyle("contact", fontName="CVArial", fontSize=9, leading=13, textColor=muted, spaceAfter=2),
    "section": ParagraphStyle("section", fontName="CVArialBold", fontSize=10.5, leading=14, textColor=ink, spaceBefore=12, spaceAfter=5, keepWithNext=True),
    "body": ParagraphStyle("body", fontName="CVArial", fontSize=9.5, leading=13.3, textColor=ink, spaceAfter=5),
    "entry": ParagraphStyle("entry", fontName="CVArialBold", fontSize=9.5, leading=13.3, textColor=ink, spaceAfter=2, keepWithNext=True),
    "small": ParagraphStyle("small", fontName="CVArial", fontSize=9, leading=12.2, textColor=muted, spaceAfter=4),
}
story = []


def p(text, style="body"):
    story.append(Paragraph(text, styles[style]))


def a(url, label):
    return f'<a href="{escape(url)}" color="{link}">{escape(label)}</a>'


p(escape(profile["name"]), "name")
p("Junior IT Support / Cybersecurity", "subtitle")
p("Pruszcz Gdański, Poland · " + a("mailto:krzysztof.c.tech@gmail.com", "krzysztof.c.tech@gmail.com"), "contact")
p(a("https://github.com/Blackecki", "github.com/Blackecki") + " · " + a("https://www.linkedin.com/in/krzysztofczarnecki/", "linkedin.com/in/krzysztofczarnecki"), "contact")
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=.6, color=colors.HexColor("#aeb8c0")))

p("PROFILE", "section")
p("Technical secondary school graduate with practical Windows/Linux, virtualization and networking experience from a home lab. Passed INF.03. Developing skills for junior IT support and cybersecurity roles through personal projects and Google cybersecurity coursework.")

p("TECHNICAL FOUNDATIONS", "section")
p("<b>Systems and support:</b> Windows, Linux, virtual machines, software installation and configuration, hardware and software troubleshooting.")
p("<b>Networking:</b> TCP/IP, DNS, DHCP, HTTP/HTTPS, LAN and connection diagnostics.<br/><b>Programming and tools:</b> Python, C#, SQL, Git, Linux terminal and Nmap.")

p("PROJECTS", "section")
p("Home lab and ThinkPad firmware", "entry")
p("Run a Raspberry Pi homelab with Pi-hole and work with Windows/Linux virtual environments. Installed coreboot on a personal ThinkPad using a Raspberry Pi and the Skulls project's instructions.")
p("Cryplab · " + a("https://github.com/Blackecki/Cryplab", "GitHub"), "entry")
p("Develop a Python command-line project for learning encryption and hashing, including text and file processing.")
p("Retro Forum · " + a("https://github.com/Blackecki/retro-forum", "GitHub"), "entry")
p("Develop a web forum and explore authentication, authorization and user-data handling as part of learning application security.")
p("Cybersecurity coursework · " + a("https://github.com/Blackecki/portfolio", "Portfolio"), "entry")
p("Prepared reports on phishing, DNS/ICMP failures and SYN flood scenarios. Documented evidence, investigation limitations and the rationale for escalation. Educational exercises.")

p("EXPERIENCE", "section")
p("H2B, Gdańsk · School placements", "entry")
p("March-April 2024; March-April 2025", "small")
p("Supported office operations through document handling, printing and administrative tasks. Worked with staff to complete assigned tasks and participated in training.")
p("<b>Additional experience:</b> warehouse and merchandising work, including preparation of reports.")

p("EDUCATION AND TRAINING", "section")
p("Pomorskie Szkoły Rzemiosł · Technical secondary school · 2026", "entry")
p("Completed the programming track. Passed INF.03: creating and administering websites and databases.")
p("Google Cybersecurity Professional Certificate", "entry")
p(escape(profile["course_status"]).capitalize() + ". Coursework includes Linux, SQL, Python, networking and security operations.")

p("LANGUAGES AND ADDITIONAL INFORMATION", "section")
p("Polish: native · English: B2 · Category B driving licence<br/>Available for on-site work and occasional business travel.")

target = ROOT / "docs" / "assets" / "krzysztof-czarnecki-cv.pdf"
target.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(str(target), pagesize=A4, leftMargin=40, rightMargin=40,
                        topMargin=31, bottomMargin=30, title=profile["name"] + " - CV",
                        author=profile["name"], subject="Junior IT Support and Cybersecurity")
doc.build(story)
print(f"Built {target.relative_to(ROOT)}")
