# StudentBridge AI V10 — Transfer & Comparison Upgrade

## What changed

- **Send money**: replaced the browser-side exchange calculator with a two-column banking-style form for country pair, sender name, amount, beneficiary, bank name, bank account, local routing/clearing code, receiving area, and optional SWIFT/BIC.
- **Country-specific formats**: Bangladesh routing (9 digits), Australian BSB (6), UK sort code (6), China CNAPS (12), Japan bank/branch (4-3), and South Korean bank code (3), plus country-specific account format checks. These checks validate **format only**; they do not verify bank ownership or whether a corridor is supported by a bank.
- **Visa / Mastercard**: separated from bank transfer. Card entry is never handled by the StudentBridge website. The pre-existing Stripe-hosted *tuition invoice checkout* remains behind provider/merchant configuration in the **Tuition payments** page. It is **not** an arbitrary person-to-person card remittance service.
- **Server validation**: `POST /api/transfers/quote` runs validation and obtains published FX from the backend. `POST /api/transfers/prepare` verifies the HMAC-signed, 15-minute review token and checks for changed details before returning an audit-only reference. Neither endpoint sends funds.
- **Sensitive data handling**: signed tokens contain only a SHA-256 digest of the full submitted details, reference FX, expiry and nonce. Full bank account and beneficiary fields are not written to MySQL. Server responses show account last four digits only. For real use, enforce HTTPS, user authentication, rate limits at the edge, privacy policies, and an appropriate financial/regulatory/compliance program.
- **Compare payment routes**: condensed into three small steps: country pair, invoice/available amount/deadline (PDF upload alongside), and documented bank quotes. Extra budget fields are inside **More options** and quote delivery options are collapsed by default. Important evidence-link and eligibility confirmation stay visible.
- **PDF invoices**: uploads now show progress, clear errors, selectable amount/date suggestions and manual-entry fallback for scanned PDFs. Upload limit 4 MB and 12 pages; backend checks PDF header and MIME type. No OCR is included; text-only extraction with pypdf is used.
- **Rates**: Frankfurter is the preferred published reference. If unavailable, the server may use the [ExchangeRate-API open feed](https://www.exchangerate-api.com/docs/free), taking USD cross-rates. The provider observation date and original source URL are shown. Neither source is a guaranteed bank quote.
- **Styling**: new `app/static/finance-v10.css` added last; consistent system sans-serif typography, responsive panels and controls.

## Endpoints

`GET /api/transfers/requirements` — country-specific fields and fixed-invoice card-provider availability.

`POST /api/transfers/quote` — validated bank account details plus published reference-rate review. Requires JSON and `X-SB-Intent: transfer-review` same-origin browser request; errors 422 for invalid input or 503 when no published source is reachable.

`POST /api/transfers/prepare` — takes the **unchanged** `details`, `quote_token`, and `confirmed: true`; verifies expiry and HMAC token; returns `INSTRUCTIONS_PREPARED_ONLY`. This makes an audit event **not a bank transfer**.

`POST /api/invoices/analyze` — PDF multipart file upload, file key `file`; responds with candidate amounts and dates, warnings and text status.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Update .env with your MySQL database and a long, random APP_SECRET.
python run.py
```

Do **not** commit `.env`, `STRIPE_SECRET_KEY`, or real bank credentials. For local tests with an isolated SQLite database, `python -m pytest -q tests` uses a dedicated test mode. Do not enable SQLite mode in production.

## Deploy on Render with GitHub

From the unzipped `StudentBridge_AI` directory, copy changed files into the same GitHub repository (keeping relative paths), commit and push, and let the linked Render service redeploy. Existing typical build command is `pip install -r requirements.txt` and start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`; use the values configured in your Render dashboard. Verify environment variables there; do not paste secrets into the UI or source repo. Hard refresh after deploy to get `?v=10.0` assets.

## Boundaries / before accepting real payments

This app is a **decision-support prototype**. It has no verified end-user login, bank settlement provider, compliance/AML controls, beneficiary confirmation service or protection against anonymous abuse at scale. Therefore it must **not** accept or send arbitrary real transfers. Connecting a licensed transfer partner, authenticating users, obtaining payment regulatory/legal approval, production key management, payment reconciliation, antifraud monitoring, and penetration testing are required for a real money-movement product. Hosted card checkout, when configured, is restricted to one merchant-authorized invoice.
