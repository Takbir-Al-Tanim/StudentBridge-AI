# StudentBridge AI — Current Test Report

**Run date:** 18 October 2026. **Source:** final packaged project code.

**Result:** `76 passed` using `python -m pytest -q tests` in an isolated disposable SQLite test database. Full exact output is in `evidence/TEST_RESULTS.txt`. `node --check app/static/app.js` also passed.

Coverage includes request validation, payment/fee/deadline decisions, cost and living reserve, Decision Passport, deterministic agent answers, reference FX provenance, sandbox approvals and duplicate protection, PDF handling, Journey Studio and calendar export, public-production restrictions for shared history/audit endpoints, and responsive interface source checks.

**Limits:** These are not end-to-end proof of a real MySQL service, public Render uptime, actual Gemini quota, verified bank provider quotes, merchant processing, or legal and security compliance. No real-money payment is performed. For live deployment checks and synthetic sandbox examples see `evidence/README.md`.

Historic test records from earlier development stages may mention fewer tests; this report is the verified test count for the current submission package.
