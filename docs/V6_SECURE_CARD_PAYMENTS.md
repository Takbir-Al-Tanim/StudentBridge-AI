# StudentBridge AI — Secure Card Checkout (V6)

## What changed?

The Payments page has a large **Pay securely by card** section. A student can
continue to a payment provider's secure website to enter the card number,
expiration date, CVC, payer email, and **required billing address**.
**StudentBridge never collects or stores raw card details.** A provider confirms
payment and sends signed webhook events. Our audit log stores only limited
payment status and provider references.

When no merchant account is configured, the button is disabled and the app
explains why. The existing payment practice flow remains available and is clearly
marked as **test only**; it does not move real money.

## Requirements before any live card payment

You must be an approved merchant allowed to collect this particular tuition or
invoice payment. A normal card payment charges **your merchant account**, it does
NOT automatically send money to a university or create a legal cross-border
remittance. You need the university/beneficiary's authorization, a legitimate
payment purpose and any licensing/contract required for your circumstances.

Stripe merchant accounts are not available in every country. Check
https://stripe.com/global and local financial rules first. Do not use a friend's
or another country's merchant account without genuine eligibility.

## Connect a provider in test mode first

1. Set up a valid Stripe merchant account **if your business is eligible**.
2. In Stripe Dashboard create one authorized, fixed-price one-time item for a
   specific invoice that **your merchant is permitted to collect**.
3. In your local `.env` set `STRIPE_SECRET_KEY=sk_test_...`,
   `STRIPE_PRICE_ID=price_...`, `AUTHORIZED_PAYEE_NAME=...`,
   `AUTHORIZED_INVOICE_REFERENCE=...`, and `PUBLIC_BASE_URL=http://127.0.0.1:8000`.
4. Keep `CARD_LIVE_ENABLED=false` and `MERCHANT_AUTHORIZED_TO_COLLECT=false`.
5. Install packages: `python -m pip install -r requirements.txt` and start `python run.py`.
6. On Payments, choose **Continue to secure card payment**. Only use Stripe's
   **published test card numbers** for test checkout, not an actual card number.
7. For a webhook test, Stripe CLI may forward events to `/api/card/webhook`;
   configure a `STRIPE_WEBHOOK_SECRET=whsec_...`.
8. A payment success return is not proof of settlement. StudentBridge checks
   the Checkout Session directly, and live webhook events need valid signatures.

## Conditions for live operation (do not enable just to test the website)

Only after merchant eligibility, institutional authorization, confirmed invoice
ownership, exact price configuration, backend authentication, fraud/AML safeguards,
required privacy and payment-service controls, a public HTTPS domain, and tested
webhooks may an authorized operator use `sk_live_...` with
`APP_ENV=production`, `CARD_LIVE_ENABLED=true`,
`MERCHANT_AUTHORIZED_TO_COLLECT=true`, and `PUBLIC_BASE_URL=https://your-domain`.
This example code is a starting integration, **not a certification that your
organization can legally accept tuition payments**. Production hardening,
client authentication/authorization, CSRF controls, rate limits, full webhook
reconciliation, reconciliation and refund/dispute processes are still required.
Do not turn it on publicly without those controls.

## Data safety

Never write card number, expiration date, CVC, password, or Stripe secret key
into StudentBridge forms, SQL tables, screenshots, logs, or GitHub.
Billing address is collected and stored by the provider under its own privacy
controls and is not written into the StudentBridge database.

## XAMPP MySQL

Existing ten tables remain intact. A minimal `provider_events` table will be
created automatically when the backend starts, if the database user has CREATE
permission. It records webhook event IDs for idempotent processing.
Run `python scripts/check_mysql.py` to confirm connectivity.
