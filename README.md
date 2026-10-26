# Krzysztof Czarnecki — Cybersecurity portfolio

Coursework from the Google Cybersecurity Professional Certificate, with revised case notes explaining the available evidence, conclusions and limitations.

The portfolio also introduces my background in programming-focused technical education (INF.03 passed), warehouse and merchandising work, a school placement, and personal work with virtual machines, Pi-hole and coreboot.

## Selected case studies

- [Phishing investigation](docs/projects/phishing.html): suspicious email, file reputation and the reasoning behind SOC escalation.
- [DNS service failure](docs/projects/dns.html): ICMP errors, alternative explanations and a corrected interpretation of the original report.
- [SYN flood incident](docs/projects/syn-flood.html): incomplete TCP handshakes, the reported traffic pattern and verification steps.

These are **educational exercises**, not claims of professional incident response. Proposed follow-up actions are distinguished from completed work. The original reports are preserved at the repository root.

## Website

The publishable site is in `docs/`. It uses static HTML and CSS, system fonts and no third-party scripts, tracking, or package dependencies. It works without JavaScript.

Preview locally from the repository root:

```sh
python -m http.server 8765 --bind 127.0.0.1 --directory docs
```

Then open `http://127.0.0.1:8765`.

## Editing

- Edit page content in `site/pages/`.
- Edit the name and course status once in `site/profile.json`.
- Edit the stylesheet in `docs/assets/style.css`.
- Run `python tools/build_site.py` to update the publishable HTML.
- Run `python tools/build_cv.py` to update the one-page English CV (requires ReportLab and the Windows Arial fonts).
- Run `python tools/check_site.py` to check local links, anchors, source-file references and unresolved placeholders.

The course is currently recorded as being in its final stage. Change `course_status` to `completed` after completion, then rebuild the site and CV. A certificate link can be added once available.

The CV uses the owner's supplied CV and corrections. Warehouse and merchandising roles are summarized without invented employers or dates. Fuller personal-project write-ups can be added when the relevant setup details and evidence are available.

## GitHub Pages setup

In the repository's **Settings → Pages**, choose **Deploy from a branch**, branch **main**, folder **/docs**, then save. Once the source is pushed and publication completes, the expected address is `https://blackecki.github.io/portfolio/`.

The `docs/.nojekyll` file keeps publication buildless. Relative internal links support both local preview and the `/portfolio/` project URL.

## Source notes

- The DNS case note corrects the original report's ICMP message classification and unsupported DDoS conclusion.
- The materials page notes the outdated periodic password-change recommendation in the original risk report.
- The phishing `.docx` at the repository root contains an HTML error page rather than a Word document. The site links to the valid PDF instead.
- No original course document has been overwritten.
