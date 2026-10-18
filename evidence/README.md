# StudentBridge AI — Evidence package

This folder separates **executed software tests** from **real deployment evidence**. Please do not imply the sample proves a live transfer or real-bank integration.

- `TEST_RESULTS.txt` — output of `python -m pytest -q tests` on the bundled source: **76 passing automated tests** on an isolated disposable SQLite test DB.
- `synthetic_sandbox_execution.json` — one generated student-finance example using a **fictional institution**, a **hypothetical quote**, and FastAPI TestClient with isolated SQLite; it produced `SIMULATED_COMPLETED`, returned `simulation_only=true`, and verified the local HMAC audit chain. **No real payment or MySQL connection occurred in this execution.**
- `examples/old_SQLite_sample_evidence.json` — older archived SQLite example; labelled legacy, not MySQL or current external evidence.

## Evidence you must still create before final competition submission

1. Start a **separate non-production** MySQL service and configure `.env` privately; keep account credentials out of evidence.
2. Run `python scripts/check_mysql.py`, then optional `MYSQL_SMOKE_TEST=YES python scripts/smoke_test_mysql.py` (only after reading the test script).
3. Run `python scripts/seed_sandbox.py` on that disposable MySQL database to create two illustrative MySQL planning and ledger samples; this creates `evidence/mysql_sandbox_example.json` in your local folder.
4. Show `/api/health` returning a working MySQL connection on the actual public deployed website. For production, the shared audit/history endpoints deliberately return HTTP 403 and cannot be used as an anonymous verification page.
5. Record your **own** short screen capture of the real deployment and sandbox flow using fake student details; do not show passwords, .env files, private invoices or payment cards. Standalone video is optional with maximum 5 minutes under the supplied rules.
6. Keep dated, source-verifiable bank/provider quotes only if permission and availability are verified. User-entered numbers are **not verified bank quotes**.

The package does not claim that these remaining live/manual checks are completed. See `docs/COMPETITION_SUBMISSION_GUIDE.md` and `docs/SECURITY_SELF_ASSESSMENT.md`.
