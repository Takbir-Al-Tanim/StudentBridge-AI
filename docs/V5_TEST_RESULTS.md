# StudentBridge AI V5 — Validation Summary

- **52 automated tests passed** using an isolated, disposable SQLite test database; they were **not** run against the user's live XAMPP MySQL database.
- Browser preview tested at **1440 × 900** and **390 × 844** using application HTML, CSS, and JavaScript connected to the same test endpoints. Both completed the full demo payment sequence with **no uncaught JavaScript errors**.
- Verified in tests: six-country catalog, existing financial calculations, HMAC-linked audit records, deadline and protected-reserve rules, permission checks, demo approval, transaction receipt, and duplicate-request prevention.
- Source/provenance separation: the three payment-demo methods are fictional and are saved in sandbox plans only, not the verified financial research tables.
- **Still required on the user's Mac:** `python scripts/check_mysql.py` and `python run.py` with their own XAMPP MySQL credentials and unchanged `.env`/`APP_SECRET`.
- **Not performed:** live-money transfers, provider quote verification, penetration test, or production authentication/security audit.

Screenshots: `docs/previews/v5-home-1440.png`, `docs/previews/v5-payment-1440.png`, `docs/previews/v5-receipt-1440.png`, and corresponding `390` mobile screenshots.
