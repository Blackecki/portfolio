# Krzysztof Czarnecki — IT Support & Cybersecurity

My portfolio brings together practical work with Windows, Linux and networking, personal software projects, and cybersecurity case studies. I am a programming-track graduate with INF.03, developing my skills for junior IT support roles.

**[Visit the portfolio](https://blackecki.github.io/portfolio/)** · **[CV](https://blackecki.github.io/portfolio/assets/krzysztof-czarnecki-cv.pdf)** · **[LinkedIn](https://www.linkedin.com/in/krzysztofczarnecki/)**

This repository contains the portfolio website, its source files and the original coursework reports. The software projects below have their own repositories.

## Personal projects

| Project | Focus |
| --- | --- |
| [Cryplab](https://github.com/Blackecki/Cryplab) | Python command-line tool with SHA-256 text and file hashing, AES-GCM text encryption and key export. |
| [Retro Forum](https://github.com/Blackecki/retro-forum) | Next.js application with Prisma/SQLite, JWT sessions, bcrypt password checks and login attempt limits. |
| [Home lab and ThinkPad firmware](https://blackecki.github.io/portfolio/about.html#practical-work) | Raspberry Pi with Pi-hole, Windows/Linux virtual machines, and a coreboot installation following the Skulls documentation. |

## Cybersecurity case studies

- [Phishing email investigation](https://blackecki.github.io/portfolio/projects/phishing.html) — suspicious attachment analysis, file reputation and the rationale for SOC escalation.
- [DNS service failure](https://blackecki.github.io/portfolio/projects/dns.html) — interpreting DNS/ICMP errors, evaluating possible causes and identifying further checks.
- [SYN flood incident](https://blackecki.github.io/portfolio/projects/syn-flood.html) — incomplete TCP handshakes, availability impact and investigation requirements.

These case studies are based on Google Cybersecurity Professional Certificate exercises. Each write-up distinguishes the supplied evidence, interpretation and proposed follow-up actions. Original reports are available through the [materials page](https://blackecki.github.io/portfolio/materials.html).

## Website

The site uses static HTML, CSS and a small amount of JavaScript, hosted on GitHub Pages. It includes responsive layouts, keyboard navigation, selectable colour themes and a downloadable CV. Content and navigation remain accessible without JavaScript.

## Repository structure

| Path | Contents |
| --- | --- |
| `site/` | Page templates, shared components and profile data. |
| `docs/` | Published website and assets. |
| `tools/` | Site generation, CV generation and validation scripts. |
| Repository root | Original coursework reports and worksheets. |

## Local development

Building and checking the website requires Python 3.9 or later, using only the standard library.

```sh
python tools/build_site.py
python tools/check_site.py
python -m http.server 8765 --bind 127.0.0.1 --directory docs
```

Open [localhost:8765](http://127.0.0.1:8765/) to preview the site. The separate CV generator, `tools/build_cv.py`, requires ReportLab and the Windows Arial fonts.

## Contact

[krzysztof.c.tech@gmail.com](mailto:krzysztof.c.tech@gmail.com)
