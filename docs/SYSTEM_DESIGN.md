# Technical Architecture and Algorithm Description

## 1. Problem

An international student faces tuition amounts, multiple payment currencies, bank FX spreads, transfer charges, deadlines, incomplete country-pair eligibility data, unpredictable living expenses and unfamiliar destination credit systems. Many general-purpose converters do not jointly address these needs.

## 2. Objective

Provide explainable **decision support** for any of 30 ordered country pairs formed by China, UK, Japan, South Korea, Australia and Bangladesh, plus a safe, approved simulated execution as proof of task completion. No claim is made that all 30 real-money corridors are available.

## 3. Architecture

**Presentation layer:** One responsive HTML/CSS/JS dashboard with Planner, Digital Twin, Credit Navigator, Source Registry, Decision Passport, Sandbox Ledger, Grounded Copilot.

**API layer:** Python FastAPI and Pydantic schema validation. A successful live reference-rate request also returns a time-limited HMAC proof; the planner verifies that proof server-side before labeling a user-transmitted rate as truly API-backed. Important endpoints: `GET /api/catalog`, `GET /api/fx`, `POST /api/plans`, `GET /api/passport/{id}`, `POST /api/scenarios`, `POST /api/sandbox/execute`, `POST /api/invoices/analyze`, `GET /api/credit/{country}`, `POST /api/chat`, `GET /api/audit`.

**Deterministic finance layer:** `app/logic.py` uses `Decimal` arithmetic for core calculations, quantizes to 2 decimal places for display, checks hard safety constraints before ranking.

**Grounded agent layer:** Intent-based function calls return factual output. Optional Gemini integration only rephrases deterministic context; the LLM cannot call transaction execution.

**Storage layer:** **MySQL 8.0 database** for plans, approval-based simulated transactions, HMAC-chained audit events and all six research tables. SQLAlchemy + PyMySQL give parameterized statements; plan/transaction + audit writes are atomic. HMAC chain updates lock the MySQL chain-head row. Read-only source registry/academic catalog is JSON with provenance and source dates.

## 4. EduRoute algorithm

Let `T` be the invoice tuition in destination currency and `S` the confirmed scholarship reduction. Required tuition `R=max(T-S,0)`.

For a provider quote `q`, with provider sell rate `r` (origin currency per one destination currency), percentage fee `p` and fixed fee `f` in origin currency, base cost `B=R×r`, fee `F=B×p/100+f`, total `C=B+F`.

`deadline_ok = quoted_eta_days <= remaining_days` (only an estimate). `affordable = C <= available_funds - protected_reserve`. `eligible = student_acknowledged_provider_eligibility`. Quotes missing a source URL are flagged (not silently treated as verified). Expired quotes are rejected. A viable option requires eligibility, deadline and affordability, and no expiry error. Among viable quotes, rank primarily by ascending total cost and secondarily by arrival estimate.

**Important:** `eligible` is a *user assertion*, not an automated regulator/provider determination; therefore the output remains a **conditional quote ranking**, never a verified real-world bank recommendation.

When no quote is viable, return a refusal to recommend with an explanation. A real reference FX observation without fees never generates a provider quote.

## 5. Financial Digital Twin

Apply a user-selected percentage shock `s` to the quoted conversion base: `B' = B × (1+s/100)`. Recalculate percentage transfer fee, add fixed fee plus user-selected incremental costs, compare the result to baseline. Check whether protected reserve remains intact. Recompute destination living-cost budget separately with a user-selected living-cost shock.

The simulation is a counterfactual what-if calculator, **not an FX forecast** or probabilistic claim. User-specified scenarios are hypothetical even if the base price comes from a real quote.

## 6. Decision Passport

The passport contains a plan identifier, created timestamp, goal, input constraints, each quote's calculated cost and rejection reasons, recommendation, reference FX provenance and caution labels. Every plan includes a SHA-256 integrity fingerprint of the deterministic result before the ID and fingerprint are attached. This is a local integrity indicator, not third-party notarization.

## 7. Invoice document analysis

The invoice endpoint processes only PDF bytes (`%PDF` signature), limited to 2.5 MB and 12 pages. PyMuPDF extracts text; conservative regular expressions surface **candidate** amounts and ISO-formatted dates. The student confirms these inputs manually. File text is never run as code or agent instructions. No recipient/bank account verification, OCR or invoice-fraud certification is claimed.

## 8. Agent reasoning and tool decisions

The assistant selects a trusted tool path based on task intent. Credit questions retrieve country guidance with primary references. Route questions return the deterministic planner decision and label quotes as user entered. Budget questions report entered funds and availability. Tuition questions select official published tuition records when available. Optional Gemini makes the text easier to read but does not create numbers or authorization decisions. There is no external agent execution autonomy in this MVP.

## 9. Testing

Automated tests exercise core arithmetic, scholarships, deadline constraints, eligibility assertions, emergency reserve, expired quotes, no-offer response, FX stress shocks, wrong currencies, explicit approval, duplicate idempotency, invoice type checks, country coverage and grounded tool selection. Run `python -m pytest -q`.

## 10. Improvements after the competition

Commercial provider quotation APIs with authenticated quote/eligibility/expiry, payment corridor rules reviewed by local counsel, actual student invoice beneficiary verification, user authentication, HTTPS deployment, encryption-at-rest, rate limiting, secrets management, signed audit attestations, accessibility audit, locale/currency rounding rules, price snapshotting, OCR, production observability, rigorous bias and robustness evaluation. None is represented as complete in the current package.

## 11. MySQL 8 deployment design (15 October 2026)

Persistent application and research data are stored in ten MySQL tables. The schema is generated as `scripts/mysql_schema.sql`; corrected official research CSV rows can be safely imported with `scripts/setup_mysql.py`. Foreign keys are used for plans/transactions, research sources, country codes and source metadata. MySQL InnoDB provides ACID transactions and row locking for serializing chained audit entries. Each sandbox transaction and its audit event use a single database transaction. Idempotency keys have a database-level UNIQUE constraint to prevent duplicate writes. Missing provider quotes remain NULL and are not made actionable. No real banking integration or real student records are included. Automated unit tests run in disposable isolated SQLite only and live MySQL smoke verification is a separate step; user must test actual MySQL deployment.
