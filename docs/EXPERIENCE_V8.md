# StudentBridge AI — Experience V8 implementation guide

**Date:** October 18, 2026 · **Project:** FinTechathon Topic C

## What changed

The website has an independently authored, high-contrast indigo / ice-blue / mint visual system with system fonts, larger headings and form fields, responsive layouts, animated abstract routes and orbit graphics, and visible focus indicators. Animations have reduced-motion support. No Flywire/Wise/Convera/other competitor code, branding, screenshots or layout assets were copied.

**New guided flow: Journey Studio (`/`, choose Journey Studio):**

1. Enter origin and destination among the six supported countries, tuition and scholarship, available funds, protected emergency savings, living expenses and months, and deadline.
2. Optionally upload a text-selectable PDF invoice (2.5 MB / 12 pages maximum). The software extracts **possible** amounts and dates. Select values and explicitly confirm them before application. Scanned PDFs and fraud verification are not supported.
3. Choose **Prepare my complete plan**. The backend performs country/currency validation, dated reference FX lookup, tuition calculation, living-cost protection, deadline guard, +5%/+10% FX stress scenarios, and five suggested actions.
4. Review the result and source date. If the FX provider cannot be reached, the system does not invent a rate or pretend there is an accurate conversion.
5. Choose **Review in payment planner** to prefill the existing planner; add **actual provider quotes** and verify the provider supports the route. Optional **Protect my living-cost budget** checks quote-based affordability with living funds reserved.
6. Choose **Download reminder** to get a local `.ics` calendar event with a seven-day warning. The file must be imported by the student; it does not automatically modify their Google/Apple/Outlook calendar.

**AI conversation:** `Ask Bridge AI` continues to answer source-aware finance questions. Requests such as “plan my tuition” now link to Journey Studio. Optional Gemini makes supplementary wording simpler; it never controls the actual calculations.

## What really happens automatically

| Automatically performed | Requires the student's confirmation | Not implemented / external agreement needed |
|---|---|---|
| Look up dated reference FX from Frankfurter | Check an invoice's actual payment amount and recipient | Real bank provider quote collection, routing, settlement |
| Calculate reference-value tuition, scholarship and living buffer | Enter and verify provider fees, exact payment-rate quote and eligibility | Auto-login to accounts, auto-payment, university submission |
| Calculate what-if FX stress and deadline buffer | Approve any practice checkout / payment explicitly | Guaranteed money transfer time and FX forecasts |
| Produce action list and downloadable local reminder | Import reminder into user's chosen calendar | Calendar account synchronization and automatic notifications |

The new `/api/journey/prepare` endpoint does **not** save personal financial information in MySQL; existing tuition planning endpoints may store their entered data. Do not enter real personal or financial identifiers in the public shared demo.

## Project modules

- `app/templates/index.html` — V8 navigation, home, Journey Studio and existing pages.
- `app/static/styles.css` — existing component styles without remote font imports.
- `app/static/experience-v8.css` — independently authored visual system, motion and responsive layouts.
- `app/static/app.js` — Journey Studio interaction, safe invoice review, calendar file, original features.
- `app/journey.py` — pure Python protection, deadlines, calendar, task generation.
- `app/main.py` — journey endpoints and public-demo audit restrictions.
- `app/logic.py` — opt-in living-cost protection using entered quote exchange rates.
- `app/assistant.py` — source-aware conversation with action to open Journey Studio.
- `tests/test_journey_v8.py` — six automated safety/functional tests added.

## New API routes

- `POST /api/journey/prepare` — read-only personal planning, returns five tool traces and optional reference FX. Does not trigger payment or persist a plan.
- `GET /api/journey/calendar?deadline=YYYY-MM-DD&title=...&remind_days=7` — returns `text/calendar` / `.ics` file.

### Safe sample request

```bash
curl -s http://127.0.0.1:8000/api/journey/prepare \
  -H 'Content-Type: application/json' \
  -d '{"origin":"Bangladesh","destination":"Australia","goal":"Help plan my tuition","tuition_amount":14000,"scholarship_amount":0,"available_balance":2000000,"emergency_reserve":100000,"monthly_living_cost":1500,"living_months":3,"deadline":"2026-12-02"}'
```

That amount is **illustrative user input, not an official fee**. Dates and reference FX depend on the live call.

## Existing deployment compatibility

Render stays **the same FastAPI Web Service**. Aiven stays **the same MySQL database**. No new tables or credentials are needed for V8. Use the existing `DATABASE_URL`, `APP_SECRET`, CA public certificate and optional `GEMINI_API_KEY` in Render Environment. Never put actual credentials in the GitHub repository or public README. Start command remains:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Build command remains `pip install -r requirements.txt`. The sole PDF dependency change is replacing AGPL/commercial PyMuPDF with **BSD-3-Clause `pypdf`**, which handles text-selectable invoices. No database migration is required by this release.

## Limits and scope

- No independent bank-quote verification or provider eligibility guarantee.
- No real-money remittance. Hosted card checkout in prior code remains disabled without explicit authorized merchant setup.
- No OCR, machine-verified invoice fraud detection, authenticated student accounts or per-user isolation.
- `GET /api/audit`, `/api/audit/verify`, and `/api/sandbox/history` now return HTTP 403 in production to prevent public enumeration of shared demo histories. Local development can continue testing them.
- Public deployments are for fictitious data only. Previously exposed Aiven/Gemini/app secrets **must be rotated** before public use. 

## Quality checks

Run `python -m pytest -q tests` in the project root. All 73 tests passed in the local disposable SQLite test setup. JavaScript `node --check app/static/app.js` also passed. Browser tests with locally stubbed network responses confirmed the Journey Studio form opens, validates, and shows results without JavaScript errors and with no horizontal overflow at 390px viewport. These tests do not prove live Aiven credentials or remote Frankfurter availability.
