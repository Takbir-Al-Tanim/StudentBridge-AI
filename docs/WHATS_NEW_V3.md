# Version 3 changes

Updated from the exact ZIP supplied by the user, preserving the MySQL SQLAlchemy tables,
financial math, existing catalog, sandbox payment flow and audit design.

## Interface
- Improved desktop and mobile spacing and more readable labels.
- Animated six-country route lines, softly floating flags, and small motion on hover.
- Respects `prefers-reduced-motion` accessibility setting.
- Clear five-question starter panel and clickable AI next-step buttons.
- Source references shown below AI answers rather than only internal tool names.
- Enter sends chat, Shift+Enter adds a new line, chat requests disable the send button until complete.

## Assistant logic
- New `app/assistant.py`: checks chosen country from the question first; uses verified
  catalog figures, program metadata, saved plan quote calculations and available sources.
- Exchange-rate requests attempt the existing Frankfurter endpoint; a failed lookup
  gives an unavailable result instead of inventing a number.
- Optional Gemini rephrasing is supplementary, not a replacement for checked facts.
- No generic all-knowing autonomous banking claims are made.

## Database
- No SQL change: existing ten tables and stored data continue to be used.
- `requirements.txt` now explicitly installs Jinja2 and a recent PyMuPDF.

## Validation
- The application tests use an isolated temporary SQLite database for safety.
  The running application continues to use the configured MySQL database.
- The package excludes `.env`, `.venv`, OS metadata, caches and all user passwords.
- Run `python -m pytest -q` and `python scripts/check_mysql.py` after installing.

## Limitations
- App UI and finance logic are a competition proof of concept, not a regulated service.
- Live rate requires internet; provider transfer offers must be confirmed by users.
- Existing PDF reports/slide decks may describe earlier visual design and serve as
  background documents. This guide/README documents the current code.
