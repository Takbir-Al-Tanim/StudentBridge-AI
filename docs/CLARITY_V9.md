# StudentBridge AI — Clarity V9

## Goal
Make the product understandable at a glance. Present **features first**, use **short, useful text**, and avoid huge headings next to tiny labels. This is an original refinement of the team's existing V8 application, not a clone of a competing website.

## What changed

| Area | Before | Clarity V9 |
|---|---|---|
| Homepage headline | Oversized and promotional | 35–46 px, short action-focused message |
| Body | Mixed tiny captions and lengthy paragraphs | 15–16 px body and compact labels |
| Cards | Repeated explanatory process cards | Four clear feature cards; repeated cards removed |
| Intro | Multiple long descriptions | One direct line about tuition, transfers and budgets |
| Journey Studio | Large title, long introduction | Compact title and the form immediately below |
| Tools | Busy supporting text | Clear button labels and simplified page descriptions |
| Mobile | Large hero and unused decorative space | Compact hero and accessible single-column layout |

## Type rules

- Font family: native system UI stack (`system-ui`, `-apple-system`, `Segoe UI`, sans-serif). No external font packages or downloaded font files.
- Body text: 16 px. Typical form labels: 15 px. Feature titles: 18–20 px. Headings: 25–35 px except limited desktop hero up to 46 px.
- Small semantic labels and safety notes: normally 13–14 px. Never hide compliance, payment-approval or data-provenance cautions solely to shorten the site.
- Responsive cards: two columns on wider screens, one column on small phones. Inputs and primary buttons target at least ~44 px high.

## What did NOT change

- All existing Topic C functionality: remittances, tuition practice payments, credit readiness, multiple currencies, route comparison, Digital Twin, Decision Passport, Journey Studio, optional Gemini chat.
- Existing FastAPI routes, database schema, MySQL connection, Aiven certificate path and Render start command.
- Payments remain practice-only unless authorized hosted checkout is separately configured. AI does not silently transfer money or invent provider quotes.

## Where to edit

- `app/templates/index.html`: copy, features, nav, forms.
- `app/static/clarity-v9.css`: all V9 layout and typography overrides (loaded last).
- `app/static/experience-v8.css`: original V8 visual and Journey Studio foundation (unchanged).
- `app/static/styles.css`: existing component base (unchanged).
- `app/static/app.js`: behavior (unchanged, only cache version in HTML bumped).

## Tests and previews

Run `python -m pytest -q tests`. The test suite uses disposable SQLite through `tests/conftest.py`, **not your Aiven database**.

Render can serve the new files after a GitHub push. The `/static/` query string is updated to `v=9.1` to prevent stale CSS/JS caching.

Screenshots generated in an **isolated mocked browser preview** for layout inspection. They are not actual Render screenshots or live bank connections:

- [Desktop home](V9_Home_Desktop.png)
- [Desktop Journey Studio](V9_Journey_Desktop.png)
- [Mobile home](V9_Home_Mobile.png)
- [Mobile Journey Studio](V9_Journey_Mobile.png)

## Competition integrity checklist

1. Retain commits demonstrating the team's original work. No Flywire/Wise/Revolut/other competitors' proprietary assets or code were used.
2. Review [Originality and third-party licenses](ORIGINALITY_AND_LICENSES.md); confirm each resolved dependency's license and notices.
3. Check reuse permissions and source dates for research CSVs and archival workbooks before making the repository public.
4. Keep API keys, MySQL password, `.env`, private keys, and real student financial documents out of the repository. Rotate earlier exposed credentials.
5. Practice payments are not real transfers; bank quotes are unverified until supplied and confirmed by an appropriate provider.
6. Review actual competition Rules and Privacy Policy on the official contest website. This checklist is not legal certification.
