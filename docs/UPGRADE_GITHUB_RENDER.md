# Upgrade your existing StudentBridge AI on GitHub, Aiven and Render

**You do not need to create a new database, GitHub repository or Render service.**

1. **Back up:** preserve the working project folder and current code. Back up existing Aiven MySQL before any future schema change. This V8 update does not change the schema.
2. **Copy source only:** extract this V8 ZIP and copy its code files into your existing **cloned GitHub project**. Keep that folder's `.git` directory. Do not copy `.env` from any ZIP into Git or replace your working app secret without reviewing audit history.
3. **Local configuration:** use your current private `.env` for local testing, keep the public Aiven CA certificate under `certs/ca.pem`, and run `python -m pip install -r requirements.txt` to install the new `pypdf` dependency.
4. **Test:** run `python -m pytest -q tests` and `python run.py`. Verify the Journey Studio, forms, date reminders and planner. If running a new version of Python, create a clean `.venv` first.
5. **Git safety check:** verify `.env`, `.venv` and private keys are ignored, and scan staged files for secrets. Do not commit real database dumps or sensitive student information.
6. **Commit and push:** `git add app/ data/ docs/ tests/ requirements.txt README.md .env.example` then `git commit -m "Release StudentBridge Experience V8"` and `git push origin main`. Stage other modified source files explicitly if needed.
7. **Render:** its existing connected Web Service should auto-deploy the pushed `main` commit. The build and start commands remain `pip install -r requirements.txt` and `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
8. **Render Environment:** keep the Aiven `DATABASE_URL`, public CA certificate path, `APP_ENV=production`, `GEMINI_API_KEY` (optional), `GEMINI_MODEL`, `CARD_LIVE_ENABLED=false`, and `MERCHANT_AUTHORIZED_TO_COLLECT=false`. Rotate credentials that were exposed previously, then set new values privately in Render (and only in local `.env`).
9. **Verify:** check Render logs, `/api/health`, `Journey Studio`, `Tuition Planner`, and `Ask Bridge AI` from the production URL. On the public demo, shared transaction/audit history endpoints now intentionally return 403.

The project remains a test/sandbox system without authenticated personal accounts, banking agreements or live user transaction authority. Do not deploy for processing real personal finance information until a proper privacy/security review and user access controls are implemented.
