# StudentBridge AI — originality, attribution and IP checklist

This document is for the 2026 FinTechathon Topic C integrity/IP requirements. It is a **project self-assessment**, not a legal certification.

## Independent work

- New Experience V8 and Clarity V9 design (layout refinements, Journey Studio, motion, color system, original CSS and UI) is newly authored for StudentBridge AI rather than copied from any commercial website.
- Other fintech websites were **studied for high-level usability ideas** only. No competitor screenshots, logos, copyrighted text, proprietary assets, or website source code are bundled.
- V8 and V9 illustrations are original CSS gradients, simple geometric SVGs, text and Unicode symbols. The supplied pre-existing StudentBridge project is retained as the starting point.
- Maintain Git commits, authorship records, issue notes and test results for competition evidence.
- The contestant team retains its original IP **subject to the respective licenses of third-party components**. Do not claim ownership of third-party software, trademarked brands, or proprietary data.

## Software dependencies and their license references

Consult the license version distributed with each installed dependency before publishing a derivative binary or commercial deployment. These are pointers, not a substitute for bundled license notices.

| Package | Intended role | License family / official link |
|---|---|---|
| FastAPI | Web API | MIT — https://github.com/fastapi/fastapi/blob/master/LICENSE |
| Uvicorn | ASGI service | BSD-3-Clause — https://github.com/encode/uvicorn/blob/master/LICENSE.md |
| HTTPX | HTTP requests | BSD-3-Clause — https://github.com/encode/httpx/blob/master/LICENSE.md |
| Pydantic | Input validation | MIT — https://github.com/pydantic/pydantic/blob/main/LICENSE |
| python-multipart | Invoice upload handling | Apache-2.0 — https://github.com/Kludex/python-multipart/blob/master/LICENSE.txt |
| pypdf | Extract text from selectable PDFs | BSD-3-Clause — https://github.com/py-pdf/pypdf/blob/main/LICENSE |
| SQLAlchemy | ORM / SQL schema | MIT — https://github.com/sqlalchemy/sqlalchemy/blob/main/LICENSE |
| PyMySQL | MySQL driver | MIT — https://github.com/PyMySQL/PyMySQL/blob/main/LICENSE |
| python-dotenv | Local environment configuration | BSD-3-Clause — https://github.com/theskumar/python-dotenv/blob/main/LICENSE |
| Jinja2 | HTML template rendering | BSD-3-Clause — https://github.com/pallets/jinja/blob/main/LICENSE.txt |
| Stripe Python SDK | Optional hosted checkout | MIT — https://github.com/stripe/stripe-python/blob/master/LICENSE |
| pytest | Automated tests | MIT — https://github.com/pytest-dev/pytest/blob/main/LICENSE |

**Important dependency change:** Previous StudentBridge releases used PyMuPDF (licensed AGPL-3.0 or commercial). V8 replaces it with the permissively licensed `pypdf` for PDF text extraction. This does *not* certify that every item in legacy code/data/docs has been cleared; review all old assets and software before commercial release. Do not copy third-party code unless its license allows it, and retain notices and attribution as required.

**Fonts:** V8 and V9 use native operating-system fonts; it does not download or package proprietary or third-party font files. All CSS/SVG illustrations added in V8 are original simple shapes. Emoji flags and platform glyphs are rendered by the user's OS.

## Data, APIs and financial disclaimers

- Financial reference rates: Frankfurter (https://frankfurter.dev/) via HTTPS; cite the displayed rate date and source; do not describe it as an executable bank quote. Check Frankfurter's published API usage terms before high-volume usage.
- External financial benchmarks, universities, government/regulatory pages and fee schedules: only link to publisher pages and cite dates. **Facts can be compared**, but do not reproduce copyrighted website text, logos or full documentation without permission.
- User-entered provider quotes are not independently verified; label them and do not pretend they are official verified prices.
- Gemini API and Stripe hosted checkout (optional): must be used in accordance with their applicable service terms; any merchant account requires an authorized payment provider and explicit configuration.
- Bank names, service provider trademarks, competitor websites and university names belong to their owners; mentioning them for source reference does not imply partnership.

## Before submitting

- [ ] Review the final competition Rules and Privacy Policy (this summary is not a replacement).
- [ ] Run `git grep` or a secret scanner and exclude `.env`, `.git`, private certificates, database backups and virtual environments from the submitted ZIP.
- [ ] Rotate exposed cloud database passwords, Gemini API keys and application secrets.
- [ ] Confirm each third-party component is licensed appropriately and include notices when required.
- [ ] Check permitted re-use and update dates for all bundled research CSV values.
- [ ] Label sandbox receipts/test payments clearly; use fake student names, invoices and numbers in the public demo.
- [ ] Keep records of independent work and testing to support originality/IP compliance.
- [ ] Do not claim banking partnerships, independently verified fees or real money transmission without evidence.

The project's original work belongs to its authors under whatever license they choose. **No top-level open-source license is automatically assigned** here; adding a `LICENSE` file is a decision for the contestants and may carry implications for code reuse.


## V9 originality and integrity update (2026-10-18)

- V9's visual hierarchy, revised writing, spacing tokens, mobile layout, and CSS overrides were independently authored for StudentBridge AI. Competitor sites were used only as inspiration for generic goals such as readable typography and simple navigation, **not** as sources of HTML, CSS, branding, screenshots, or illustrations.
- V9 adds no frontend packages, CDN fonts, icon libraries, stock images, tracking scripts, licensed commercial templates, or new third-party components.
- Every backend dependency remains listed in the table above. License names and direct links are **research pointers**; verify the specific resolved versions and all license notice requirements before submission or public redistribution.
- Source-linked financial research data need the team's own permission, accuracy, source, and reuse review. Historical original-workbook archives are intentionally omitted from this final release pending redistribution review. Names of financial providers/universities are factual references, not endorsements.
- A PDF copy of the competition rules is not necessary to execute or distribute the application. The public V9 release omits that PDF while retaining competition rule summaries and directions to consult the official rules.
- Publishing original competition work does **not** transfer ownership of external dependencies, datasets or trademarks. The project has no automatically selected repository-level license. The team must choose distribution terms appropriate for the contest and project.
- This is a documented due-diligence step—not a legal opinion or a guarantee that all third-party rights have been cleared.
