# Final Competition Submission Guide — StudentBridge AI

The project is named **StudentBridge AI**. The ZIP and root folder are named `StudentBridge_AI` (no release/version suffix). Internally, the app records its software version for reproducibility.

## Official requirements (competition's supplied Appendix 2, pages 2–4)

**Track:** International Track, Topic C — Cross-border & Student Finance Assistant.  
**Judging:** Task completion **40%**, security/compliance **30%**, innovation/interaction **30%**.  
**Submission deadline:** **20 October 2026, 23:59 Beijing (UTC+8)**, which is **20 October 2026, 21:59 Bangladesh (UTC+6)**.  
**Submission/presentation language:** English.  
**Team eligibility:** 2–5 eligible students, 60%+ non-Chinese nationals; verify full detailed rules with the organizer.

## Files to provide

| Required item | Included location | Status |
|---|---|---|
| Source code | `app/`, `scripts/`, `requirements.txt`, `run.py`, research data, tests | Included |
| README and instructions | `README.md`, `docs/MYSQL_SETUP.md` | Included |
| Architecture, algorithms, security design | `docs/TECHNICAL_DOCUMENTATION.pdf`, `docs/TECHNICAL_ADDENDUM.md`, `docs/SYSTEM_DESIGN.md` | Included |
| Presentation deck (<=10 minutes) | `docs/submission/StudentBridge_AI_Presentation.pptx` and `.pdf` | Included; team must rehearse |
| Security self-assessment / permission tiers | `docs/SECURITY_SELF_ASSESSMENT.md` and `.pdf` | Included; known gaps listed |
| Test cases and test execution | `tests/`, `evidence/TEST_RESULTS.txt`, README testing section | Included; 76 isolated tests |
| Demonstration operation evidence | `evidence/synthetic_sandbox_execution.json`, `evidence/README.md` | Simulated local evidence; still run MySQL demo |
| Demo video <=5 minutes | `docs/DEMO_VIDEO_SCRIPT.md` | **NOT recorded or included; optional standalone video** |
| GitHub repository URL | https://github.com/Takbir-Al-Tanim/StudentBridge-AI | Link provided; owner must publish/check repo |
| Live Render website URL | README top section | **NOT VERIFIED** — contestant must paste genuine live URL and test it |
| License and provenance review | `docs/ORIGINALITY_AND_LICENSES.md`, `docs/THIRD_PARTY_REVIEW.md` | Checklist included; team review outstanding |

## Suggested <=10-minute presentation

1. 0:00–1:00: user problem and why deadlines, fees and living costs matter.
2. 1:00–2:00: Topic C feature overview across six supported countries; no claim all bank corridors work.
3. 2:00–4:00: show invoice, Journey Studio and date/calendar planning with demo facts.
4. 4:00–6:00: show quote ranking, rejected offers, and FX/living-cost scenarios.
5. 6:00–7:00: demonstrate Decision Passport and source provenance.
6. 7:00–8:00: demonstrate **clearly simulated** approval/receipt/audit evidence.
7. 8:00–9:00: explain source-verified data vs hypothetical quotes and known security limits.
8. 9:00–10:00: implementation, tests, novelty, realistic next steps.

## Before submission — human actions still required

- [ ] Put the correct live website URL in README after opening it in a private browser and checking `/api/health`.
- [ ] Ensure GitHub repository contains **only clean source**, no `.env`, secrets, student invoices, `.git`, local VENV or database backup.
- [ ] **Rotate previously exposed passwords and API keys** and review Git history; do not assume removing a file removes secret history.
- [ ] Confirm intellectual-property ownership and third-party dependency and data permissions. Keep necessary notices.
- [ ] Run `python -m pytest -q tests` on the final source; check actual Render+MySQL connection separately.
- [ ] Use a dedicated test MySQL DB, execute sandbox cases and capture logs/recording. Do not represent the bundled SQLite test evidence as live MySQL.
- [ ] Record a <=5-minute optional demo video if desired; verify each team member is eligible.
- [ ] Rehearse the <=10-minute deck and ensure screenshots demonstrate the submitted build.
- [ ] Re-read the official competition Rules and Privacy Policy: https://fintechathon.g-ican.com/.

**Important:** Packaging these items is not evidence of an actual competition submission, guaranteed compliance, or a competition award.
