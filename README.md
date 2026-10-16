# StudentBridge AI

### Cross-Border & Student Finance Assistant

**A student-friendly finance planning platform for China, the United Kingdom, Japan, South Korea, Australia, and Bangladesh.**

StudentBridge AI helps international students understand the cost of studying abroad. It brings tuition planning, money-transfer estimates, credit-building guidance, multi-currency calculations, financial what-if scenarios, and source-linked explanations into one website.

It is built with **Python, FastAPI, MySQL, HTML, CSS, JavaScript, and an optional Gemini API connection**. The important financial calculations happen in Python, not inside the language model.

> [!IMPORTANT]
> **Project status: educational / competition prototype.** The platform can estimate and compare costs, store plans, create practice transactions and test receipts, and optionally connect an *authorized merchant* to a hosted card checkout. **It does not provide a licensed remittance service, independently verify bank offers, or automatically pay a university.** Do not submit real card details to StudentBridge forms.

**Repository:** [StudentBridge-AI on GitHub](https://github.com/Takbir-Al-Tanim/StudentBridge-AI)  
**Project track:** FinTechathon — Topic C: Cross-border & Student Finance Assistant  
**Document basis:** StudentBridge AI Topic C V7 code and accompanying project documentation (October 2026)

---

## Table of contents

1. [What problem does it solve?](#1-what-problem-does-it-solve)
2. [Main features](#2-main-features)
3. [Supported countries and currencies](#3-supported-countries-and-currencies)
4. [Screenshots](#4-screenshots)
5. [How the entire system works](#5-how-the-entire-system-works)
6. [Technical architecture and project files](#6-technical-architecture-and-project-files)
7. [Database architecture](#7-database-architecture)
8. [Requirements](#8-requirements)
9. [Run locally on macOS](#9-run-locally-on-macos)
10. [Run locally on Windows](#10-run-locally-on-windows)
11. [Run locally on Linux](#11-run-locally-on-linux)
12. [Optional: run MySQL using Docker](#12-optional-run-mysql-using-docker)
13. [Configuration and environment variables](#13-configuration-and-environment-variables)
14. [Connect to Aiven cloud MySQL](#14-connect-to-aiven-cloud-mysql)
15. [Deploy the public website on Render](#15-deploy-the-public-website-on-render)
16. [User guide: how to use each feature](#16-user-guide-how-to-use-each-feature)
17. [Important API endpoints](#17-important-api-endpoints)
18. [How the financial calculations work](#18-how-the-financial-calculations-work)
19. [Financial data and sources](#19-financial-data-and-sources)
20. [Security, privacy, and payment boundaries](#20-security-privacy-and-payment-boundaries)
21. [Testing and verification](#21-testing-and-verification)
22. [Common errors and solutions](#22-common-errors-and-solutions)
23. [Frequently asked questions](#23-frequently-asked-questions)
24. [Future improvements](#24-future-improvements)
25. [Contributing and project documentation](#25-contributing-and-project-documentation)

---

## 1. What problem does it solve?

Studying in another country can involve many financial decisions. Students may need to pay tuition in a different currency, estimate transfer costs, keep enough emergency savings, understand living expenses, and learn how credit works in a new country.

These questions are usually handled in separate places. A currency converter may not include bank fees. A university invoice may not clearly show the whole study budget. A general chatbot may give an answer without identifying its data source.

**StudentBridge AI brings these questions into one guided workflow.** Students can:

- Estimate the amount received when sending money from one supported country to another.
- Plan tuition expenses and compare *user-provided* provider quotes by cost and estimated arrival time.
- See whether a planned payment could leave too little money for emergency needs.
- Explore what would happen if exchange rates or living costs changed.
- Learn general steps for building credit in a destination country.
- Add balances from different currencies and estimate their total in a selected currency.
- Understand why the platform produced a recommendation and which figures need independent checking.

The goal is **better financial understanding and safer planning**, not replacing banks, universities, regulated advisers, or licensed payment companies.

---

## 2. Main features

| Feature | What the student does | What the system provides | Important limitation |
|---|---|---|---|
| **Send Money Abroad** | Select two countries, enter an amount, optional fee and exchange markup | An estimated transfer value using a dated reference exchange rate, when available | No transfer is sent; bank rate and eligibility are not confirmed |
| **Tuition Payments** | Review tuition needs, invoice details, and available payment choices | Tuition planning, cost comparisons, a guided practice-payment workflow and receipt | Practice payments do not settle tuition; hosted card checkout needs authorized merchant configuration |
| **Build Credit Abroad** | Select the destination country and follow a preparation checklist | Country-specific educational guidance and linked source information | No credit score, credit bureau connection, loan offer or eligibility decision |
| **My Currencies** | Enter balances in CNY, GBP, JPY, KRW, AUD and BDT | An estimated total in a target currency with reference-rate dates | Not linked to bank accounts; balances entered here are not saved |
| **EduRoute Planner** | Enter tuition, scholarship, savings, emergency reserve, deadline and provider quotes | Conditional quote comparison, cost calculations, affordability checks and explanations | Quotes and provider eligibility are supplied by the user, not verified by the system |
| **Financial Digital Twin** | Try different exchange-rate, fee, or living-cost changes | A what-if result showing cost changes and possible reserve risk | Not a forecast of future market prices |
| **Decision Passport** | Open an already-created finance plan | A traceable summary: inputs, calculations, reasons, sources and limitations | The integrity hash is not an external financial certification |
| **AI Finance Assistant** | Ask questions in easy language | Source-aware responses, suggested next actions and financial tool results | Gemini is optional and only supplements grounded results |
| **Invoice Reader** | Upload a supported PDF invoice | Candidate amounts and dates extracted from selectable PDF text | It cannot certify an invoice or reliably read scanned PDFs without OCR |
| **Practice Payment & Audit** | Review and explicitly approve a simulated option | A test transaction, practice receipt, and recorded audit event | No bank is contacted and no real money moves |

### Why this design matters

The **language model explains** financial information. **Python calculates** the amounts. **MySQL stores** records that need saving. **The student remains responsible** for confirming provider details and any actual payment.

---

## 3. Supported countries and currencies

| Country | Currency name | Code |
|---|---|---|
| China | Chinese yuan | `CNY` |
| United Kingdom | Pound sterling | `GBP` |
| Japan | Japanese yen | `JPY` |
| South Korea | South Korean won | `KRW` |
| Australia | Australian dollar | `AUD` |
| Bangladesh | Bangladeshi taka | `BDT` |

There are **six origin countries** and **five different destination countries** for each origin, giving **30 directional planning combinations** (`6 × 5 = 30`). For example, Japan → United Kingdom and United Kingdom → Japan are different planning directions.

> **30 planning combinations do not mean 30 verified banking routes.** A financial provider may not offer a particular corridor, transfer type, or payment method. Confirm availability directly with the provider.

---

## 4. Screenshots

These images are included in the full V7 project package. They will appear on GitHub when the `docs/` folder is uploaded with the repository.

### Home page

![StudentBridge AI Topic C homepage](docs/topicc_home.png)

### Send Money Abroad

![StudentBridge AI transfer estimation screen](docs/topicc_remittance.png)

### My Currencies

![StudentBridge AI multi-currency overview](docs/topicc_currencies.png)

Other UI images are available in `docs/previews/`.

---

## 5. How the entire system works

### 5.1 High-level system architecture

```mermaid
flowchart TD
    U["Student using a phone or laptop"] --> WEB["StudentBridge AI website<br/>HTML + CSS + JavaScript"]
    WEB --> API["FastAPI backend<br/>Python + Pydantic validation"]
    API --> FIN["Financial rules and calculations<br/>EduRoute + Digital Twin"]
    API --> CHAT["Source-aware assistant"]
    API --> PDF["PDF invoice analysis"]
    API --> DB[("MySQL database<br/>Plans, research, test transactions, audit")]
    API --> FX["Frankfurter reference FX API"]
    CHAT -. "optional rewriting" .-> GEM["Gemini API"]
    API -. "only if correctly configured and authorized" .-> CARD["Stripe-hosted card checkout"]
    FIN --> API
    DB --> API
    FX --> API
    API --> WEB

    classDef core fill:#e8f1ff,stroke:#3b67a1,color:#183153
    classDef storage fill:#e8f5e9,stroke:#47835a,color:#193b26
    class API,FIN,CHAT core
    class DB storage
```

**In simple words:** The student enters information in the website. The website sends it to FastAPI. Python validates the input, applies financial calculations, and reads or saves information in MySQL. The result returns to the website. For reference exchange rates, the backend may also ask an external FX API. Gemini is optional; it is not trusted to make payment decisions.

### 5.2 Example: planning a tuition payment

```mermaid
flowchart TD
    A["Enter countries, tuition, savings, and deadline"] --> B["Check inputs and currencies"]
    B --> C["Add provider quotes or request reference FX"]
    C --> D["Calculate cost, fees, and remaining balance"]
    D --> E{"Quote meets the entered<br/>eligibility, funds, and deadline?"}
    E -- "Yes" --> F["Compare qualifying quotes by cost"]
    E -- "No" --> G["Show why the option does not qualify"]
    F --> H["Create plan and Decision Passport"]
    G --> H
    H --> I["Try Digital Twin what-if scenarios"]
    I --> J["Optional explicit approval of a practice transaction"]
    J --> K["Store test receipt and audit record"]
```

The system must be able to say **“no suitable quote was entered”** rather than invent a provider, a fee, or a transfer guarantee.

### 5.3 Deployment architecture

```mermaid
flowchart LR
    DEV["Developer's laptop"] --> GH["GitHub repository<br/>source code only"]
    GH --> R["Render Web Service<br/>FastAPI + frontend"]
    VIS["Competition judges / visitors"] -->|"HTTPS"| R
    R -->|"TLS MySQL connection"| A[("Aiven MySQL")]
    R -->|"optional HTTPS request"| G["Gemini API"]
    R -->|"reference FX request"| F["Frankfurter API"]
    R -. "optional authorized checkout" .-> S["Stripe"]
```

**GitHub is where the code lives. Render runs the application. Aiven stores the database.** Netlify is not needed for the current single FastAPI application.

---

## 6. Technical architecture and project files

### 6.1 Technology stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | HTML, CSS, JavaScript, Jinja2 | Website screens, forms, dashboards, charts and navigation |
| Backend | Python 3.11+, FastAPI, Uvicorn | APIs, request handling and application startup |
| Input validation | Pydantic | Rejects invalid data before calculations |
| Finance engine | Python `Decimal` calculations | More controlled fee and budget arithmetic |
| Database | MySQL / compatible MariaDB, SQLAlchemy, PyMySQL | Stores plans, research, test transactions and audit events |
| AI explanations | Source-aware rules, optional Gemini API | Understandable financial explanations and next-step guidance |
| Exchange-rate reference | Frankfurter API | Published reference exchange rates, with observation dates |
| Invoice processing | PyMuPDF | Reads selectable text from PDF invoices |
| Optional hosted checkout | Stripe | Provider-hosted card details and payment confirmation, when authorized |
| Tests | Pytest and FastAPI test client | Automated API and logic checks |

### 6.2 Folder structure

```text
StudentBridge_AI_MySQL/
├── app/
│   ├── main.py                  # FastAPI website and API routes
│   ├── database.py              # MySQL tables, queries, imports, audit
│   ├── logic.py                 # EduRoute and Digital Twin calculations
│   ├── assistant.py             # Source-aware finance assistant
│   ├── secure_card.py           # Optional provider-hosted card checkout
│   ├── data/
│   │   ├── catalog.json         # Country and feature reference catalog
│   │   ├── sources.json         # Linked research source registry
│   │   └── research_summary.json
│   ├── templates/
│   │   └── index.html           # Main website page
│   └── static/
│       ├── app.js               # Frontend interactions
│       └── styles.css           # Design and responsive layout
├── data/
│   └── research/
│       ├── corrected/           # CSV data imported into MySQL
│       ├── uploaded_originals/  # Original research inputs
│       └── legacy_archive/      # Historical material
├── docs/                       # Design, guides, security, screenshots
├── scripts/
│   ├── setup_mysql.py           # Initialize tables and research data
│   ├── check_mysql.py           # Test actual MySQL connectivity
│   ├── smoke_test_mysql.py      # Write/read check for a test database
│   ├── seed_sandbox.py          # Optional fictional test transactions
│   └── mysql_schema.sql        # Reference SQL schema
├── tests/                      # Automated tests
├── evidence/                   # Saved example evidence files
├── certs/                      # Optional downloaded public CA certificate
│   └── ca.pem
├── .env.example                 # Sample settings without real secrets
├── .env                         # Your private settings; do NOT upload
├── .gitignore
├── docker-compose.yml           # Optional MySQL Docker service
├── requirements.txt            # Python dependencies
├── run.py                      # Local server launcher
└── README.md                   # This guide
```

The `certs/` directory and `.env` file are created by the developer if needed; they are not required to be present in every downloaded copy of the project.

### 6.3 What the main Python files do

- `app/main.py`: defines the endpoints, checks input fields, serves the homepage and runs application startup.
- `app/logic.py`: performs tuition, fee, savings and what-if calculations. It does not depend on Gemini.
- `app/database.py`: connects to MySQL, creates tables if missing, saves plans and records audit events.
- `app/assistant.py`: selects grounded explanations using country and plan information.
- `app/secure_card.py`: handles the optional hosted-checkout configuration and provider calls.
- `run.py`: starts the local website at `http://127.0.0.1:8000`.

---

## 7. Database architecture

The current code defines **11 tables: 5 operational/audit tables and 6 research tables**. Some older project notes mention ten tables; the V7 code also contains the `provider_events` table for optional checkout webhooks.

### 7.1 Database relationships

```mermaid
erDiagram
    PLANS ||--o{ TRANSACTIONS : "plan_id"
    COUNTRIES ||--o{ FINANCIAL_BENCHMARKS : "country_code"
    COUNTRIES ||--o{ TUITION_BENCHMARKS : "country_code"
    COUNTRIES ||--o{ PAYMENT_QUOTES : "origin/destination"
    SOURCES ||--o{ FINANCIAL_BENCHMARKS : "source_id"
    SOURCES ||--o{ TUITION_BENCHMARKS : "source_id"
    SOURCES ||--o{ FX_RATES : "source_id"

    PLANS {
        string id PK
        string created_at
        text payload_json
        text result_json
        string decision_hash
    }
    TRANSACTIONS {
        string id PK
        string plan_id FK
        string status
        string idempotency_key UK
    }
    AUDIT {
        int id PK
        string previous_hash
        string event_hash
    }
    AUDIT_CHAIN_STATE {
        int state_id PK
        string last_hash
    }
    PROVIDER_EVENTS {
        string event_id PK
        string session_id
        string payment_status
    }
    COUNTRIES {
        string country_code PK
        string country_name
        string currency_code
    }
    SOURCES {
        int source_id PK
        string publisher
        string source_url
    }
    FINANCIAL_BENCHMARKS {
        int benchmark_id PK
        string country_code FK
        int source_id FK
    }
    TUITION_BENCHMARKS {
        int tuition_id PK
        string country_code FK
        int source_id FK
    }
    FX_RATES {
        int fx_id PK
        int source_id FK
        decimal rate
    }
    PAYMENT_QUOTES {
        int quote_id PK
        string origin_country_code FK
        string destination_country_code FK
    }
```

**Reading this diagram:** A plan may have multiple practice transactions. Research entries refer to countries and, when available, their original sources. The audit and provider-event tables are separate operational logs; they should not be mistaken for records of actual bank settlement.

### 7.2 What is saved?

| Information | Where it lives |
|---|---|
| Saved finance plan inputs/results | `plans` table |
| Practice-payment history | `transactions` table |
| Audit events and audit-chain head | `audit`, `audit_chain_state` tables |
| Optional hosted-checkout event references | `provider_events` table |
| Research country/financial/tuition/rate information | Six research tables |
| Static information and source catalog | `app/data/*.json` |
| Entered multi-currency balances | Browser while in use; **not saved** in MySQL |
| Raw card number or CVC | **Not collected or stored by StudentBridge** |

The app creates missing tables at startup. If the database contains no country research rows, startup imports the bundled corrected CSVs. You can also run `python scripts/setup_mysql.py` manually. Neither action should be used as a substitute for database backups.

---

## 8. Requirements

### 8.1 Minimum software

- A laptop or desktop with Windows, macOS, or Linux.
- **Python 3.11** recommended for reproducing the tested development environment.
- A terminal: Terminal on macOS/Linux or PowerShell on Windows.
- MySQL 8.x, a compatible local MariaDB/XAMPP service, Docker MySQL, **or** a managed MySQL database such as Aiven.
- An internet connection to install Python packages and use live reference FX or the optional Gemini service.
- A browser such as Chrome, Firefox, Safari, or Edge.

### 8.2 Helpful but optional tools

- Git and a GitHub account for sharing or deployment.
- VS Code for editing files.
- Docker Desktop to start a local MySQL instance.
- A Gemini API key for supplementary AI explanations. **The basic financial rules work without this key.**
- A CA certificate for a managed MySQL server that requires TLS verification.

### 8.3 Check Python and Git

**macOS / Linux:**

```bash
python3 --version
git --version
```

**Windows PowerShell:**

```powershell
py --version
git --version
```

If Python is missing, download it from [python.org](https://www.python.org/downloads/). If Git is missing, download it from [git-scm.com](https://git-scm.com/downloads).

---

## 9. Run locally on macOS

This section is for someone who wants to run the website on their own MacBook. You can use **local XAMPP MySQL** or an already-created **Aiven MySQL** database; choose one, not both.

### Step 1 — Download the source code

If GitHub already contains the project:

```bash
git clone https://github.com/Takbir-Al-Tanim/StudentBridge-AI.git
cd StudentBridge-AI
```

Alternatively, download the project ZIP, extract it, open Terminal inside the extracted folder, and confirm you can see `requirements.txt` and `run.py`.

For the original development folder with spaces in its name, use quotes around the path, for example:

```bash
cd "/path/to/StudentBridge_AI_MySQL 5"
```

### Step 2 — Create and activate a Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The `.venv` folder keeps this project's libraries separate from other Python projects.

### Step 3 — Set up MySQL

**Option A: XAMPP (local development)**

1. Open XAMPP and start **MySQL**.
2. Open phpMyAdmin or a MySQL client.
3. Create a database named `studentbridge_ai` if it does not exist.
4. Prefer a dedicated MySQL user with permission to work on this database. Some local XAMPP installations use `root` without a password; that is suitable only for isolated local development, not a public server.

Example SQL for creating the database:

```sql
CREATE DATABASE IF NOT EXISTS studentbridge_ai
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Option B: Aiven (cloud MySQL)** — If you already have Aiven, skip starting XAMPP. Follow [Section 14](#14-connect-to-aiven-cloud-mysql) and use your Aiven `DATABASE_URL` instead.

### Step 4 — Create your private `.env` file

```bash
cp .env.example .env
```

For a local, password-protected MySQL server, edit the new `.env` with a code editor or:

```bash
nano .env
```

Example **only** (replace the placeholder locally):

```dotenv
DATABASE_URL=mysql+pymysql://studentbridge_app:YOUR_LOCAL_PASSWORD@127.0.0.1:3306/studentbridge_ai?charset=utf8mb4
APP_ENV=development
APP_SECRET=YOUR_UNIQUE_RANDOM_SECRET_AT_LEAST_32_CHARACTERS
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash
CARD_LIVE_ENABLED=false
MERCHANT_AUTHORIZED_TO_COLLECT=false
```

Generate a new `APP_SECRET` using:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(48))"
```

Do not place a real password, API key or secret in GitHub, a README, screenshots, or a public issue. If you use existing audit records, **keep the original `APP_SECRET`** or verification of those old records will fail.

### Step 5 — Create the application tables and import research data

```bash
python scripts/setup_mysql.py
```

This is normally needed only for a new database or to refresh the corrected research rows. It does not delete old plans or practice transactions.

### Step 6 — Check the database connection

```bash
python scripts/check_mysql.py
```

A successful run begins with output similar to:

```text
Connected: mysql
Tables: [...]
Research counts: {...}
Audit check: {'valid': True, ...}
```

The exact research row counts depend on the imported dataset. If you changed `APP_SECRET` while reusing existing audit data, the audit verification may report `valid: False`.

### Step 7 — Start the website

```bash
python run.py
```

Open **http://127.0.0.1:8000** in your browser. For the V7 interface, you can also open **http://127.0.0.1:8000/?v=7**.

To stop the server, press **Ctrl + C** in Terminal. To run it again later, return to the project folder, activate `.venv`, and run `python run.py`.

---

## 10. Run locally on Windows

### Step 1 — Get the code

Clone the repository in PowerShell:

```powershell
git clone https://github.com/Takbir-Al-Tanim/StudentBridge-AI.git
cd StudentBridge-AI
```

Or download and extract the ZIP, then open PowerShell inside that folder.

### Step 2 — Create a virtual environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If `py -3.11` is unavailable but a compatible version of Python is installed, use `py -m venv .venv`.

If PowerShell blocks the activation script, you can avoid changing any system security settings by running the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Use `.\.venv\Scripts\python.exe` instead of `python` in the later commands if you choose this option.

### Step 3 — Install or connect to MySQL

Start MySQL using XAMPP, MySQL Community Server, or Docker. Create the database `studentbridge_ai`, or choose a cloud MySQL database that is already running.

### Step 4 — Configure the environment

```powershell
Copy-Item .env.example .env
notepad .env
```

Enter the `DATABASE_URL`, `APP_SECRET`, and optional Gemini settings described in [Section 13](#13-configuration-and-environment-variables). Never publish the file.

### Step 5 — Prepare, check, and run

```powershell
python scripts/setup_mysql.py
python scripts/check_mysql.py
python run.py
```

Open **http://127.0.0.1:8000**. Stop the server with **Ctrl + C**.

---

## 11. Run locally on Linux

Install Python 3.11 or a compatible recent Python 3 release with virtual-environment support, Git, and MySQL (or use Aiven). Package-install commands vary by Linux distribution.

```bash
git clone https://github.com/Takbir-Al-Tanim/StudentBridge-AI.git
cd StudentBridge-AI
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Configure `.env`, start or connect to MySQL, then run:

```bash
python scripts/setup_mysql.py
python scripts/check_mysql.py
python run.py
```

Open **http://127.0.0.1:8000** in a browser on the same machine.

> The local `run.py` listens on `127.0.0.1`, so only the computer running the server can normally open it. For a public website use a proper web host such as Render rather than opening the development server directly to the internet.

---

## 12. Optional: run MySQL using Docker

The project includes `docker-compose.yml` for a local MySQL **8.4** service. This runs the database in Docker; the FastAPI application still runs in your Python environment.

1. Install Docker Desktop or Docker Engine with Compose.
2. Create a private `.env` file in the project root.
3. Add the following settings **with real private values only in your local file**:

```dotenv
MYSQL_ROOT_PASSWORD=YOUR_PRIVATE_ROOT_PASSWORD
MYSQL_APP_PASSWORD=YOUR_PRIVATE_APP_PASSWORD
DATABASE_URL=mysql+pymysql://studentbridge_app:YOUR_PRIVATE_APP_PASSWORD@127.0.0.1:3306/studentbridge_ai?charset=utf8mb4
APP_ENV=development
APP_SECRET=YOUR_RANDOM_SECRET_AT_LEAST_32_CHARACTERS
```

4. Start the Docker database:

```bash
docker compose up -d mysql
```

5. Wait until MySQL reports healthy and then run:

```bash
python scripts/setup_mysql.py
python scripts/check_mysql.py
python run.py
```

Stop the Docker database using `docker compose stop mysql`. The Compose volume keeps stored data when the container is stopped. **Do not run `docker compose down -v` unless you intentionally want to delete that database volume.**

If local XAMPP/MySQL is already using port `3306`, stop that service first or change the Docker port mapping.

---

## 13. Configuration and environment variables

StudentBridge reads environment variables from `.env` when running locally. On Render, enter them in the **Environment** settings rather than uploading a `.env` file.

| Variable | Required? | Meaning |
|---|---|---|
| `DATABASE_URL` | **Yes** | SQLAlchemy/MySQL connection URL |
| `APP_ENV` | Yes for clear deployment behavior | `development` locally or `production` on a hosted site |
| `APP_SECRET` | **Yes for safe deployment** | Secret used to sign records and verify the audit chain; use at least 32 random characters in production |
| `GEMINI_API_KEY` | No | Enables an optional text explanation from Gemini |
| `GEMINI_MODEL` | No | Gemini model name, e.g. `gemini-2.5-flash` |
| `CARD_LIVE_ENABLED` | Recommended | Keep `false` for this prototype |
| `MERCHANT_AUTHORIZED_TO_COLLECT` | Recommended | Keep `false` unless legally and technically authorized |
| `STRIPE_SECRET_KEY` | No | Optional provider secret; leave blank unless an eligible merchant is configuring checkout |
| `STRIPE_PRICE_ID` | No | Provider-created fixed-price item for an authorized invoice |
| `STRIPE_WEBHOOK_SECRET` | No | Provider's webhook-signing secret |
| `AUTHORIZED_PAYEE_NAME` | No | Verified person/organization that is permitted to receive that charge |
| `AUTHORIZED_INVOICE_REFERENCE` | No | Reference for the authorized invoice |
| `PUBLIC_BASE_URL` | Needed for hosted card checkout | Public HTTPS address used for provider return URLs |
| `MYSQL_ROOT_PASSWORD` | Docker only | Password for the local Docker database administrator |
| `MYSQL_APP_PASSWORD` | Docker only | Password for Docker's application database user |

### Safe example `.env`

```dotenv
# Use ONLY private values in your real .env file.
DATABASE_URL=mysql+pymysql://YOUR_USER:YOUR_URL_ENCODED_PASSWORD@YOUR_DATABASE_HOST:3306/studentbridge_ai?charset=utf8mb4
APP_ENV=development
APP_SECRET=REPLACE_WITH_NEW_RANDOM_SECRET_AT_LEAST_32_CHARACTERS
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash
STRIPE_SECRET_KEY=
STRIPE_PRICE_ID=
STRIPE_WEBHOOK_SECRET=
AUTHORIZED_PAYEE_NAME=
AUTHORIZED_INVOICE_REFERENCE=
PUBLIC_BASE_URL=http://127.0.0.1:8000
CARD_LIVE_ENABLED=false
MERCHANT_AUTHORIZED_TO_COLLECT=false
```

### Passwords with symbols

Special characters in a password must be URL-encoded when placed inside `DATABASE_URL`. For example, an `@` inside the password becomes `%40` and a `#` becomes `%23`. A convenient *private* method is to URL-encode the password locally using `urllib.parse.quote`; do not paste the original or encoded password into online chat or GitHub.

### Protect `.env`

Add these patterns to `.gitignore` before the first commit:

```gitignore
.env
.env.*
!.env.example
.venv/
__pycache__/
.pytest_cache/
*.pyc
*.log
*.sqlite3
.DS_Store
*.key
*.p12
```

The tracked `.env.example` must contain **placeholders only**. If a secret was already committed, simply adding `.gitignore` is not enough to remove it from Git history: revoke/rotate the exposed credential and clean the affected commit history before sharing the repository.

---

## 14. Connect to Aiven cloud MySQL

Aiven can host the database while the website runs on your laptop or Render. **Aiven is the database service, not the website host.**

### Step 1 — Create an Aiven MySQL service

1. Sign in to [Aiven Console](https://console.aiven.io/).
2. Select your project and create a MySQL service using an available plan.
3. Give the service a simple name, such as `studentbridge-ai` (service names use hyphens rather than underscores).
4. Wait for the service to become ready.

### Step 2 — Choose the database

Aiven may provide `defaultdb` automatically. You can use `defaultdb` or create `studentbridge_ai` under **Connect → Databases**. **The database name in `DATABASE_URL` must match the actual database you chose.**

### Step 3 — Download the public CA certificate

In Aiven, open the MySQL service's **Overview** / connection information page and download the **CA certificate**. Save it inside your project as `certs/ca.pem`.

**macOS / Linux:**

```bash
mkdir -p certs
cp "/path/to/downloaded/ca.pem" certs/ca.pem
```

**Windows PowerShell:**

```powershell
New-Item -ItemType Directory -Force certs
Copy-Item "C:\path\to\downloaded\ca.pem" "certs\ca.pem"
```

The CA certificate is a *public trust certificate*; it is different from a private key. If you commit `certs/ca.pem` to GitHub for deployment, inspect it first to make sure it contains only the expected CA certificate and **not** a private key or client credential.

### Step 4 — Set the Aiven connection URL

Use your own host, port, database, and password. **This is a format example, not a usable password:**

```dotenv
DATABASE_URL=mysql+pymysql://avnadmin:YOUR_URL_ENCODED_PASSWORD@YOUR_AIVEN_HOST:YOUR_AIVEN_PORT/defaultdb?charset=utf8mb4&ssl_ca=certs/ca.pem
```

If you created a separate database, replace `defaultdb` with `studentbridge_ai`. In the current code, `ssl_ca=certs/ca.pem` is passed to the MySQL driver so it can verify the server's certificate. The certificate path must exist in the environment where the application runs.

### Step 5 — Initialize and test

With your Python environment active:

```bash
python scripts/setup_mysql.py
python scripts/check_mysql.py
```

Then start the website with `python run.py` and confirm that `http://127.0.0.1:8000/api/health` reports an available MySQL connection.

> A newly created Aiven service is a separate database. It does **not** automatically contain your old local XAMPP plans or practice transactions. The setup script creates tables and imports packaged research rows; transferring old application records would require a separate, carefully planned database migration.

---

## 15. Deploy the public website on Render

**Recommended deployment: GitHub + Render Web Service + Aiven MySQL.** The complete website is served by FastAPI, so no separate Netlify frontend is required.

### Step 1 — Make sure the local project works

Run `python scripts/check_mysql.py` and `python run.py` successfully before moving to Render. Confirm that the CA certificate path exists and the UI loads.

### Step 2 — Prepare GitHub safely

First check that `.env` and other private files are ignored. Also inspect staged files for hard-coded keys before the first push:

```bash
git init
git add .
git status
git diff --cached --name-only
git grep --cached -l -I -E 'AVNS_|AQ[.]|sk_live_|mysql[+]pymysql://avnadmin:' || true
```

If the final command lists files containing actual credentials, remove the credentials from those files **before** committing. Never post those values in issues or screenshots.

Then, in your existing repository:

```bash
git commit -m "Document and publish StudentBridge AI"
git branch -M main
git remote add origin https://github.com/Takbir-Al-Tanim/StudentBridge-AI.git
git push -u origin main
```

If you already initialized Git, committed, or configured `origin`, do **not** run the corresponding step again. Instead use `git status`, `git remote -v`, and, after new changes, `git add .`, `git commit -m "Update documentation"`, and `git push`.

### Step 3 — Create the Render service

1. Open [Render Dashboard](https://dashboard.render.com/).
2. Choose **New → Web Service**.
3. Connect GitHub and select the `StudentBridge-AI` repository.
4. Select a Python runtime and an available plan suitable for testing.
5. Use the settings below.

| Render field | Value |
|---|---|
| **Name** | `studentbridge-ai` (or another available name) |
| **Repository** | `Takbir-Al-Tanim/StudentBridge-AI` |
| **Branch** | `main` |
| **Root directory** | Repository root; normally leave blank |
| **Build command** | `pip install -r requirements.txt` |
| **Start command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Health check path** | `/api/health` |
| **Python version** | Prefer a version compatible with Python 3.11 and installed dependencies |

**Why not `python run.py` on Render?** `run.py` is designed for local use and listens on the fixed local address `127.0.0.1:8000`. Render needs the application to listen on `0.0.0.0` and use the port that Render provides.

### Step 4 — Add Render environment variables

In **Render → Environment**, enter your **private** configuration values using the interface. Do not copy your local `.env` into GitHub.

```text
DATABASE_URL         = <your real Aiven MySQL URL, including ssl_ca=certs/ca.pem>
APP_ENV              = production
APP_SECRET           = <your private strong secret>
GEMINI_API_KEY       = <your private API key, or leave unset>
GEMINI_MODEL         = gemini-2.5-flash
CARD_LIVE_ENABLED    = false
MERCHANT_AUTHORIZED_TO_COLLECT = false
PUBLIC_BASE_URL      = https://<your-render-domain>
```

If card checkout is **not** configured, `PUBLIC_BASE_URL` is only preparatory. Keep all live card-payment settings disabled. Confirm `certs/ca.pem` is present in the committed project and available to the running server.

### Step 5 — Deploy and test

Click **Create Web Service** / **Deploy** and follow the build logs.

Open the HTTPS URL given by Render. Check:

1. Homepage loads and all navigation buttons are visible.
2. `/api/health` reports `status: ok` and `database_engine: mysql`.
3. Send Money retrieves a dated reference rate when the provider is available.
4. Tuition Planner accepts sample inputs and handles missing quotes honestly.
5. My Currencies does not invent a conversion when a rate is unavailable.
6. Credit guidance and AI assistant show expected content.
7. Test transactions, if used, are clearly marked as simulated.

**Free hosting:** Availability, sleep behavior, quotas, and plan limits can change. Free web services may take time to wake up. Check the provider's current plan details and keep backups of the database.

### Step 6 — Public-deployment safety warning

The present project **does not have user accounts, sign-in, role permissions, or per-user data isolation**. Some stored plans, test history, and audit endpoints are accessible without authentication. Therefore, **only publish it as a restricted-risk competition demonstration using fictional/non-sensitive information**. Do not invite students to upload real invoices or personal financial information. Before production use, add authentication, authorization, data protection, rate limits, abuse prevention, and an independent security review.

---

## 16. User guide: how to use each feature

### A. Send Money Abroad

1. Open **Send Money**.
2. Choose the **sending country** and **receiving country**.
3. Enter a sending amount.
4. If you know a bank's fixed fee or markup, you can enter it; otherwise treat the result as a rough estimate.
5. Click the calculation button.
6. Read the converted amount, the source and date of the reference FX rate, and the warnings.

**Example question:** “Approximately how much AUD could 10,000 CNY represent before actual provider costs?”

**Remember:** A published reference exchange rate is not the rate at which a bank promises to send money.

### B. Tuition Payments and EduRoute Planner

1. Open **Tuition Payments** or **Compare Payment Routes**.
2. Select where money is coming from and where the university is located.
3. Enter tuition, scholarship, current savings and the protected emergency reserve.
4. Add the tuition deadline and, if relevant, living expenses.
5. If you have provider quotes, enter their rate, charges, estimated transfer time, expiry and original link.
6. Ask the planner to compare the choices.
7. Read the result and the reasons why an option qualifies or fails.

The plan is only as dependable as the information entered. The app **does not independently verify user-entered provider quotes or legal route eligibility**.

### C. Build Credit Abroad

1. Open **Build Credit**.
2. Select the destination country.
3. Read the country-specific general guidance.
4. Work through the four-item readiness checklist.
5. Open the linked original sources before acting.

This is educational guidance. The platform does not check an actual credit file or promise approval of a credit product.

### D. My Currencies

1. Open **My Currencies**.
2. Enter any balances you wish to estimate across the six supported currencies.
3. Select the currency in which you want to see the total.
4. Calculate the total.
5. Check the dates and missing-rate messages.

These are manually entered balances, not bank-connected account balances. The current V7 UI does not save them to MySQL.

### E. Financial Digital Twin

After creating a suitable plan:

1. Open **Financial Digital Twin**.
2. Choose an imagined exchange-rate change, such as +5%.
3. Optionally add an extra fee or a living-cost percentage change.
4. Review the new estimated cost and the emergency-reserve check.

The result answers a **“what if?”** question. It is not a market prediction.

### F. Decision Passport

Open a saved plan's Decision Passport to see the planning goal, quote-level calculations, reasons for an outcome, the reference-rate classification, and cautions. A local SHA-256 hash helps identify a change to a saved deterministic result; it is not a legally certified transaction proof.

### G. Invoice Reader

Upload a PDF invoice through the relevant section. The server accepts up to **2.5 MB and 12 pages** and extracts possible amounts and dates from selectable text. Confirm all extracted values against the university's official invoice. Scanned PDFs without selectable text may need OCR, which is not supplied by this endpoint.

### H. AI Finance Assistant

Ask ordinary questions such as:

- “What can StudentBridge AI do?”
- “Explain how university tuition planning works.”
- “How can a student start building credit in Australia?”
- “How would a 5% exchange-rate rise affect my saved tuition plan?”
- “What is the reference exchange rate between GBP and AUD?”

Source-aware rules and financial tools provide the main answers. If configured, Gemini can add a clearer explanation but does not authorize payments or replace the calculated result.

### I. Practice Payment and Receipt

Use the separate practice-payment flow with invented sample inputs. An explicit confirmation is required before a simulated transaction is written. A practice receipt and audit log are created. **The transaction does not pay a university or move any money.**

---

## 17. Important API endpoints

FastAPI automatically provides an interactive API reference at **`/docs`** and OpenAPI JSON at **`/openapi.json`**.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Main website |
| `GET` | `/api/health` | Service and MySQL connection check |
| `GET` | `/api/catalog` | Countries, source catalog and feature data |
| `GET` | `/api/research/summary` | Research-data summary |
| `GET` | `/api/research/benchmarks` | Research benchmarks, optionally by country |
| `GET` | `/api/fx?base=GBP&quote=AUD` | Published reference FX (when available) |
| `POST` | `/api/plans` | Create a tuition/payment plan |
| `GET` | `/api/plans/{plan_id}` | Retrieve a saved plan |
| `POST` | `/api/scenarios` | Run a Digital Twin what-if scenario |
| `GET` | `/api/passport/{plan_id}` | Retrieve an explainable plan passport |
| `POST` | `/api/demo/prepare` | Prepare synthetic practice payment options |
| `POST` | `/api/sandbox/execute` | Explicitly confirm and record a simulated transaction |
| `GET` | `/api/sandbox/receipt/{transaction_id}` | Practice receipt |
| `GET` | `/api/sandbox/history` | Saved simulated transactions |
| `GET` | `/api/audit` | Audit event list |
| `GET` | `/api/audit/verify` | Check HMAC audit-chain consistency |
| `GET` | `/api/credit/{country}` | Country credit guidance |
| `POST` | `/api/invoices/analyze` | Extract candidate values from a PDF |
| `POST` | `/api/chat` | Source-aware financial assistant |
| `GET` | `/api/card/availability` | Optional hosted checkout availability |
| `POST` | `/api/card/checkout` | Begin a configured provider-hosted checkout |
| `GET` | `/api/card/session/{session_id}` | Check provider session status |
| `POST` | `/api/card/webhook` | Receive signed provider webhook events |

### API example 1 — Health check

```bash
curl http://127.0.0.1:8000/api/health
```

Expected structure when MySQL is working:

```json
{
  "status": "ok",
  "version": "3.0.0",
  "mode": "SANDBOX_NO_REAL_MONEY",
  "database": true,
  "database_engine": "mysql"
}
```

### API example 2 — Reference exchange rate

```bash
curl "http://127.0.0.1:8000/api/fx?base=GBP&quote=AUD"
```

When the external reference service is available, this returns the published rate and observation date. When it is unavailable, it returns `available: false` rather than a guessed rate.

### API example 3 — Ask the assistant

```bash
curl -X POST "http://127.0.0.1:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"What can you do?"}'
```

### API example 4 — Create a plan *without* provider quotes

This demonstrates why the system should never invent a transfer provider:

```bash
curl -X POST "http://127.0.0.1:8000/api/plans" \
  -H "Content-Type: application/json" \
  -d '{
    "origin":"Japan",
    "destination":"United Kingdom",
    "origin_currency":"JPY",
    "destination_currency":"GBP",
    "university":"Example University",
    "tuition_amount":20000,
    "scholarship_amount":2000,
    "available_balance":6000000,
    "emergency_reserve":800000,
    "monthly_living_cost":1000,
    "living_months":6,
    "deadline":"2027-01-15",
    "quotes":[]
  }'
```

The response will have a saved plan ID, but **no recommended provider** because no actual provider quote was entered. These numbers and the university are fictional illustrations.

For full request schemas and required fields, open `http://127.0.0.1:8000/docs` while the app is running.

---

## 18. How the financial calculations work

### 18.1 Tuition amount after scholarship

```text
Required tuition = Tuition amount - Scholarship amount
```

For example, if tuition is 20,000 GBP and a confirmed scholarship covers 2,000 GBP:

```text
Required tuition = 20,000 - 2,000 = 18,000 GBP
```

The engine rejects a scholarship amount larger than the entered tuition amount for that payment.

### 18.2 Convert a provider quote and calculate fees

For a quote whose rate is expressed as **sending-currency units per one receiving-currency unit**:

```text
Base cost          = Required tuition × Provider quote rate
Percentage fee     = Base cost × (Fee percent / 100)
Total transfer fee = Percentage fee + Fixed fee
Overall cost       = Base cost + Total transfer fee
```

**Fictional calculation example:**

```text
Tuition to send:       1,000 GBP
Illustrative rate:       190 JPY per GBP
Illustrative fee:        0.5%
Illustrative fixed fee:  300 JPY

Base cost:          1,000 × 190 = 190,000 JPY
Percentage fee:    190,000 × 0.005 = 950 JPY
Total fees:        950 + 300 = 1,250 JPY
Overall cost:      191,250 JPY
```

**This is not a live JPY/GBP quotation.** The figures are invented only to explain the formula.

### 18.3 Emergency reserve and deadline checks

```text
Spendable money = Available balance - Protected emergency reserve
Affordable      = Overall cost <= Spendable money
Deadline passes = Estimated delivery days <= Days until deadline
```

The planner also checks the student's stated provider eligibility, any quote expiry, and whether the quote has evidence or is a clearly labeled practice option.

Among options that pass the checks, the engine generally chooses the lowest calculated cost, using estimated delivery time as a secondary comparison. **A user-checked eligibility box is not regulatory verification.**

### 18.4 Digital Twin what-if example

A student can try an imaginary 5% rise in the rate:

```text
New converted base cost = Original base cost × 1.05
```

The system recalculates applicable percentage fees, adds any extra cost, and tests whether the student's protected reserve is still covered. It does not claim the market will really rise by 5%.

### 18.5 Integrity and duplicate prevention

- A SHA-256 fingerprint is attached to the deterministic plan result.
- Audit events form a local **HMAC-SHA256 hash chain**.
- Sandbox transactions have a unique **idempotency key** to reduce duplicate execution records.
- MySQL transactions keep related sandbox records and audit events together.

These are useful technical safeguards, but do **not** turn the prototype into a regulated payment processor or prove that real money moved.

---

## 19. Financial data and sources

The project combines research records shipped with the source code and, where available, a live request to the Frankfurter reference-rate API.

### Data locations

- `data/research/corrected/`: country, sources, benchmark, tuition, FX and payment-quote CSVs used by the importer.
- `data/research/uploaded_originals/`: original research inputs kept for review.
- `app/data/catalog.json`: country and guidance catalog used in the interface.
- `app/data/sources.json`: clickable source entries used by the assistant and pages.
- `app/data/research_summary.json`: packaged research summary.

### Important data labels

| Type | Meaning |
|---|---|
| **Published reference FX** | A dated reference exchange rate; **not** the rate a transfer service must offer |
| **Historical benchmark** | A figure published for an earlier period; may be outdated |
| **User-entered quote** | Price/fee information entered by a student; not independently checked |
| **Illustrative practice quote** | Invented provider/fee/ETA used only to test workflow |
| **Missing/unverified** | The platform has insufficient evidence and should not fill the gap with an invented amount |

The source records include origin information and dates when available. Costs, migration rules, visa requirements, tuition schedules and payment restrictions can change. Check the original institution, authority or provider before relying on any amount.

The Frankfurter endpoint used by the backend follows this format:

`https://api.frankfurter.dev/v2/rate/GBP/AUD`

Internet access and external-service availability are necessary for live reference-rate requests. Gemini is not required for these calculations.

---

## 20. Security, privacy, and payment boundaries

### What is already implemented

- Input checks using Pydantic, including supported country/currency combinations.
- Validation of tuition, funds, reserve amounts and dates.
- Conditional quote comparison with clear reasons for rejected options.
- An explicit approval phrase for practice payment recording.
- Duplicate-prevention keys for practice transaction requests.
- Local HMAC audit-chain checks and database transactions.
- Limits on PDF size and page count; PDF content is treated as untrusted text.
- Provider-hosted card forms rather than collecting raw card details in the StudentBridge interface.
- Flags that disable real-money card collection by default.

### What must be added before use with real customers

- Login, user identities, sessions and per-user access rules.
- Permission separation between administrators and students.
- Privacy notices, lawful personal-data handling, deletion rules and encrypted storage.
- Rate limiting, monitoring, abuse prevention and file scanning.
- Strong secrets management and regular credential rotation.
- Verified payment beneficiaries, invoices and real provider quotation APIs.
- Merchant or payment-provider authorization and any applicable legal/regulatory review.
- KYC/AML/sanctions checks if a future product legally requires them.
- Proper reconciliation, refunds, dispute handling and production backups.
- Independent security review and penetration testing.

### Critical warning for public demonstrations

**There is currently no user authentication or per-user plan isolation.** Routes for saved plans, practice history and audit information should not hold real student personal or banking data. For a public competition site, use sample universities and fictional amounts, and avoid accepting real invoices. Consider adding access controls or disabling sensitive operational endpoints before inviting general visitors.

### Card payments: what is and is not supported

The optional card module is a starting point for **Stripe-hosted Checkout**. An approved merchant would configure a fixed-price item for an authorized invoice. If not configured, checkout is unavailable. Test mode is for Stripe test cards only.

Even a successfully charged card is **not automatically a tuition payment to a university or a cross-border remittance**. The merchant must be permitted to collect for the stated purpose and beneficiary, and all legal and technical checks must be completed. Keep these values `false` in a public prototype:

```dotenv
CARD_LIVE_ENABLED=false
MERCHANT_AUTHORIZED_TO_COLLECT=false
```

For more detail, read `docs/SECURITY_SELF_ASSESSMENT.md` and `docs/V6_SECURE_CARD_PAYMENTS.md`.

---

## 21. Testing and verification

### 21.1 Automated tests

From the project root, with your Python environment active:

```bash
python -m pytest -q
```

The V7 project package was prepared after **64 automated tests passed** in an isolated test environment, plus a browser interaction test with mocked FX responses. This historical result does **not** prove that a newly installed MySQL server, Gemini key, Stripe configuration, or current FX API is working. Run the tests again on your own machine.

The automated tests use disposable **SQLite only in special test mode**. The real application requires MySQL (or compatible local MariaDB). A passing unit test therefore does not replace a real database connection test.

### 21.2 Check your actual MySQL service

```bash
python scripts/check_mysql.py
```

Check the connected engine, table names, research counts, and audit verification result.

### 21.3 Optional write/read smoke test

**Run only on a separate disposable MySQL database containing no real or important records:**

**macOS / Linux:**

```bash
MYSQL_SMOKE_TEST=YES python scripts/smoke_test_mysql.py
```

**Windows PowerShell:**

```powershell
$env:MYSQL_SMOKE_TEST="YES"
python scripts/smoke_test_mysql.py
Remove-Item Env:MYSQL_SMOKE_TEST
```

This writes an example plan/transaction to test actual database behavior. Do not run it against your production database.

### 21.4 Optional practice evidence

```bash
python scripts/seed_sandbox.py
```

Run this only on a non-production database. It creates fictional example test transactions and saves an evidence file at `evidence/mysql_sandbox_example.json`.

### 21.5 Manual website checklist

- [ ] Homepage opens without missing styles or scripts.
- [ ] All six countries are available.
- [ ] A transfer estimate shows the source and date, or an honest unavailable message.
- [ ] Tuition planning handles valid and invalid input safely.
- [ ] A plan without quotes does not create a fictitious provider recommendation.
- [ ] A hypothetical Digital Twin scenario recalculates the cost correctly.
- [ ] The credit page shows general guidance and sources.
- [ ] The multi-currency page handles missing rates openly.
- [ ] The assistant works even when `GEMINI_API_KEY` is empty.
- [ ] The practice payment shows explicit warnings and does not charge money.
- [ ] `/api/health` responds successfully.
- [ ] `/api/audit/verify` reports a valid chain for a consistent test database and secret.

---

## 22. Common errors and solutions

| Problem | Likely reason | How to fix it |
|---|---|---|
| `ModuleNotFoundError: No module named 'sqlalchemy'` | Python packages were not installed into the active environment | Activate `.venv` and run `python -m pip install -r requirements.txt` |
| `Can't connect to MySQL server on 'YOUR_AIVEN_HOST'` | The example hostname was never replaced | Copy the real host from Aiven's connection page into the private `.env` |
| `Unknown database 'studentbridge_ai'` | That database does not exist, or Aiven only has `defaultdb` | Create `studentbridge_ai` or point the URL to the existing `defaultdb` |
| `Access denied for user` | Wrong database username/password/permissions | Check the private connection details and the user's access rights |
| Certificate file not found | `certs/ca.pem` is missing or path is different | Put the downloaded public CA file at that relative path in the app's working directory |
| SSL or certificate verification error | Wrong CA, hostname or TLS configuration | Re-download the correct certificate; verify Aiven host/port and TLS settings |
| Browser cannot open port 8000 | Server is not running or another process owns the port | Start `python run.py`; stop old servers or choose an available port with Uvicorn |
| Old version still appears | Browser cache or older server instance | Stop previous server and hard-refresh (Cmd/Ctrl + Shift + R) |
| `/api/health` returns 503 | MySQL connection failed | Run `python scripts/check_mysql.py`, inspect configuration and service status |
| `Audit check: valid: False` | `APP_SECRET` was changed or audit records differ | Restore the original secret for that database; investigate unexpected changes |
| Assistant does not return Gemini explanations | Key missing, expired, quota exceeded or service unavailable | Basic grounded answers still work; check the key privately and provider status |
| FX rate says unavailable | Reference service unavailable or network problem | Try later; never substitute a guessed rate |
| PDF has no extracted text | Invoice is a scanned image | Enter figures manually after verifying the official invoice; OCR is not built into this endpoint |
| Card checkout button is disabled | No approved merchant/invoice is configured | Keep it disabled for the public prototype; use the clearly labeled practice flow |
| Render deployment fails to start | Wrong command, missing library, missing env variable or failed database initialization | Inspect Render logs; verify build/start commands, database permissions and CA path |
| `fatal: remote origin already exists` | GitHub remote has already been configured | Run `git remote -v`; update the existing remote rather than adding a second one |
| `nothing to commit` | Git sees no new changes | Run `git status`; if already committed, proceed to `git push` |

**Do not post `.env`, database URLs containing passwords, API keys, private certificates or entire exception logs containing credentials.** Redact them before asking for help.

---

## 23. Frequently asked questions

**Q: Do I need Gemini to use StudentBridge AI?**  
No. The backend has source-aware explanations and Python financial tools. Gemini optionally adds a plain-English explanation. The core calculations and validation do not rely on it.

**Q: Is StudentBridge AI its own trained LLM?**  
No. The current project is a finance application with a source-aware assistant and optional Gemini integration. A self-hosted open model such as Qwen could be investigated later, but it is not part of this V7 implementation.

**Q: Can I run the website without internet?**  
The local pages and basic calculations can work once dependencies and the database are available. Live exchange-rate requests, Gemini answers and cloud database access require internet.

**Q: Do I need both Render and Netlify?**  
No. Render can serve the entire existing FastAPI application. Netlify is only useful if the frontend is split into a separate deployment in the future.

**Q: Do I need MySQL on every user's laptop?**  
No. A developer who runs a separate local copy needs access to a compatible database. People visiting the hosted Render website use its cloud backend and database; they do not install Python or MySQL.

**Q: What is the difference between an exchange-rate reference and a provider quote?**  
A reference rate is published market information. A provider quote includes terms such as markup, bank fees, delivery time, eligibility and expiry. They are not interchangeable.

**Q: Are 30 transfer corridors connected to real providers?**  
No. They are 30 selectable directional planning pairs across six countries. Provider availability must be verified independently.

**Q: Can StudentBridge pay real university fees?**  
Not as a general cross-border tuition settlement service. Its practice flow never moves money. Optional provider-hosted card checkout requires an authorized merchant and invoice; receiving a card charge does not itself pay a university.

**Q: Is it safe to make the GitHub repository public?**  
You can share the source code publicly **after** removing secrets, reviewing included data and licenses, and ensuring no credentials exist in Git history. A public source repository does not make the system safe for public handling of real student data.

**Q: Does the platform store card numbers?**  
No. When authorized hosted checkout is configured, card details are entered on the provider's own page, not in the StudentBridge application.

**Q: What if the financial data is old?**  
Use the original source link and publication/observation date. Do not treat historical rates, tuition values or visa figures as guaranteed current amounts.

---

## 24. Future improvements

The following are ideas for a later version, **not current features**:

1. Secure student accounts with login, roles and individual saved plans.
2. Verified quotes and route eligibility from approved banks or remittance partners.
3. More complete official university tuition and living-cost datasets, refreshed regularly.
4. Optional local open-weight AI model, evaluated against the existing assistant.
5. Better invoice scanning/OCR and university beneficiary verification.
6. Personal budgets saved securely with explicit user permission.
7. Regional compliance checks designed with qualified legal and payment-service professionals.
8. Stronger accessibility, translations and mobile usability testing.
9. Production-grade monitoring, rate limiting, backups, audit attestations and incident response.
10. Independent testing for mathematical correctness, security and source reliability.

---

## 25. Contributing and project documentation

### For people who want to understand or improve the code

1. Fork or clone the repository.
2. Create a local `.env` containing **your own private** credentials.
3. Use a separate MySQL test database, not a production database.
4. Start the application and run `python -m pytest -q`.
5. Make changes in a Git branch and explain the change in a pull request.
6. Do not submit private keys, personal student invoices, real card data or copyrighted datasets without permission.

### Additional project documents

| Document | What it explains |
|---|---|
| `docs/TOPIC_C_FOUR_FEATURES.md` | The four Topic C requirements and their limits |
| `docs/V7_START_HERE.md` | Short V7 startup guide |
| `docs/SYSTEM_DESIGN.md` | Detailed decision logic and technology design |
| `docs/MYSQL_SETUP.md` | Local MySQL, Docker, importing and integration tests |
| `docs/AI_ASSISTANT_GUIDE.md` | Grounded financial assistant behavior |
| `docs/V6_SECURE_CARD_PAYMENTS.md` | Optional provider-hosted card payments and restrictions |
| `docs/SECURITY_SELF_ASSESSMENT.md` | Risks, implemented safeguards and missing production controls |
| `docs/COMPETITION_ALIGNMENT.md` | How the project relates to the competition's Topic C |
| `docs/DATA_REVIEW_AND_UPDATE.md` | Reviewing and updating source-backed research figures |

### License and third-party material

This README does not grant a license by itself. The repository owner should choose and add an appropriate `LICENSE` file after reviewing ownership and all third-party assets, datasets, API conditions, and dependencies. Official data being publicly readable does not always mean it can be freely redistributed for every purpose.

### Useful links

- **Project:** https://github.com/Takbir-Al-Tanim/StudentBridge-AI
- **Python:** https://www.python.org/
- **FastAPI:** https://fastapi.tiangolo.com/
- **MySQL:** https://dev.mysql.com/doc/
- **Aiven:** https://aiven.io/
- **Render:** https://render.com/
- **Frankfurter:** https://frankfurter.dev/
- **Stripe documentation:** https://docs.stripe.com/

---

## Final summary

**StudentBridge AI is a cross-border student finance decision-support platform.** It combines four Topic C use cases—remittance estimation, tuition planning, credit-building education and multi-currency management—with transparent calculations, a Financial Digital Twin, an explainable Decision Passport, MySQL persistence and a grounded assistant.

To try it yourself: **clone the repository → install Python requirements → configure MySQL and a private `.env` → run the setup/check scripts → start `python run.py` → open `http://127.0.0.1:8000`.**

To publish a competition demonstration: **push only non-secret project files to GitHub → deploy FastAPI on Render → connect Aiven MySQL with TLS → test every feature using fictional financial data.**

> **Remember:** Financial estimates are not payment guarantees. Practice transactions do not move real money. Always verify important amounts and payment instructions through an official institution or licensed provider.
