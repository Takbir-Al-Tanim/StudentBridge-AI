# StudentBridge AI V7 — First steps

The homepage has four large buttons matching Topic C: **Send money abroad**, **Pay university tuition**, **Build credit abroad**, and **Manage my currencies**.

## Run with your current XAMPP database

1. Extract the ZIP to a *new* project folder on your Mac.
2. Copy your working `.env` from the old StudentBridge folder into this new folder. Do not share `.env`.
3. Start XAMPP MySQL.
4. In Terminal, inside the new project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/check_mysql.py
python run.py
```

5. Open **http://127.0.0.1:8000/?v=7**. Press Cmd + Shift + R if the old UI appears.

You do not need to run another MySQL schema query. Old plans and audit records remain in the database; use the same APP_SECRET for integrity checks.

## Demonstrate the four features

- **Remittances**: Choose China → Australia, enter the sending amount and optional actual bank fee, then click Calculate transfer. The result uses a published FX reference *if available*, not a live transfer quote. Compare separately collected real bank quotes in the payment planner.
- **Tuition**: Click Tuition payments. Review the provider checkout availability and, if not authorized, use the clearly labelled practice payment wizard. For an official quote and tuition plan use Compare payment routes. An actual provider-hosted card checkout requires authorized merchant configuration.
- **Credit**: Click Build credit. Select the destination country, read official guidance, complete the four-step preparation checklist.
- **Multi-currency**: Click My currencies. Enter your own amounts across CNY, GBP, JPY, KRW, AUD, and BDT. Select a target currency. If reference FX is available, the estimated total appears with source dates. Missing rates will never be filled with fictional values.

## Testing

```bash
python -m pytest -q
```

The ZIP was built after passing **64 automated tests** and a browser UI test that supplied *mock FX responses* for calculation checks. This did not verify a live XAMPP MySQL connection or current third-party API uptime. Run `scripts/check_mysql.py` on your Mac.

## Important limits

- 30 directional country combinations mean 30 planning selections, **not** 30 active money-transfer providers.
- Tuition charges to a merchant account are not automatically tuition remittances to a university.
- Credit guidance is informational and does not access credit bureaus or approve loans.
- The multi-currency manager does not connect to bank accounts or save entered balances.
- No real card numbers, CVCs, account passwords or OTPs should be entered into StudentBridge forms. Use only an approved payment provider's secure hosted card page.
