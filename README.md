# StudentBridge AI

**Cross-Border & Student Finance Assistant**  
*Topic C — FinTechathon*

StudentBridge AI helps international students understand tuition costs, plan living expenses, review cross-border payment details, compare estimated payment routes, and learn financial basics before studying abroad. It combines a responsive website, an explainable Python backend, a research-backed data registry, and an optional AI explanation assistant.

**Project repository:** [Takbir-Al-Tanim/StudentBridge-AI](https://github.com/Takbir-Al-Tanim/StudentBridge-AI)  
**API documentation when running locally:** `http://127.0.0.1:8000/docs`  
**Application health endpoint:** `http://127.0.0.1:8000/api/health`  
**Detailed system architecture:** [SYSTEM_ARCHITECTURE.md](docs/SYSTEM_ARCHITECTURE.md)

![StudentBridge AI home screen](docs/screenshots/01-home.png)

> **Important:** StudentBridge AI is an educational finance-planning and demonstration system, **not a bank or licensed remittance provider**. A bank-transfer review only prepares instructions; it never moves money. Payment history and receipts are sandbox records. Card payment requires a separately authorized provider-hosted checkout, which is disabled unless properly configured. Never upload live banking credentials, real card numbers, private student invoices or sensitive recipient data to a public demo.

## Contents

1. [Problem and solution](#1-problem-and-solution)
2. [What the project offers](#2-what-the-project-offers)
3. [Supported countries and currencies](#3-supported-countries-and-currencies)
4. [Website features and screenshots](#4-website-features-and-screenshots)
5. [System architecture](#5-system-architecture)
6. [How the main flows work](#6-how-the-main-flows-work)
7. [Financial decisions and AI](#7-financial-decisions-and-ai)
8. [Data and database design](#8-data-and-database-design)
9. [Project structure](#9-project-structure)
10. [Installation and local run](#10-installation-and-local-run)
11. [Configuration and MySQL](#11-configuration-and-mysql)
12. [Deployment on Render](#12-deployment-on-render)
13. [API reference](#13-api-reference)
14. [Testing](#14-testing)
15. [Security and limitations](#15-security-and-limitations)
16. [Presentation walkthrough](#16-presentation-walkthrough)
17. [Troubleshooting and useful links](#17-troubleshooting-and-useful-links)

---

## 1. Problem and solution

Students preparing to study abroad often need to make several financial decisions at once: pay tuition in a different currency, estimate fees and exchange-rate spreads, arrange the right beneficiary information, meet university deadlines, and protect money for rent, food and emergencies. A simple currency converter does not explain all these risks.

**StudentBridge AI brings these tasks into one website.** Students can build a guided budget, use a bank-style transfer-review flow, compare indicative payment methods, read source-linked financial information, and ask an assistant to explain their options in simple language. Where information cannot be verified, the application shows that limitation instead of claiming to provide a live bank quote.

The main objective is **clearer financial decisions before any real-world payment**.

## 2. What the project offers

| Capability | What it does | Important boundary |
|---|---|---|
| Profile | Creates a temporary demonstration sign-in and displays profile details | No verified identity, persistent account database or production authentication |
| Saved beneficiaries | Adds and selects recipient bank details during the current application session | Stored in server memory; not persistent or appropriate for real recipient records |
| Send money | Guides user through country, recipient, bank details, method, and final review | Produces **instructions only**; does not send funds |
| Compare payment routes | Shows three indicative methods with modeled costs and timing | Not live quotes or validated provider offers |
| Tuition payments | Guides users through a practice tuition flow and sandbox receipt | Real payment collection is disabled without separate merchant authorization |
| Journey Studio | Combines tuition, scholarship, savings, living costs and deadline | Read-only planning; official invoice and provider terms still need checking |
| Invoice PDF extraction | Finds candidate dates and amounts in text-selectable PDFs | No OCR, recipient verification or automatic acceptance of extracted values |
| My currencies | Estimates totals for manually entered currency balances | Not connected to bank accounts |
| My budget | Runs what-if shocks on a saved detailed plan | Simplified route comparison alone does not create that saved plan |
| Build credit | Gives country guidance and a readiness checklist | Not a credit-scoring or lending service |
| Data sources | Shows published research benchmarks and provenance | Historical or published figures are not live executable offers |
| Decision Passport | Explains detailed plan results and their local fingerprint | Not an externally certified financial decision |
| Ask Bridge AI | Answers finance questions using app tools and sources | Optional Gemini improves wording but cannot authorize transfers |
| Payment history | Shows practice transaction and audit records locally | Restricted for public production configuration |

## 3. Supported countries and currencies

| Country | Currency | Code |
|---|---|---|
| Bangladesh | Bangladeshi taka | BDT |
| China | Chinese yuan | CNY |
| United Kingdom | Pound sterling | GBP |
| Japan | Japanese yen | JPY |
| South Korea | South Korean won | KRW |
| Australia | Australian dollar | AUD |

The application allows **30 directional selections** between different countries. This is a planning scope, **not a claim that 30 real-world bank-transfer corridors are approved**. Actual payment availability depends on the bank or provider, the law, the recipient, the currency, and the type of transaction.

## 4. Website features and screenshots

Screenshots below are illustrative captures of the **provided project interface**. They show local page layouts with sample or unfilled fields, not verified live bank connections, an authenticated production account, real payment settlement, or a deployed website. The screenshots belong in `docs/screenshots/` alongside the README in GitHub.

### 4.1 Home

![Home screen](docs/screenshots/01-home.png)

The dashboard links to Journey Studio, Send money, Tuition payments, Compare payment routes, My currencies, My budget, Build credit, Data sources, and Payment history. The sidebar includes **My profile**. Students can also open **Ask Bridge AI**.

### 4.2 My profile and temporary sign-in

![Profile and saved beneficiaries](docs/screenshots/15-profile-and-beneficiaries.png)

The user enters a name, email, home country and password to create a **demonstration session** and open their profile. The backend does **not** verify the password against a stored account. The server holds the profile and saved beneficiaries in memory, associated with a session cookie. Data may disappear after server restart, logout or deployment replacement. Do not describe this as secure bank login.

### 4.3 Send money — guided bank-transfer review

![Guided transfer review](docs/screenshots/03-send-money.png)

The page uses a multi-step layout:

1. Select the sending and receiving countries and enter a transfer amount.
2. Enter or choose a beneficiary, including name, bank, account number and destination-specific routing details.
3. Select an available **review** method. Card funding points to the separate tuition checkout flow.
4. Review the server-generated estimated amount, source date, beneficiary summary and warning.
5. Explicitly confirm the details to prepare bank-transfer instructions, **not to execute a transfer**.

Where the user signs in, the **Add beneficiary + save** option can store up to 12 recipients in their temporary application session. The server validates account/routing formats and uses a short-lived signed review token. A recipient being format-valid does **not** establish that the account exists or belongs to the intended beneficiary.

### 4.4 Compare payment routes — simplified form

![Compare payment routes](docs/screenshots/05-route-comparison.png)

The user chooses the sending country, university country, amount, and optional deadline or university name. They may also upload a text-selectable tuition PDF to review candidate amount and due-date fields.

The backend returns **three illustrative route types**: a student remittance partner, a bank transfer, and a Visa/Mastercard route. Cost estimates use a published reference exchange rate and **modeled fee and markup assumptions** defined in the application. They are not verified provider prices. The displayed recommendation is an illustrative preference based on the model, not a real availability or eligibility check; an urgent deadline may favor the card illustration even if the user has no authorized checkout provider.

For research-grade comparisons of **student-entered actual quotes**, the application also has the more detailed `POST /api/plans` engine. That detailed workflow checks user-entered fees, quote evidence, affordability, estimated delivery, and expiration. Do not confuse its results with the simpler on-screen three-card comparison.

### 4.5 Journey Studio and invoice reader

Journey Studio receives the student's tuition amount, confirmed scholarship amount, savings, protected emergency reserve, monthly living costs, planned months, and deadline. It prepares a combined financial summary, reference-rate assumptions, hypothetical FX stress results, and suggested steps. It can generate an `.ics` calendar reminder for manual import.

The PDF invoice reader supports **PDF files smaller than 4 MB and no more than 12 pages** when text is selectable. It returns candidate fields for user confirmation, not a verified invoice or approved bank beneficiary. Scanned image-only PDFs may require manual entry.

### 4.6 Tuition payments and sandbox records

The tuition section prepares a practice-only payment experience. In the authorized sandbox path, users review a payment, explicitly approve it, and may get a simulated receipt. No tuition reaches a university. Optional live merchant checkout is guarded by configuration and separate provider authorization. The project does not contain a general Visa/Mastercard transfer gateway and does not collect card numbers or CVC on its own forms.

### 4.7 My currencies, My budget and Decision Passport

**My currencies** accepts manually entered balances across the supported countries and converts them using reference data where available. **My budget** applies an FX percentage change, added fee or changed living costs to a previously saved detailed plan. A simplified comparison result does not automatically create that plan. **Decision Passport** explains the detailed planner's assumptions, candidate decisions, warnings, and SHA-256 fingerprint.

### 4.8 Build credit, Data sources, Payment history and Ask Bridge AI

**Build credit** explains general banking/credit preparation for a destination country. **Data sources** separates original sources, historical research records, reference exchange rates, and unverified fields. **Payment history** is for sandbox activity only and its shared history/audit listing endpoints are blocked when `APP_ENV=production`. **Ask Bridge AI** selects known financial information and tools, with optional Gemini wording assistance.

---

## 5. System architecture

![StudentBridge AI system architecture](docs/diagrams/system-architecture.png)

**Editable architecture file:** [`docs/diagrams/system-architecture.drawio`](docs/diagrams/system-architecture.drawio)  
**Diagram document:** [`docs/SYSTEM_ARCHITECTURE.md`](docs/SYSTEM_ARCHITECTURE.md)

The browser communicates through HTTPS/JSON with **FastAPI**, which validates inputs and dispatches requests to finance rules, transfer review, session/beneficiary handling, Journey Studio, invoice reading and the source-aware assistant. **MySQL** stores detailed plans, research records, simulated transactions and integrity audit events. Published reference FX comes from **Frankfurter**. Optional **Gemini** produces wording help; optional separately authorized **Stripe-hosted Checkout** is guarded and disabled by default.

### 5.1 Application architecture (GitHub-compatible diagram)

```mermaid
flowchart TB
    U["Student browser"] --> W["HTML CSS JavaScript interface"]
    W --> API["FastAPI and Pydantic validation"]
    API --> SESSION["Temporary profile and beneficiaries"]
    API --> TRANSFER["Transfer review and signed estimate"]
    API --> ROUTE["Simple routes and detailed finance rules"]
    API --> JOURNEY["Journey planning and invoice review"]
    API --> ASSIST["Source-aware finance assistant"]
    API <--> MYSQL[("MySQL research plans sandbox and audit")]
    API <--> FX["Frankfurter reference exchange rates"]
    ASSIST -.-> GEMINI["Optional Gemini wording service"]
    API -.-> CHECKOUT["Guarded provider-hosted checkout"]
    SESSION --> API
    TRANSFER --> API
    ROUTE --> API
    JOURNEY --> API
    ASSIST --> API
    API --> W
```

### 5.2 Request sequence (GitHub-compatible diagram)

```mermaid
sequenceDiagram
    actor Student
    participant UI as Browser
    participant API as FastAPI
    participant FX as Reference FX service
    participant Rules as Finance rules
    participant DB as MySQL
    Student->>UI: Choose countries and enter details
    UI->>API: POST /api/routes/compare
    API->>FX: Request reference exchange rate
    alt Rate is available
        FX-->>API: Dated rate and source
        API->>Rules: Calculate illustrative route costs
        Rules-->>API: Modeled costs and explanatory notes
        API-->>UI: Route cards and source information
    else Rate is unavailable
        FX-->>API: No usable reference rate
        API-->>UI: Show unavailable rate warning
    end
    UI-->>Student: Display planning guidance only
    Note over UI,DB: No bank transfer takes place during comparison
```

### 5.3 Bank-transfer review (not execution)

```mermaid
flowchart TD
    A["Enter corridor and recipient"] --> B["Check required details"]
    B --> C["Look up dated reference rate"]
    C --> D["Create signed estimate with limited validity"]
    D --> E{"Student reviews and confirms"}
    E -->|No| STOP["Stop without preparation"]
    E -->|Yes| REVIEW["Validate review token"]
    REVIEW --> AUDIT["Write masked audit event"]
    AUDIT --> END["Prepare instructions only"]
```

The detailed system, deployment, trust boundaries, and storage relationships are explained in the separate architecture document.

## 6. How the main flows work

**Profile and saved beneficiaries:** `app/main.py` defines `/api/auth/profile`, `/api/auth/login`, `/api/auth/logout` and `/api/beneficiaries`. These endpoints use temporary in-memory session state. Logging in is not identity verification; recipient details should be synthetic for demonstrations.

**Bank-transfer review:** `app/transfer_flow.py` validates destination account and bank routing formats, calculates an indicative received amount from a published reference rate, issues a short-lived HMAC-protected review token, and verifies the token on final confirmation. `/api/transfers/prepare` returns a reference and instructions with masked account details, never a real transfer receipt.

**Simple comparison:** `/api/routes/compare` builds indicative partner, bank and card cases from application-defined fee assumptions. It requires reference FX availability and returns cards sorted by modeled debit amounts. This is a decision-support illustration, not proof of a licensed or available provider.

**Detailed finance planner:** `app/logic.py` checks the origin and destination, currencies, tuition amount, scholarship, fees, declared eligibility, deadlines, quote evidence and available funds. Eligible user-entered quotes are evaluated with deterministic financial rules before comparison. `app/journey.py` handles guided financial planning.

**Invoice reader:** `/api/invoices/analyze` inspects limited PDF content and returns potential amounts and dates. The student must check the original official invoice before using any candidate field.

**Evidence and assistant:** `app/assistant.py` builds answers from the project catalog, source registry, credit guidance and available calculations. Gemini is optional and does not control the deterministic decision rules.

## 7. Financial decisions and AI

### 7.1 Example of a detailed entered-provider calculation

For each student-entered provider quote in the detailed planner:

```text
Tuition still due = max(Tuition - Confirmed scholarship, 0)
Conversion cost = Tuition still due × Entered sell rate
Percentage charge = Conversion cost × (Fee percentage / 100)
Total modeled debit = Conversion cost + Percentage charge + Fixed charge
```

The planner then checks estimated arrival against the payment deadline, the remaining balance after protected savings/living costs, submitted quote evidence, declared eligibility and quote expiration. It reports why a quote is rejected rather than silently hiding it. Quoted eligibility is **user-provided**, not verified with a regulator or bank.

### 7.2 Example (fictional values)

A student owes 17,000 GBP after scholarship. An example quote uses 190 JPY per GBP with a 1% percentage fee and a 1,000 JPY fixed fee:

```text
Conversion: 17,000 × 190 = 3,230,000 JPY
Percentage charge: 3,230,000 × 0.01 = 32,300 JPY
Fixed charge: 1,000 JPY
Estimated total: 3,263,300 JPY
```

This is not a live provider quote. The simple three-card comparison uses a **different** modeled-fee calculation defined in `/api/routes/compare`.

### 7.3 AI rules

The AI can explain the calculations, source links and possible next steps. It cannot invent or certify a provider offer, verify a beneficiary bank account, or approve a payment. When optional Gemini is unavailable, the core deterministic features and grounded assistant responses remain available.

## 8. Data and database design

The application runtime uses **MySQL** through SQLAlchemy and PyMySQL, with **11 tables**:

| Table | Stored content |
|---|---|
| `countries` | Supported countries and currency information |
| `sources` | Publisher references and links |
| `financial_benchmarks` | Financial and living-cost research benchmarks |
| `tuition_benchmarks` | Tuition-related research records |
| `fx_rates` | Historical/reference exchange rate observations |
| `payment_quotes` | Research quote records with verification status |
| `plans` | Detailed comparison requests and result fingerprints |
| `transactions` | Simulated transaction records |
| `audit` | HMAC-linked event log |
| `audit_chain_state` | Integrity chain-head state |
| `provider_events` | Optional provider-hosted checkout event references |

**Important:** temporary session profiles and saved beneficiaries are **not stored in these tables**. They exist only in application memory. Research data provenance is tracked separately from independently verified bank quotations; these are not interchangeable.

The data layer is in `app/database.py`. The safe initializer and database check scripts are `scripts/setup_mysql.py` and `scripts/check_mysql.py`. `scripts/mysql_schema.sql` documents the database schema. For a relationship diagram, see [SYSTEM_ARCHITECTURE.md](docs/SYSTEM_ARCHITECTURE.md#6-data-relationships).

## 9. Project structure

```text
StudentBridge_AI/
├── app/
│   ├── main.py                 # FastAPI routes, temporary profile sessions
│   ├── transfer_flow.py        # Beneficiary validation and transfer review
│   ├── logic.py                # Detailed planner and stress calculations
│   ├── journey.py              # Journey Studio and calendar export
│   ├── assistant.py            # Grounded finance assistant
│   ├── database.py             # MySQL storage and integrity audit
│   ├── secure_card.py          # Optional guarded hosted checkout
│   ├── data/                   # Catalog, sources and country guidance
│   ├── templates/index.html    # Web interface and feature sections
│   └── static/                 # JavaScript and CSS
├── data/research/corrected/    # Research CSV data
├── docs/
│   ├── SYSTEM_ARCHITECTURE.md  # Architecture explanation and diagrams
│   ├── diagrams/               # PNG, SVG and editable draw.io source
│   └── screenshots/            # README interface illustrations
├── scripts/                    # Database setup, schema, checks
├── tests/                      # Automated tests
├── evidence/                   # Included demonstration test records
├── certs/                      # Public database CA certificate if used
├── .env.example                # Configuration template
├── .gitignore                  # Excludes local sensitive material
├── docker-compose.yml         # Optional local MySQL
├── requirements.txt            # Python dependencies
├── run.py                      # Development entry point
└── README.md                   # Documentation
```

## 10. Installation and local run

The project requires a compatible Python environment and a MySQL database for normal runtime. **macOS instructions:**

```bash
# In the project directory containing requirements.txt and run.py
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

Edit the **private** `.env` and set a valid `DATABASE_URL`, `APP_SECRET` and other needed settings. Then run:

```bash
python scripts/setup_mysql.py
python scripts/check_mysql.py
python run.py
```

Open `http://127.0.0.1:8000`. API docs are at `http://127.0.0.1:8000/docs`. To stop, use `Ctrl+C`.

For Windows PowerShell, create the virtual environment using `py -m venv .venv`, activate using `.\.venv\Scripts\Activate.ps1`, and replace `cp` with `Copy-Item .env.example .env`. The remaining Python commands are the same.

**Tip:** A Python backend is required. Opening `index.html` directly in a browser does not start FastAPI, load the database, or make the buttons work.

## 11. Configuration and MySQL

Do not commit `.env`, real personal data, database passwords, API keys or private certificates to GitHub.

| Environment variable | Purpose |
|---|---|
| `DATABASE_URL` | SQLAlchemy MySQL connection URL |
| `APP_SECRET` | Long random secret for signed information and audit integrity |
| `APP_ENV` | `development` locally or `production` for a deployed service |
| `GEMINI_API_KEY` | Optional Gemini explanation support |
| `GEMINI_MODEL` | Optional configured Gemini model |
| `CARD_LIVE_ENABLED` | Keep `false` unless explicitly authorized |
| `MERCHANT_AUTHORIZED_TO_COLLECT` | Keep `false` for a normal competition demo |
| `PUBLIC_BASE_URL` | HTTPS public base URL if hosted checkout is authorized |
| `STRIPE_SECRET_KEY`, `STRIPE_PRICE_ID`, `STRIPE_WEBHOOK_SECRET` | Optional authorized provider-hosted checkout only |
| `AUTHORIZED_PAYEE_NAME`, `AUTHORIZED_INVOICE_REFERENCE` | Optional verified checkout constraints |

Generate a strong secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

A local MySQL URL follows this shape (replace with your **own private** details):

```dotenv
DATABASE_URL=mysql+pymysql://USER:URL_ENCODED_PASSWORD@127.0.0.1:3306/studentbridge_ai?charset=utf8mb4
APP_ENV=development
APP_SECRET=YOUR_LONG_RANDOM_SECRET
CARD_LIVE_ENABLED=false
MERCHANT_AUTHORIZED_TO_COLLECT=false
```

Choose **one** MySQL host: existing XAMPP/MySQL, the supplied local Docker Compose service, or a managed provider such as Aiven or Railway. Managed services may require TLS parameters and a correct CA certificate. Never paste a real credential-filled database URL into a README.

For Docker MySQL, configure the private passwords from `.env` and run `docker compose up -d mysql`. Beware that `docker compose down -v` removes the named data volume. The application must not be deployed with a test-only SQLite URL.

## 12. Deployment on Render

1. Upload the project to the GitHub repository, excluding `.env`, `.venv`, local database dumps, and secrets.
2. Create a **Render Web Service** connected to the repository's `main` branch.
3. Set the language to Python, the build command to `pip install -r requirements.txt`, and the start command to:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. In Render environment variables, enter the correct **private** `DATABASE_URL`, a strong `APP_SECRET`, `APP_ENV=production`, and any optional permitted integration keys.
5. Keep the card-payment authorization flags disabled unless a genuine, properly approved integration is configured.
6. Check Render logs and visit your **actual** published URL. Confirm `/api/health` works with the production MySQL database.

**The live Render URL is not verified from the uploaded project and is intentionally not invented here.** Do not claim the deployment is working without opening it and testing the routes.

After editing documentation or code locally:

```bash
git status
git add README.md docs/ app/ tests/ scripts/ data/ requirements.txt
git diff --cached --name-only
git commit -m "Update StudentBridge AI documentation"
git push origin main
```

Do not commit files from `.env` or `.venv`. If secrets were previously uploaded to GitHub, rotate them; deleting a visible file does not erase older commit history.

## 13. API reference

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Main website |
| GET | `/api/health` | Service and database status |
| GET | `/api/catalog` | Country catalog and source registry |
| GET | `/api/auth/profile` | Temporary session profile |
| POST | `/api/auth/login` | Create a demo session |
| POST | `/api/auth/logout` | End a demo session |
| GET | `/api/beneficiaries` | List saved temporary beneficiaries |
| GET | `/api/beneficiaries/{beneficiary_id}` | Read session beneficiary |
| POST | `/api/beneficiaries` | Save session beneficiary |
| GET | `/api/transfers/requirements` | Country-specific recipient field rules |
| POST | `/api/transfers/quote` | Estimate and sign transfer review |
| POST | `/api/transfers/prepare` | Confirm and prepare instructions only |
| POST | `/api/routes/compare` | Three illustrative payment-route estimates |
| GET | `/api/fx` | Reference exchange-rate observation |
| POST | `/api/journey/prepare` | Guided financial summary |
| GET | `/api/journey/calendar` | Download tuition reminder |
| POST | `/api/invoices/analyze` | Extract candidate PDF fields |
| POST | `/api/plans` | Detailed quote evaluation and saved plan |
| GET | `/api/plans/{plan_id}` | Retrieve detailed plan |
| POST | `/api/scenarios` | Stress-test a detailed plan |
| GET | `/api/passport/{plan_id}` | Explainable decision record |
| POST | `/api/demo/prepare` | Prepare example tuition workflow |
| POST | `/api/sandbox/execute` | Explicitly approved simulation |
| GET | `/api/sandbox/receipt/{transaction_id}` | Practice receipt |
| GET | `/api/credit/{country}` | General country credit guidance |
| POST | `/api/chat` | Source-aware assistant |
| GET | `/api/research/summary` | Research dataset overview |
| GET | `/api/research/benchmarks` | Published benchmark records |
| GET | `/api/sandbox/history` | Development-only shared sandbox history |
| GET | `/api/audit` | Development-only shared audit log |
| GET | `/api/audit/verify` | Development-only audit integrity check |
| GET | `/api/card/availability` | Optional hosted-checkout status |

Additional guarded card checkout session/webhook paths exist in `app/main.py`. In production, the shared history and audit-list endpoints return 403 by design. Use the interactive local API reference for request/response field details.

## 14. Testing

Run tests from the project root:

```bash
python -m pytest -q tests
node --check app/static/app.js
python -m compileall -q app
```

**Validation of the uploaded project files during this documentation review:**

```text
85 passed
JavaScript syntax check: passed
Python compile check: passed
```

Unit/API tests use a temporary isolated SQLite database in an **explicit test mode**; this is **not** the normal runtime database. Tests do not prove a public Render deployment, Aiven/Railway connection, live FX availability, real card integration or security certification. Separately check a live configured database with `python scripts/check_mysql.py`.

Recommended manual checks: load the home page, navigate to **My profile**, create a demo session, save an example beneficiary, review a sample transfer without executing it, compare sample route cards, inspect the invoice reader with a synthetic PDF, ask the assistant a basic question, and verify that the public site never reveals secrets or offers unsupported payment claims.

## 15. Security and limitations

**Existing protections:** input validation, bounded amount fields, destination-specific account/routing format checks, short-lived signed transfer reviews, explicit sandbox approvals, protected deterministic rules, masked audit fields in transfer review, HMAC-linked audit history, optional guarded provider-hosted checkout, published source attribution, and production restrictions on shared history/audit listings.

**Important limitations:**

- Demo login is **not real authentication**. A password is accepted to create an in-memory session, not checked against a registered account. The session cookie is not configured for secure HTTPS-only usage in the supplied code.
- Saved recipient bank details are held in application memory during a demo; do not provide real account information. Restarting the server may erase them.
- No licensed cross-border payment connection, KYC, AML, sanctions screening, beneficiary identity verification, universal corridor eligibility verification or guaranteed bank settlement.
- Route cards contain fee assumptions and reference FX, **not** live institution quotations.
- The simplified on-screen comparison is separate from the detailed saved-plan stress-test workflow.
- Optional hosted card checkout is restricted and unavailable by default. Do not describe a configured payment gateway unless you have verified and are authorized to use it.
- The PDF reader cannot certify invoice authenticity or generally read image-only scans.
- Full per-user production authorization and durable multi-user account isolation require further engineering.
- Financial recommendations remain planning illustrations and should not replace checking the university's official invoice or the licensed provider's actual terms.

If you previously shared database passwords or API keys outside a trusted secrets manager, rotate them before any public deployment.

## 16. Presentation walkthrough

A short competition walkthrough can follow this sequence:

1. **Problem:** tuition payments involve conversion costs, deadlines, recipient details and living expenses.
2. **Home:** show the clear student-focused dashboard and six supported countries.
3. **My profile:** demonstrate a temporary sign-in and show where saved beneficiaries appear.
4. **Send money:** walk through entering a sample beneficiary, estimated FX review and explicit confirmation. State clearly that no funds move.
5. **Compare routes:** enter an amount and explain the indicative partner/bank/card cards and their assumptions.
6. **Journey Studio:** show tuition, scholarship and living-cost protection, then discuss invoice extraction and the calendar reminder.
7. **Bridge AI and Data sources:** explain how the assistant uses reference information rather than deciding payments on its own.
8. **Architecture and conclusion:** show separation of frontend, financial logic, data and optional external services, then emphasize safer planning and transparency.

Use fictional student names and fabricated example account details only. Avoid presenting illustrative data as proof of payment or provider acceptance.

## 17. Troubleshooting and useful links

| Problem | Likely cause | Suggested fix |
|---|---|---|
| Buttons do not work when opening an HTML file | FastAPI or JavaScript initialization is not running | Start `python run.py`, then visit the server URL |
| `DATABASE_URL is required` | `.env` missing or incorrect | Create `.env`, configure a working MySQL URL and rerun |
| MySQL authentication or SSL failure | Host, password, port or TLS settings incorrect | Check provider settings, CA certificate and `scripts/check_mysql.py` |
| Rate or route comparison unavailable | External reference FX service did not return usable data | Check internet access and reference currency pair; do not invent a rate |
| Blank profile after restart | Profile/beneficiaries are in-memory demo data | Create a fresh demonstration session; use test details only |
| Public payment history returns 403 | Expected production restriction | Do not expose unauthenticated shared history publicly |
| Mermaid diagram has a parsing error on GitHub | Mermaid syntax contains unsupported separators or syntax | Replace the README with this corrected file and keep each complete diagram in its own fenced `mermaid` block |
| README images are missing on GitHub | `docs/screenshots` or `docs/diagrams` assets not uploaded | Upload the supplied documentation folders with the README |

**Reference links:** [GitHub repository](https://github.com/Takbir-Al-Tanim/StudentBridge-AI) · [Render](https://dashboard.render.com/) · [Aiven](https://console.aiven.io/) · [Frankfurter](https://www.frankfurter.app/) · [FastAPI](https://fastapi.tiangolo.com/) · [Mermaid diagrams](https://mermaid.js.org/intro/)

---

**StudentBridge AI** — one place to understand student finances, compare possible costs, and plan with clearer information.
