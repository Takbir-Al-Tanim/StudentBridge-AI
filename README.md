# StudentBridge AI — Topic C, Version 7

Four clearly visible services are available from the homepage and sidebar:

1. **Send money abroad:** six-country remittance planning with source-linked reference FX, user-entered fees and markup, and a link to verified provider-quote comparison. This estimates value; it does not move money.
2. **Pay university tuition:** invoice and course fee planning, real-provider quote comparison, authorized-provider card checkout if configured, and separately labeled practice transactions.
3. **Build credit abroad:** country guidance with sources and an interactive preparation checklist. This is informational, not a loan or credit eligibility decision.
4. **Manage currencies:** combined estimated value for user-entered holdings in CNY, GBP, JPY, KRW, AUD and BDT; no bank access or storage of balance inputs. Missing FX values stay missing.

The Financial Digital Twin, decision passports, AI assistant, sources, MySQL, and audit tools are preserved.

## Quick start (existing XAMPP MySQL)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
# Copy your previously working .env file into this folder. Never publish it.
python scripts/check_mysql.py
python run.py
```

Open http://127.0.0.1:8000/?v=7. **No new SQL migration is required.**

## Financial safety

- Reference FX does not equal a real executable remittance quote; optional fees/markups entered by the user are unverified.
- Real cross-border settlement is not enabled for all 30 pairs. Actual transfers require licensed providers and corridor verification.
- Card numbers are entered only on an authorized external hosted checkout and never enter the app database.
- Practice payments remain explicitly labeled and do not transfer money.
- Keep a consistent APP_SECRET for existing audit records.

Run tests with `python -m pytest -q`.

For detail see `docs/TOPIC_C_FOUR_FEATURES.md`.
