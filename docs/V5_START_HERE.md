# StudentBridge AI — V5 Start Here

**This is the redesigned, MySQL-backed competition demonstration.** It keeps the six-country planner, sourced financial information, budget simulator, credit guide, AI helper, and MySQL audit trail from V4. The new feature is a complete **demo payment checkout**.

## What visitors can do

1. Open **Make a demo payment** from the left menu.
2. Choose **any two different** countries among China, UK, Japan, South Korea, Australia and Bangladesh.
3. Enter university name, tuition, deadline, funds, emergency reserve and exchange rate. Click **Get published rate** to try Frankfurter's latest reference figure; if it is unavailable, you may enter a **clearly labeled sample rate**. No value is silently invented.
4. Press **Show payment methods**. The website displays three **fictional example options** with different sample fees and estimated times. Options failing the deadline or budget checks are disabled.
5. Choose one eligible demo option, read the **Review** screen, tick the approval box, and press **Approve test payment**.
6. Read the confirmation screen. Download a **plain text demo receipt** or open **Payment history**. The transaction and chained audit record are saved in your existing MySQL tables.

**No real money is sent.** The demo providers, charges, and transfer times are not real offers. A published reference rate is not a remittance rate. Do not enter real bank credentials or real payment card information.

## What changed

- One readable main content area rather than three crowded columns.
- Larger, simpler text and a prominent demo payment menu.
- The AI helper opens on demand through **Ask Bridge AI**.
- A four-step payment process with visible progress, selectable methods, itemized totals, explicit confirmation and downloadable receipt.
- Responsive mobile views, reduced-motion support and the existing country route animation.
- New **/api/demo/prepare** and **/api/sandbox/receipt/{id}** endpoints.
- Server checks for budget, protected reserve, deadline, approval, transaction idempotency and audit integrity.
- No new SQL tables or database migration are required.

## Installation on Mac + XAMPP

1. Unzip the package; open a Terminal **inside its `StudentBridge_AI_MySQL` folder**.
2. Ensure XAMPP MySQL is running.
3. Copy the working `.env` from your previous project into this folder **without sharing it**. Use the same `APP_SECRET` to preserve existing audit verification.
4. Install dependencies and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/check_mysql.py
python run.py
```

5. Open **http://127.0.0.1:8000/?v=5**. If an old site loads, stop old servers on port 8000 and press **Cmd+Shift+R** in Chrome.

If you do not know where your prior `.env` is, see `docs/MYSQL_SETUP.md`. Do not create another database or re-import your research tables unless your database is empty.

## Quick demonstration for judges

Choose **Japan → UK**, tuition **2,500 GBP**, available funds **800,000 JPY**, reserve **50,000 JPY**, and a deadline twenty days away. Fetch a published rate; if the API is unavailable, enter a rate as **sample input** (for example `185 JPY per GBP`, which is illustrative, **not a verified current rate**). Compare the three fictional options, approve the test payment, then display the receipt and the audit record. The system should keep the reserved money and prevent duplicate payments.

## Project limits to disclose

- Not a licensed payment processor; no actual provider integration or payments.
- Quote comparison in the other planner still relies on user-entered bank quotes and source checks.
- Built-in application authorization is insufficient for public production use. Do not publish a public instance with real user data; add identity verification, access controls, secure secrets, rate limiting and privacy protections first.
- Published tuition, FX and credit data need current source verification before live financial use.
- PDF reports and slides from previous builds are **draft competition materials**, not newly verified descriptions of the V5 checkout. Update them before submission.
