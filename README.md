# StudentBridge AI

### Cross-Border & Student Finance Assistant · Clarity V9

**One clear place to plan tuition, compare international transfer costs, protect living expenses, and understand money decisions before studying abroad.**


**Competition-ready documentation:** [Submission guide](docs/COMPETITION_SUBMISSION_GUIDE.md) · [Updated security assessment](docs/SECURITY_SELF_ASSESSMENT.md) · [Technical addendum](docs/TECHNICAL_ADDENDUM.md) · [Third-party review register](docs/THIRD_PARTY_REVIEW.md). The complete release archive is named `StudentBridge_AI.zip`; the root folder is `StudentBridge_AI/`.

**Competition track:** Topic C — Cross-border & Student Finance Assistant  
**Version:** **V9**  
**Source code:** [github.com/Takbir-Al-Tanim/StudentBridge-AI](https://github.com/Takbir-Al-Tanim/StudentBridge-AI)  
**Live website (Render):** **Not verified yet.** After deploying, replace this text with your **real Render URL** from the Render dashboard. Example URL format: `https://YOUR-SERVICE.onrender.com` — **this is a placeholder, not a confirmed live website**.  
**API documentation (when running):** [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)  
**Health check (when running):** [`http://127.0.0.1:8000/api/health`](http://127.0.0.1:8000/api/health)

![StudentBridge AI homepage](docs/screenshots/01-home.png)

> [!IMPORTANT]
> **Educational competition prototype, not a bank.** StudentBridge AI calculates and explains plans, but it does not transfer money, provide verified live bank quotes, issue loans, or automatically pay a university. The payment workflow is a **sandbox simulation**. A separately authorized provider-hosted card checkout is optional and disabled by default. Do not enter real student financial records in a public demo.

> [!NOTE]
> **Screenshot note:** Images in this README were captured from the uploaded **V9 frontend** using an isolated browser with demo/mock API responses. They show the real page layouts, **not** proof of an online Render deployment, live bank connections, live exchange rates, or actual payment processing. Upload the included `docs/screenshots/` folder with this README to make the images display on GitHub.

---

## Contents

1. [The problem and our solution](#1-the-problem-and-our-solution)
2. [What makes StudentBridge AI different?](#2-what-makes-studentbridge-ai-different)
3. [Who can use it? Countries and currencies](#3-who-can-use-it-countries-and-currencies)
4. [Features at a glance](#4-features-at-a-glance)
5. [Complete page-by-page guide with screenshots](#5-complete-page-by-page-guide-with-screenshots)
6. [A real-world student example](#6-a-real-world-student-example)
7. [System architecture](#7-system-architecture)
8. [How the main features work internally](#8-how-the-main-features-work-internally)
9. [AI assistant design and safety](#9-ai-assistant-design-and-safety)
10. [Database design](#10-database-design)
11. [Project folder structure](#11-project-folder-structure)
12. [Technology stack](#12-technology-stack)
13. [How to run on your own laptop](#13-how-to-run-on-your-own-laptop)
14. [MySQL setup: Docker, XAMPP, Aiven, or Railway](#14-mysql-setup-docker-xampp-aiven-or-railway)
15. [Environment variables](#15-environment-variables)
16. [Deploy to Render and publish the website](#16-deploy-to-render-and-publish-the-website)
17. [Keep GitHub and Render updated](#17-keep-github-and-render-updated)
18. [API guide for developers](#18-api-guide-for-developers)
19. [Financial rules and example calculations](#19-financial-rules-and-example-calculations)
20. [Testing: commands, test cases, and evidence](#20-testing-commands-test-cases-and-evidence)
21. [Security, privacy, and limitations](#21-security-privacy-and-limitations)
22. [Data accuracy, sources, and originality](#22-data-accuracy-sources-and-originality)
23. [Competition demo and presentation guide](#23-competition-demo-and-presentation-guide)
24. [Development roadmap](#24-development-roadmap)
25. [Troubleshooting and FAQ](#25-troubleshooting-and-faq)
26. [Submission checklist and useful links](#26-submission-checklist-and-useful-links)

---

## 1. The problem and our solution

### The problem

Studying abroad is expensive, and money planning is often confusing. An international student may have to:

- Pay university tuition in a different currency.
- Understand the **real total cost**, including bank fees and exchange-rate differences.
- Meet a payment deadline, even when a transfer takes several days.
- Keep enough money for rent, food, transport, and emergencies.
- Learn unfamiliar banking and credit rules in a new country.
- Compare information from different websites without knowing which numbers are current or reliable.

**The main problem is not just currency conversion. It is knowing whether a financial decision is affordable, timely, and based on enough evidence.**

### Our solution

**StudentBridge AI** combines multiple planning tools in one understandable website. It helps a student build a plan, check possible financial risks, compare **user-entered** provider quotes, and understand what should be verified before taking any real-world action.

Our aim is simple:

> **Help students make clearer financial plans before moving money across borders.**

### What this project does *not* claim

This software is not a licensed financial institution. It does not promise savings, guarantee delivery times, predict future exchange rates, or verify that any payment route is legally available. This honest limitation is part of the product design.

---

## 2. What makes StudentBridge AI different?

Many finance websites focus on one job, such as sending money, paying tuition, or showing currency balances. StudentBridge AI brings **planning decisions together**, with separate tools that explain their assumptions.

| Key idea | How it helps | Implemented status in V9 |
|---|---|---|
| **Journey Studio** | Prepares one guided tuition, savings, living-cost, and deadline brief | Implemented; planning only |
| **EduRoute comparison** | Ranks entered payment quotes after checking fees, affordability, eligibility, and delivery time | Implemented; quotes are **not** independently verified |
| **Living-cost protection** | Can reserve money for several months of expenses before recommending an entered quote | Implemented as optional planner setting |
| **Budget stress test** | Shows what happens if FX costs, extra fees, or living costs rise | Implemented; hypothetical, not predictive |
| **Explainable Decision Passport** | Records the calculation result, rejected options, warnings, and plan fingerprint | Implemented |
| **Invoice reading** | Finds possible amounts and dates in a text-selectable PDF | Implemented; human confirmation required |
| **Calendar export** | Downloads a tuition reminder for a student's own calendar | Implemented; does not schedule automatic email alerts |
| **Transparent evidence** | Separates published reference rates, student-entered quotes, and missing data | Implemented |
| **Sandbox approval and audit** | Records a practice-only payment after explicit approval | Implemented; no real transfer |
| **Source-aware AI help** | Explains financial facts and points students to relevant tools | Implemented; optional Gemini language layer |

**Design principle:** The interface should be simple, but the calculations, warnings, and evidence must remain clear.

---

## 3. Who can use it? Countries and currencies

V9 supports six countries in its planning forms:

| Country | Currency | Code |
|---|---|---|
| China | Chinese yuan | `CNY` |
| United Kingdom | Pound sterling | `GBP` |
| Japan | Japanese yen | `JPY` |
| South Korea | South Korean won | `KRW` |
| Australia | Australian dollar | `AUD` |
| Bangladesh | Bangladeshi taka | `BDT` |

There are **30 directional country selections**: six origins × five different destinations. For example, **Bangladesh → Australia** and **Australia → Bangladesh** are two different planning directions.

> **30 selections do not mean 30 approved money-transfer routes.** Actual banking or tuition-payment availability depends on the bank, country rules, recipient, amount, and payment method.

---

## 4. Features at a glance

| Feature | Student can do | Result | What still needs human checking |
|---|---|---|---|
| Home | Choose a task or country pair | Opens a suitable tool | Route availability |
| Journey Studio | Enter tuition, savings, living budget, deadline | Financial brief, stress comparisons, action list | Actual invoice, provider quote, bank recipient |
| Send money | Choose countries, amount, fees, markup | Estimated conversion | Live provider rate and all fees |
| Tuition payments | Practice a tuition-payment flow | Practice-only steps and receipt | Real payment uses a separate authorized provider |
| Compare routes | Enter payment quotes, budget, and deadline | Ranked qualifying options and explanations | Provider eligibility and quote accuracy |
| My currencies | Enter balances in six currencies | Estimated combined total | Not linked to real bank accounts |
| My budget | Change FX, extra fees, living costs | Before-and-after scenario | Future rates cannot be predicted |
| Build credit | Select destination | Country guidance and checklist | Local eligibility rules |
| Data sources | Open supporting links and dates | Evidence trail | Source validity and latest updates |
| Payment history | Inspect local sandbox actions | Practice transaction and audit display in development | Not a real bank statement; production access restricted |
| Ask Bridge AI | Ask a finance question | Source-aware explanation, suggested tools | Check important financial claims yourself |

---

## 5. Complete page-by-page guide with screenshots

Each screenshot below is an **illustrative V9 UI preview**. The actual data you see when running the app depends on your database and available external APIs.

### 5.1 Home — your starting point

![Home page](docs/screenshots/01-home.png)

**What you see:** a short introduction, available country pairs, four main service cards, a Journey Studio shortcut, and a note explaining that the website is for planning.

**How to use it:** Click **Make a plan**, choose **Send money**, **Pay tuition**, **Build credit**, or **My currencies**, or use the left navigation.

**Why this page matters:** A new student can choose a task quickly without reading a long manual.

### 5.2 Journey Studio — prepare a complete money plan

![Journey Studio](docs/screenshots/02-journey-studio.png)

**What you enter:** your origin and destination, goal, tuition amount, any scholarship, available funds, protected emergency savings, monthly living cost, number of months, and payment deadline.

**What it produces:** a prepared tuition-and-budget brief, deadline buffer, source-linked reference FX where available, example FX stress scenarios, and next steps.

**How to use it:**

1. Open **Journey Studio**.
2. Choose the two countries.
3. Enter your tuition and savings information.
4. Add your living-cost and emergency reserve amounts.
5. Check the payment deadline.
6. Click **Prepare my complete plan**.
7. Read the result and verify any missing data.
8. Optionally send the reviewed information to the route comparison planner or download a calendar reminder.

**Important:** This workflow is **read-only planning**, not automatic payment. The reference rate is **not** a bank quote.

#### Invoice review inside Journey Studio

The student can also upload a **text-selectable university invoice PDF**. The system extracts *candidate* amounts and dates. The student must select the correct values, verify them against the official invoice, and confirm before the form is filled.

**Current limits:** PDF only; maximum **2.5 MB** and **12 pages**; no general OCR for scanned/image-only invoices; no bank-recipient authenticity verification.

![Synthetic PDF invoice review UI](docs/screenshots/13-pdf-invoice-review.png)

*Illustrative invoice-review step using fabricated test values, not a real student invoice.*

#### Calendar reminder

Journey Studio offers a downloadable `.ics` file. Open that file in Apple Calendar, Google Calendar, or Outlook to add the tuition reminder yourself. The website does **not** read your calendar account or send an automatic reminder email.

### 5.3 Send Money — understand estimated transfer costs

![Send Money page](docs/screenshots/03-send-money.png)

**What you enter:** origin, destination, amount, optional fixed fee, and optional exchange-rate markup.

**What it shows:** an estimated received value using an external published **reference** exchange rate when available. It displays the difference between an estimate and an actual provider quote.

**Example task:** “If I send money from China to Australia, what might the equivalent amount be before a bank confirms fees?”

**Important:** The calculator does not send money or guarantee the estimate.

### 5.4 Tuition Payments — practice the payment journey

![Tuition Payments page](docs/screenshots/04-tuition-payments.png)

**What you see:** a tuition-payment guide and a step-by-step practice flow. A card-checkout section can connect to a **separate provider-hosted** checkout only if a merchant has been specifically configured and authorized.

**How to use it:**

1. Choose the relevant countries and tuition amount.
2. Review the plan and practice method.
3. Check the displayed warnings and simulated amount.
4. Complete the confirmation step to produce a **practice receipt**.

**Important:** There is no built-in card-number form. Never enter a card number or CVC into StudentBridge forms. Live merchant collection is disabled by default.

### 5.5 Compare Payment Routes — choose among entered quotes

![Compare Routes page](docs/screenshots/05-route-comparison.png)

**What you enter:** the destination university or manual tuition amount, scholarship, available balance, emergency reserve, living-cost information, deadline, and up to eight **user-entered** provider quotes.

For each quote, you can enter: provider name, rate, fixed fee, percentage fee, estimated delivery days, whether the provider confirmed eligibility, and an HTTPS source link.

**What it checks:** total cost; whether the payment appears affordable after protected reserves; whether the estimated delivery time fits the deadline; and whether required supporting details are present.

**What it returns:** a comparison with warnings. If an eligible option remains, the application selects the **lowest-cost qualifying entered quote**; it does not declare the cheapest bank in the market.

**Extra feature — Decision Passport:** Once a plan exists, open or download the explanation record with chosen and rejected options, assumptions, source metadata, and a SHA-256 decision fingerprint.

![Illustrative Decision Passport screen](docs/screenshots/14-decision-passport.png)

*Sample Decision Passport with deliberately synthetic entries (SAMPLE-123).*

### 5.6 My Currencies — view combined estimated balances

![My Currencies page](docs/screenshots/06-my-currencies.png)

**What you enter:** balances in the six supported currencies and the target currency.

**What it does:** converts supported balances using available reference data, shows an estimated combined total, and flags missing rates instead of inventing them.

**Important:** The figures are typed by the user in the browser. There is **no bank-account connection** and the feature does not create a real wallet.

### 5.7 My Budget — Financial Digital Twin

![Budget Digital Twin page](docs/screenshots/07-budget-digital-twin.png)

**What you can change:** exchange-rate change, extra transfer fee, and living-cost increase or decrease.

**How to use it:** First create a suitable plan in **Compare Payment Routes**, then open **My budget**, move the sliders, and click **Run stress test**.

**What it shows:** original cost versus the changed-cost scenario, possible money remaining, and whether your protected reserve is still covered.

**Important:** This is a **what-if model**, not a forecast of future currency rates.

### 5.8 Build Credit — learn destination-country basics

![Build Credit page](docs/screenshots/08-credit-guidance.png)

**What you do:** choose a destination country, read the key preparation steps, open relevant source links, and tick off the four-item readiness checklist.

**What it provides:** general information about getting ready for banking and credit in a new country.

**Important:** StudentBridge AI does not check credit scores, decide eligibility, open bank accounts, or submit loan applications.

### 5.9 Data Sources — check where numbers come from

![Data Sources page](docs/screenshots/09-data-sources.png)

**What you see:** published cost benchmarks, historical FX references, and other source registry items. The website explains whether a number is a published reference, a user-provided quote, or unverified/missing.

**How to use it:** open the original source, check its date, then confirm that it is relevant to your country, university, and payment situation.

**Important:** Historical numbers are not current executable offers. Some research values are reference benchmarks rather than individual tuition invoices.

### 5.10 Payment History — review practice actions

![Practice Payment History page](docs/screenshots/10-practice-history.png)

**What you see in development:** local practice transactions and related audit entries.

**What it means:** a sandbox transaction records a **simulation**, not money reaching a university.

**Public deployment rule:** the shared history, audit listing, and audit verification endpoints return **403** when `APP_ENV=production`. These are **not** authenticated multi-user account pages; the project still needs proper login and data isolation before real public use.

### 5.11 Ask Bridge AI — get understandable explanations

![Bridge AI assistant](docs/screenshots/11-ai-assistant.png)

**What you can ask:**

- “How do I compare two tuition payment quotes?”
- “What are important living-cost factors in Japan?”
- “What happens if my exchange rate becomes worse?”
- “Where do I begin building credit in Australia?”
- “What can you do for my university payment plan?”

**How it works:** the assistant uses project information and approved financial calculations to explain results. It may suggest opening Journey Studio or another tool. If Gemini is configured, Gemini can optionally rewrite an already grounded explanation in friendlier language.

**Important:** The language model does not independently verify live banks, execute payments, or override the Python safety rules.

### 5.12 Mobile interface

![Mobile website preview](docs/screenshots/12-mobile-home.png)

The main screens adjust to phone widths, with a smaller page layout and mobile navigation. Basic responsive behavior is included; always review the final public site on the devices you will use in the competition.

---

## 6. A real-world student example

Let's use a **fictional** student, Ayesha, who plans to move from **Bangladesh to Australia**. She wants to pay tuition while still keeping enough money for her first few months of living expenses.

```mermaid
flowchart TD
    A["Ayesha plans to study in Australia"] --> B["Enter her tuition, scholarship, savings, and deadline"]
    B --> C["Journey Studio prepares an indicative budget"]
    C --> D["Review official invoice and living-cost buffer"]
    D --> E["Enter documented quotes from available providers"]
    E --> F{"Quote fits deadline, funds, and stated eligibility?"}
    F -->|No| G["Show why it fails; ask for another quote"]
    F -->|Yes| H["Compare total cost and review Decision Passport"]
    H --> I["Run an FX and extra-fee stress test"]
    I --> J["Download a tuition deadline reminder"]
    J --> K["Optional approved sandbox simulation"]
    K --> L["Practice receipt only; no money transferred"]
```

### What should Ayesha learn?

1. Tuition is not the only cost; living and emergency money must also be protected.
2. The bank's actual fee and exchange rate matter more than the headline reference rate alone.
3. A cheaper quote may be unsuitable if it is late or the provider cannot serve the route.
4. The system can explain why it preferred or rejected the information Ayesha entered.
5. Final beneficiary details, real payment options, and eligibility still need checking directly with the university and the payment provider.

> All names and numbers in a public competition demo should be **fictional** or from examples you have permission to show.

---

## 7. System architecture

### 7.1 Full application architecture

```mermaid
flowchart TB
    USER["Student or competition judge"] --> BROWSER["Browser: desktop or phone"]
    subgraph FRONTEND["StudentBridge AI frontend"]
        HTML["HTML and Jinja2"]
        CSS["Original CSS and responsive layout"]
        JS["JavaScript navigation, forms, charts and UI"]
        HTML --- CSS
        CSS --- JS
    end
    BROWSER --> FRONTEND
    FRONTEND -->|"HTTPS / JSON / PDF upload"| API["FastAPI: app/main.py"]
    subgraph BACKEND["Application logic"]
        VALID["Pydantic input checks"]
        JOURNEY["Journey Studio: app/journey.py"]
        RULES["Payment comparison and stress rules: app/logic.py"]
        ASSIST["Grounded assistant: app/assistant.py"]
        SECURE["Hosted-checkout guard: app/secure_card.py"]
    end
    API --> VALID
    VALID --> JOURNEY
    VALID --> RULES
    VALID --> ASSIST
    VALID --> SECURE
    API <--> DB[("MySQL: plans, research, sandbox, audit")]
    API <--> FX["Frankfurter: reference FX API"]
    ASSIST -. "optional wording help" .-> GEMINI["Gemini API"]
    SECURE -. "only if configured and authorized" .-> STRIPE["Stripe-hosted checkout"]
    RULES --> OUT["Warnings, plan, explanation, and sandbox options"]
    JOURNEY --> OUT
    ASSIST --> OUT
    OUT --> API
    API --> FRONTEND
```

**Plain-English explanation:** The student uses the website. The Python backend validates the information and does the calculations. MySQL saves records when needed. The assistant explains the results. External APIs provide optional reference information, but **no external service is trusted to authorize a transfer simply because it returns text**.

### 7.2 How the website communicates with the backend

```mermaid
sequenceDiagram
    actor Student
    participant UI as Browser interface
    participant API as FastAPI
    participant Rules as Python finance rules
    participant DB as MySQL
    participant Source as Published FX service
    Student->>UI: Enter study goal and money details
    UI->>API: POST /api/journey/prepare
    API->>Source: Request dated reference rate
    alt Rate available
        Source-->>API: Rate and observation date
    else Not available
        Source-->>API: No usable rate
    end
    API->>Rules: Check budget, living costs and deadline
    Rules-->>API: Safe planning results and warnings
    API-->>UI: Prepared plan; no transfer
    UI-->>Student: Show next steps and limitations
    Note over UI,DB: Planning does not need to create a real payment
    Student->>UI: Enter verified provider quotes later
    UI->>API: POST /api/plans
    API->>Rules: Evaluate quotes
    API->>DB: Save plan and audit event
    DB-->>API: Stored decision
    API-->>UI: Ranked quotes and plan reference
```

### 7.3 Deployment architecture: GitHub + Render + MySQL

```mermaid
flowchart LR
    DEV["Developer's laptop"] -->|"git push"| GIT["GitHub repository"]
    GIT -->|"Auto-deploy main branch"| RENDER["Render Web Service: FastAPI + frontend"]
    VISITOR["Public visitor"] -->|"HTTPS"| RENDER
    RENDER -->|"Database connection; TLS as supported"| MYSQL[("Managed MySQL: Aiven or Railway")]
    RENDER -. "optional HTTPS" .-> GEM["Gemini API"]
    RENDER -. "HTTPS reference data" .-> FX["Frankfurter"]
    OPS["Developer / operator"] -->|"Private environment variables"| RENDER
    MYSQL --> BACKUP["Separate database backup"]
```

**Aiven and Railway are alternatives**: use one working MySQL database for a deployment, not two database URLs at once. Your website can stay on Render while the database is elsewhere.

### 7.4 Trust and approval boundaries

```mermaid
flowchart TD
    INPUT["Student input or uploaded PDF"] --> VERIFY["Validate input and treat documents as untrusted"]
    VERIFY --> CALC["Deterministic Python rules"]
    CALC --> SUMMARY["Explainable plan with sources and warnings"]
    SUMMARY --> AI["Optional assistant explanation; read-only"]
    SUMMARY --> DECISION{"Does student want a practice payment?"}
    DECISION -->|No| STOP["Stop: no transaction"]
    DECISION -->|Yes| CONSENT["Explicit checkbox and approval phrase"]
    CONSENT --> ELIGIBILITY{"Quote meets planner checks?"}
    ELIGIBILITY -->|No| BLOCK["Block sandbox action"]
    ELIGIBILITY -->|Yes| AUDIT["Create simulated transaction + audit entry"]
    AUDIT --> RECEIPT["Clearly marked test receipt"]
    AI -. "cannot call payment execution by itself" .-> STOP
```

**Safety idea:** The AI is not allowed to silently move money. The student must approve a simulation, and the backend checks the plan again.

---

## 8. How the main features work internally

### 8.1 Journey Studio

The Journey Studio backend uses `app/journey.py`. It checks the deadline, estimates tuition and protected living costs with a published reference rate (if available), creates example 0%, +5%, and +10% FX stress results, and builds a next-action list. It does **not** create a payment or permanently save personal details as part of this preparation request.

### 8.2 Invoice PDF reader

The backend uses `pypdf` to extract selectable text. It checks the file type and size and searches for *possible* amounts and dates. Document text is never allowed to become instructions for the payment agent. The user checks the original invoice before values are applied.

### 8.3 Fee and route comparison

The calculation logic in `app/logic.py` uses `Decimal` for money math. It evaluates quotes entered by the student; it checks the cost, stated eligibility, arrival time, evidence link and quote expiry. Only a quote passing the required conditions can be recommended among the entered options.

### 8.4 FX and living-cost scenarios

A saved plan can be stress-tested to see what would change if the assumed exchange rate, extra fees, or living cost changed. These figures describe assumptions, not predictions.

### 8.5 Decision Passport and audit

The backend creates a plan fingerprint using SHA-256. The database stores related audit events in an **HMAC-SHA256 linked chain**. The chain can help reveal changes to local records, but it is **not blockchain**, external notarization, or proof of bank settlement.

### 8.6 Sandbox payment logic

The practice workflow requires a confirmed selection and an approval phrase. The backend rejects plans that do not pass its conditions, prevents unintended duplicate processing with an idempotency key, and records a **simulation only**.

### 8.7 Reference data

The FX service returns an observed reference rate, date, and source when available. Missing data is shown as missing. Historical benchmarks are not advertised as current payable tuition or executable transfer quotes.

---

## 9. AI assistant design and safety

```mermaid
flowchart LR
    QUESTION["Student's question"] --> INTENT["Identify country, topic, and requested tool"]
    INTENT --> SOURCES["Approved reference data and source links"]
    INTENT --> PLAN["Existing plan if one was provided"]
    INTENT --> FX["Optional published FX lookup"]
    SOURCES --> ANSWER["Grounded explanation"]
    PLAN --> ANSWER
    FX --> ANSWER
    ANSWER -. "optional language rewrite" .-> LLM["Gemini API"]
    ANSWER --> UI["Answer + evidence + suggested pages"]
    LLM --> UI
```

**How it is implemented:** `app/assistant.py` creates guidance from the known country catalog, data registry, available calculation results, and optional reference rate. The `/api/chat` endpoint may ask Gemini to **rewrite** verified guidance into easier language. The model does not directly execute an international transfer, verify a bank quote, or approve a payment.

**Works without Gemini?** The core finance rules and the assistant's grounded fallback can work without a `GEMINI_API_KEY`. A Gemini connection is an optional improvement, not the source of truth for costs.

---

## 10. Database design

The runtime uses **MySQL 8** through SQLAlchemy and PyMySQL. There are **11 tables** in the supplied database schema.

### 10.1 Database relationship diagram

```mermaid
erDiagram
    COUNTRIES ||--o{ FINANCIAL_BENCHMARKS : has
    COUNTRIES ||--o{ TUITION_BENCHMARKS : has
    COUNTRIES ||--o{ PAYMENT_QUOTES : origin_or_destination
    SOURCES ||--o{ FINANCIAL_BENCHMARKS : supports
    SOURCES ||--o{ TUITION_BENCHMARKS : supports
    SOURCES ||--o{ FX_RATES : supports
    PLANS ||--o{ TRANSACTIONS : records

    COUNTRIES {
        string country_code PK
        string country_name
        string currency_code
        string data_status
    }
    SOURCES {
        int source_id PK
        string publisher
        string title
        string source_url
        string collection_date
    }
    FINANCIAL_BENCHMARKS {
        int benchmark_id PK
        string country_code FK
        decimal amount
        string verification_status
        int source_id FK
    }
    TUITION_BENCHMARKS {
        int tuition_id PK
        string country_code FK
        string institution
        decimal amount
        int source_id FK
    }
    FX_RATES {
        int fx_id PK
        string base_currency
        string quote_currency
        decimal rate
        string rate_date
        int source_id FK
    }
    PAYMENT_QUOTES {
        int quote_id PK
        string origin_country_code FK
        string destination_country_code FK
        string provider_name
        string verification_status
    }
    PLANS {
        string id PK
        string created_at
        string payload_json
        string result_json
        string decision_hash
    }
    TRANSACTIONS {
        string id PK
        string plan_id FK
        string status
        decimal approved_amount
        string idempotency_key
    }
    AUDIT {
        bigint id PK
        string event_type
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
```

**Note:** This diagram shows the major database relationships. Some audit and provider-event references are stored as values rather than enforced foreign keys.

### 10.2 What each table stores

| Table | Purpose |
|---|---|
| `countries` | Supported places and currency metadata |
| `sources` | Publishers, links, dates, and source notes |
| `financial_benchmarks` | Published living-cost or financial reference figures |
| `tuition_benchmarks` | Source-linked academic fee reference information |
| `fx_rates` | Historical/reference FX observations |
| `payment_quotes` | Research quote records; not necessarily verified or current |
| `plans` | Saved input assumptions and generated comparisons |
| `transactions` | **Practice-only** payment transaction records |
| `audit` | Event details and linked integrity hashes |
| `audit_chain_state` | Current integrity-chain state |
| `provider_events` | Minimal optional hosted-checkout event references |

**Database code:** `app/database.py`.  
**Schema file:** `scripts/mysql_schema.sql`.  
**Safe initializer:** `scripts/setup_mysql.py`.

> The project has **no full multi-user authentication or per-student data isolation**. Do not store real confidential student documents in a publicly accessible copy.

---

## 11. Project folder structure

```text
StudentBridge_AI/
│
├── app/
│   ├── main.py                  # FastAPI server and API routes
│   ├── logic.py                 # Financial comparison and stress calculations
│   ├── journey.py               # Journey Studio and calendar creation
│   ├── assistant.py             # Grounded financial assistant
│   ├── database.py              # MySQL schema, persistence, and audit
│   ├── secure_card.py           # Optional provider-hosted checkout safeguards
│   ├── data/                    # App catalog and source registry
│   ├── templates/
│   │   └── index.html           # Main website and all page sections
│   └── static/
│       ├── app.js               # Browser interactions
│       ├── styles.css           # Base styling
│       ├── experience-v8.css    # Existing UI foundation file
│       └── clarity-v9.css       # V9 styling and typography rules
│
├── data/research/corrected/     # Research CSV files used by the app
├── scripts/
│   ├── setup_mysql.py           # Create/seed MySQL safely
│   ├── check_mysql.py           # Read-only database connection check
│   ├── smoke_test_mysql.py      # Writes synthetic test records, opt-in only
│   ├── mysql_schema.sql         # SQL schema reference
│   └── export_mysql_sql.py      # Research/database export support
│
├── tests/                       # Automated unit and API tests
├── docs/
│   ├── screenshots/             # README page screenshots (this documentation bundle)
│   ├── ORIGINALITY_AND_LICENSES.md
│   ├── SECURITY_SELF_ASSESSMENT.md
│   └── ...                     # Other technical and demo documents
│
├── certs/ca.pem                 # Public CA certificate for configured MySQL provider
├── .env.example                 # Safe configuration example
├── .gitignore                   # Prevent local secrets from being committed
├── docker-compose.yml          # Optional local MySQL service
├── requirements.txt             # Python packages
├── run.py                       # Local Python launcher
└── README.md                    # This file
```

**Never upload:** `.env`, `.venv/`, Git secrets, database password files, private keys, real student invoices, or account data. The user-provided ZIP contained a `.env`; remove it from any public release package.

---

## 12. Technology stack

| Area | Technology | Purpose |
|---|---|---|
| Website | HTML, CSS, JavaScript | Interactive frontend and responsive pages |
| Server-side template | Jinja2 | Render the single-page website shell |
| Backend | Python 3.11+, FastAPI, Uvicorn | API and web service |
| Input validation | Pydantic | Check user-provided fields |
| Math | Python `Decimal` | Avoid common floating-point money-calculation errors |
| Database | MySQL 8, SQLAlchemy, PyMySQL | Research, plans, sandbox records, and audit |
| AI | Grounded Python assistant; optional Gemini | Understand questions and explain verified information |
| Reference FX | Frankfurter API | Published exchange-rate observations |
| PDF | `pypdf` | Extract text from selectable invoices |
| Calendar | iCalendar `.ics` file | Download a deadline reminder |
| Optional checkout | Stripe-hosted Checkout | Provider-managed card flow only if separately authorized |
| Testing | pytest, FastAPI TestClient | Automated checks |
| Hosting | GitHub + Render + managed MySQL | Source, website, and database |

No React, Node.js application server, or proprietary commercial frontend template is needed to run this version.

---

## 13. How to run on your own laptop

### 13.1 What you need first

- **Python 3.11** is a tested baseline; use a compatible Python version supported by the package requirements.
- A terminal: macOS Terminal, Windows PowerShell, or Linux shell.
- MySQL 8, supplied by **Docker**, **XAMPP/local MySQL**, or a **managed cloud MySQL service**.
- Internet access if you want reference FX or Gemini API calls.
- Optional: Git for cloning and updating the project.

**You do not need a Gemini key to test the basic financial rules.** Node.js is *optional* and only used for the `node --check` JavaScript syntax command.

### 13.2 macOS — complete setup

**1. Get the source code**

```bash
cd ~/Downloads
git clone https://github.com/Takbir-Al-Tanim/StudentBridge-AI.git
cd StudentBridge-AI
```

If you downloaded a ZIP instead of cloning, extract it and `cd` into the folder that contains `requirements.txt` and `run.py`.

**2. Create an isolated Python environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**3. Create your private configuration file**

```bash
cp .env.example .env
```

Then open `.env` in a text editor. Follow [MySQL setup](#14-mysql-setup-docker-xampp-aiven-or-railway) below and set a correct `DATABASE_URL`. Create your own random `APP_SECRET`:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(48))"
```

Keep the generated value private. Do not paste it into GitHub or screenshots.

**4. Prepare the database**

```bash
python scripts/setup_mysql.py
python scripts/check_mysql.py
```

The setup script creates the required MySQL tables and imports the packaged research CSV values. It is designed not to drop an existing database.

**5. Start StudentBridge AI**

```bash
python run.py
```

**6. Open the website**

- Website: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/api/health`

**Stop the server:** press `Ctrl + C` in Terminal.

**Next day:** run only:

```bash
cd ~/Downloads/StudentBridge-AI
source .venv/bin/activate
python run.py
```

If you saved the code elsewhere, adjust the `cd` path.

### 13.3 Windows 10/11 — PowerShell

Install Python 3.11 and a working MySQL 8 database first. Then:

```powershell
git clone https://github.com/Takbir-Al-Tanim/StudentBridge-AI.git
cd StudentBridge-AI
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Configure your MySQL connection and `APP_SECRET`, then:

```powershell
python scripts/setup_mysql.py
python scripts/check_mysql.py
python run.py
```

Open `http://127.0.0.1:8000`.

If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`, or call `.venv\Scripts\python.exe` directly without activating.

### 13.4 Linux (Ubuntu / Debian)

Install Python, Git, venv, and MySQL or Docker with your package manager. Then:

```bash
git clone https://github.com/Takbir-Al-Tanim/StudentBridge-AI.git
cd StudentBridge-AI
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`, configure a running MySQL 8 database, then:

```bash
python scripts/setup_mysql.py
python scripts/check_mysql.py
python run.py
```

### 13.5 Run on a phone or tablet

The frontend works in a browser, but the **Python server and MySQL database must run somewhere**. A phone cannot run the hosted website simply by opening the source ZIP.

- **Best option:** open the published Render HTTPS URL in the phone browser.
- **Same-Wi-Fi development option:** start the server on a laptop using `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`, find the laptop's LAN IP, and open `http://LAPTOP_LAN_IP:8000` on the phone. Allow the local firewall connection. This is for a **trusted private network only**; do not expose an unprotected development server publicly.

---

## 14. MySQL setup: Docker, XAMPP, Aiven, or Railway

You need **one** working MySQL database connection. Choose whichever option matches your device and budget.

### Option A — Docker Desktop (repeatable local setup)

This repository includes `docker-compose.yml` for a local MySQL 8.4 instance.

1. Install Docker Desktop and start it.
2. Copy `.env.example` to `.env`.
3. In your **private** `.env`, add these variables:

```dotenv
MYSQL_ROOT_PASSWORD=CHOOSE_A_LONG_PRIVATE_ROOT_PASSWORD
MYSQL_APP_PASSWORD=CHOOSE_A_DIFFERENT_LONG_PRIVATE_APP_PASSWORD
DATABASE_URL=mysql+pymysql://studentbridge_app:URL_ENCODED_APP_PASSWORD@127.0.0.1:3306/studentbridge_ai?charset=utf8mb4
APP_ENV=development
APP_SECRET=GENERATE_YOUR_OWN_LONG_RANDOM_SECRET
```

Replace placeholders locally. URL-encode special characters in the database password when placing it in `DATABASE_URL`.

4. Start MySQL and wait until it becomes healthy:

```bash
docker compose up -d mysql
docker compose ps
```

5. Create the app tables and check:

```bash
python scripts/setup_mysql.py
python scripts/check_mysql.py
```

6. Run `python run.py`.

**Docker notes:** The compose file binds MySQL to `127.0.0.1:3306`, so another local MySQL/XAMPP service using that port will conflict. Data lives in the named `studentbridge_mysql` Docker volume. `docker compose down -v` would delete that volume—**do not use it unless you intentionally want to destroy local test data**.

### Option B — XAMPP or an existing local MySQL server

1. Start MySQL from XAMPP or your own MySQL service.
2. Create a database named `studentbridge_ai`.
3. Create a separate MySQL user with access to this database if possible.
4. Set your private `.env` connection, for example:

```dotenv
DATABASE_URL=mysql+pymysql://studentbridge_app:YOUR_URL_ENCODED_PASSWORD@127.0.0.1:3306/studentbridge_ai?charset=utf8mb4
APP_ENV=development
APP_SECRET=GENERATE_YOUR_OWN_SECRET
```

5. Run:

```bash
python scripts/setup_mysql.py
python scripts/check_mysql.py
python run.py
```

The port is often `3306`, but check the value your local MySQL installation actually uses. Do not assume the `root` user has no password.

### Option C — Aiven managed MySQL

1. Create a MySQL service in the [Aiven Console](https://console.aiven.io/).
2. Open the service and create or choose your app database (`defaultdb` or a named database).
3. Copy the **current** host, port, username, and password into your **private** `.env`.
4. Download the service's public **CA certificate** and place it at `certs/ca.pem`.
5. Configure a SQLAlchemy/PyMySQL URL using the correct MySQL CA/TLS options for your provider and installed driver.
6. Run `python scripts/check_mysql.py`, then `python scripts/setup_mysql.py` if the database is empty.

A typical form of the URL used by this project is:

```dotenv
DATABASE_URL=mysql+pymysql://USER:URL_ENCODED_PASSWORD@CURRENT_AIVEN_HOST:PORT/DATABASE_NAME?charset=utf8mb4&ssl_ca=certs/ca.pem
```

The CA certificate is **public certificate material**, not the secret password or private client key. Always verify the server's active hostname; a rebuilding/offline service may not resolve.

### Option D — Railway managed MySQL + Render website

1. Create a MySQL database in the [Railway Dashboard](https://railway.com/dashboard).
2. If Render hosts the backend, enable the required **public TCP access** in the Railway service. Railway's private host (`railway.internal`) cannot be reached directly from Render.
3. Find Railway's **external MySQL hostname and port**. Use the database name and credentials from the Railway service variables.
4. Configure TLS as supported by the Railway MySQL endpoint and verify encryption before using an external database connection. **Do not reuse Aiven's `ca.pem`** for Railway.
5. Create a new private `DATABASE_URL` in Render and test the database connection before switching your demo.

A generic URL shape is:

```dotenv
DATABASE_URL=mysql+pymysql://USER:URL_ENCODED_PASSWORD@RAILWAY_EXTERNAL_HOST:EXTERNAL_PORT/DATABASE_NAME
```

This is a **shape**, not a complete secure-production configuration. Railway billing, egress charges, database volume, backups and TLS settings should be reviewed separately. A new Railway database does not automatically contain Aiven data; migrate only after taking a backup.

---

## 15. Environment variables

A sample `.env.example` is included. Create a new **private** `.env` for local development or enter these variables through Render's secret settings.

| Key | Required? | What it means |
|---|---|---|
| `DATABASE_URL` | Yes | Correct MySQL connection URL |
| `APP_SECRET` | Yes for safe operation | Long random signing secret; keep stable if verifying older audit entries |
| `APP_ENV` | Yes for production policy | `development` locally; `production` on Render |
| `GEMINI_API_KEY` | Optional | Enables optional Gemini wording assistance |
| `GEMINI_MODEL` | Optional | Configured Gemini model identifier |
| `PUBLIC_BASE_URL` | If provider-hosted checkout is configured | Public HTTPS URL for returning from payment provider |
| `CARD_LIVE_ENABLED` | Important safety flag | Keep `false` for competition demo |
| `MERCHANT_AUTHORIZED_TO_COLLECT` | Important safety flag | Keep `false` unless authorized and verified |
| `STRIPE_SECRET_KEY` | Optional | Provider secret; do **not** put in JavaScript or GitHub |
| `STRIPE_PRICE_ID` | Optional | Approved provider-side fixed payment item |
| `STRIPE_WEBHOOK_SECRET` | Optional | Validates provider payment webhooks |
| `AUTHORIZED_PAYEE_NAME` | Optional | Authorized recipient if hosted checkout is configured |
| `AUTHORIZED_INVOICE_REFERENCE` | Optional | Authorized invoice reference if checkout is configured |
| `MYSQL_ROOT_PASSWORD` | Docker only | Private local Docker MySQL root password |
| `MYSQL_APP_PASSWORD` | Docker only | Private local Docker MySQL application password |

**Security rules:**

- Do not upload `.env` to GitHub, including inside ZIP files.
- Do not paste an API key, password, database URL containing credentials, or app secret into screenshots.
- Generate your own `APP_SECRET`; a sample value is not safe for public use.
- Keep `APP_SECRET` stable when existing audit history must remain verifiable. Changing it can invalidate old HMAC verification; plan rotation carefully.
- **Rotate any database passwords, Gemini keys or app secrets previously shown in public/shared messages before deploying.**

---

## 16. Deploy to Render and publish the website

### 16.1 Deployment preparation

Before deploying, confirm:

- Code is committed in the correct GitHub repository and branch.
- The repository includes `app/`, `requirements.txt`, `run.py`, `data/`, `scripts/`, and the public CA file only if needed.
- The repository does **not** include `.env`, `.venv/`, private keys or database dumps with confidential information.
- Aiven or Railway MySQL is running and reachable from the cloud.
- The managed database has been initialized, and `python scripts/check_mysql.py` succeeds when run with the same connection from a trusted device.

### 16.2 Create the Render Web Service

1. Open [Render Dashboard](https://dashboard.render.com/).
2. Select **New → Web Service**.
3. Connect the GitHub repository **`Takbir-Al-Tanim/StudentBridge-AI`**.
4. Use these values:

| Render field | Value |
|---|---|
| Name | `studentbridge-ai` (or another available name) |
| Runtime / Language | Python 3 |
| Branch | `main` |
| Root directory | Leave blank |
| Build command | `pip install -r requirements.txt` |
| Start command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Health check path | `/api/health` |
| Instance type | Choose your available plan |

5. In **Environment**, add `DATABASE_URL`, `APP_SECRET`, `APP_ENV=production`, and optional Gemini settings. For example, you may pin a compatible Python version using Render's supported Python-version mechanism.
6. Set `CARD_LIVE_ENABLED=false` and `MERCHANT_AUTHORIZED_TO_COLLECT=false` for the competition demo.
7. Deploy, then open **Logs** and **Events/Deploys**.

### 16.3 Verify the website

A normal successful startup includes an Uvicorn message similar to **“Application startup complete.”** It is not enough to see the build finish; the website and database health must also work.

Open:

```text
https://YOUR-ACTUAL-RENDER-URL/
https://YOUR-ACTUAL-RENDER-URL/api/health
https://YOUR-ACTUAL-RENDER-URL/docs
```

Check that the health API returns an `ok` status and a **MySQL** database engine. Test the financial forms with sample data, and verify that sensitive production audit/history endpoints are restricted.

### 16.4 Add your real website link here

**Live website:** **NOT YET VERIFIED FROM THE SUPPLIED FILES.**

Before submission, open your service in the [Render Dashboard](https://dashboard.render.com/), copy the **exact public URL**, test it in a logged-out/private browser window, and replace the placeholder near the top of this README. Do not present an untested example address as a live deployment.

### 16.5 Hosting limitations

Render free instances can sleep when inactive. Managed MySQL free tiers may have inactivity or billing limits. An always-on, production-grade setup requires appropriate service plans, backups, security controls, and uptime monitoring. **A public HTTPS website is not automatically a compliant payment system.**

---

## 17. Keep GitHub and Render updated

When you change the website later:

```bash
git status
python -m pytest -q tests
node --check app/static/app.js
python -m compileall -q app

git add app/ docs/ tests/ scripts/ data/ README.md requirements.txt
# Review the staged file names before committing:
git diff --cached --name-only
# Check for common secret markers; this is not a complete secret scanner:
git grep --cached -l -I -E 'AVNS_|AQ[.]|mysql[+]pymysql://avnadmin:' || true

git commit -m "Improve StudentBridge AI V9"
git push origin main
```

If auto-deploy is enabled in Render, a push to `main` can trigger the next deployment. You normally **do not** need a new Render service or GitHub repository. Update Render variables if the code requires new secrets. Apply proper MySQL migrations before code changes that depend on new tables or columns.

> Deleting current GitHub files does **not** remove secrets from old commits. If a secret was ever committed, rotate it and clean the history using an appropriate, reviewed procedure.

---

## 18. API guide for developers

FastAPI automatically provides interactive API docs at `/docs` and an OpenAPI schema at `/openapi.json` while the app runs.

### 18.1 Main endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Website |
| GET | `/api/health` | Database and application health |
| GET | `/api/catalog` | Countries, catalog and source registry |
| GET | `/api/research/summary` | Research overview |
| GET | `/api/research/benchmarks` | Financial reference benchmarks |
| GET | `/api/fx?base=GBP&quote=AUD` | Published reference rate when available |
| POST | `/api/journey/prepare` | Prepare a guided money plan |
| GET | `/api/journey/calendar` | Download an `.ics` deadline reminder |
| POST | `/api/invoices/analyze` | Extract possible PDF invoice fields |
| POST | `/api/plans` | Save and evaluate entered provider quotes |
| GET | `/api/plans/{plan_id}` | Read a saved plan |
| POST | `/api/scenarios` | Evaluate a hypothetical financial shock |
| GET | `/api/passport/{plan_id}` | Explainable decision record |
| GET | `/api/credit/{country}` | Destination credit guidance |
| POST | `/api/chat` | Source-aware financial assistant |
| POST | `/api/demo/prepare` | Prepare practice tuition workflow |
| POST | `/api/sandbox/execute` | Explicitly approved **simulated** payment |
| GET | `/api/sandbox/receipt/{transaction_id}` | Practice receipt |
| GET | `/api/sandbox/history` | Sandbox list; restricted in production |
| GET | `/api/audit` | Audit list; restricted in production |
| GET | `/api/audit/verify` | Audit check; restricted in production |
| GET | `/api/card/availability` | Optional hosted-checkout availability |

There are additional guarded provider-hosted checkout session/webhook endpoints in `app/main.py` if a merchant integration is explicitly configured.

### 18.2 Example: check health

```bash
curl http://127.0.0.1:8000/api/health
```

**Example shape** (values vary by environment):

```json
{
  "status": "ok",
  "version": "9.0.0",
  "mode": "SANDBOX_NO_REAL_MONEY",
  "database": true,
  "database_engine": "mysql"
}
```

### 18.3 Example: download a deadline reminder

```bash
curl -L \
  'http://127.0.0.1:8000/api/journey/calendar?deadline=2026-12-15&title=Tuition%20deadline&remind_days=7' \
  -o tuition-reminder.ics
```

The example date is for illustration only; replace it with the student's actual deadline after verifying the university's instructions.

### 18.4 Example: analyze a permitted sample invoice

```bash
curl -X POST \
  -F "file=@example-invoice.pdf" \
  http://127.0.0.1:8000/api/invoices/analyze
```

Use a **synthetic or permitted sample PDF**. The response contains candidate amounts and dates that must be reviewed.

---

## 19. Financial rules and example calculations

### 19.1 Cost calculation

For a **student-entered quote**:

```text
Tuition still due = Tuition amount - Scholarship amount
Base cost (origin currency) = Tuition still due × Entered provider rate
Percentage fee = Base cost × (Entered fee % / 100)
Total fee = Percentage fee + Fixed fee
Total planned debit = Base cost + Total fee
```

### 19.2 A clear example (fictional numbers)

Assume:

- Tuition = **20,000 GBP**
- Scholarship = **3,000 GBP**
- Entered example rate = **190 JPY for 1 GBP**
- Entered percentage fee = **1%**
- Entered fixed fee = **1,000 JPY**

Calculation:

```text
Tuition due = 20,000 - 3,000 = 17,000 GBP
Base cost = 17,000 × 190 = 3,230,000 JPY
Percentage fee = 3,230,000 × 1% = 32,300 JPY
Total fees = 32,300 + 1,000 = 33,300 JPY
Total planned debit = 3,230,000 + 33,300 = 3,263,300 JPY
```

The entered rate and fees are **illustrative**, not a bank offer. The system must also check funds, the deadline, quote evidence, and declared eligibility before it marks an option as qualifying.

### 19.3 Deadline and budget decisions

```mermaid
flowchart TD
    Q["Entered provider quote"] --> C["Calculate total cost"]
    C --> A{"Affordable after protected reserves?"}
    A -->|No| R1["Reject; show budget shortfall"]
    A -->|Yes| D{"Delivery estimate meets deadline?"}
    D -->|No| R2["Reject; show deadline risk"]
    D -->|Yes| E{"Eligibility stated and evidence link acceptable?"}
    E -->|No| R3["Reject; show missing verification"]
    E -->|Yes| EXP{"Quote unexpired?"}
    EXP -->|No| R4["Reject expired quote"]
    EXP -->|Yes| OK["Compare cost with other qualifying entered quotes"]
```

### 19.4 Financial Digital Twin

The stress test recalculates a scenario using the selected plan's cost basis and user-controlled shocks. **Example:** a +5% exchange-cost change can make tuition more expensive even if the tuition price itself stays the same. It is a scenario, **not an exchange-rate forecast**.

---

## 20. Testing: commands, test cases, and evidence

### 20.1 Automated tests

Run from the project root after installing dependencies:

```bash
python -m pytest -q tests
node --check app/static/app.js
python -m compileall -q app
```

**Verification performed on the uploaded V9 source for this README:**

```text
76 passed
JavaScript syntax check: passed
Python compilation check: passed
```

**Important:** The pytest suite uses a **temporary SQLite database in explicit test mode**. Normal application runtime uses **MySQL**. These automated tests do **not** prove that your Aiven/Railway server, Render deployment, Gemini API, or payment provider is available.

### 20.2 Test-case matrix

| Case | Input/action | Expected behavior | Type |
|---|---|---|---|
| TC-01 | Open `/api/health` with working MySQL | API reports `ok`, database engine `mysql` | Manual integration |
| TC-02 | Select origin and destination as the same country | Input rejected | Automated |
| TC-03 | Scholarship greater than tuition | Input rejected | Automated |
| TC-04 | Enter fixed and percentage fees | Total debit includes both correctly | Automated |
| TC-05 | Enter late delivery estimate | Late route not recommended | Automated |
| TC-06 | Mark route as ineligible | Route not recommended | Automated |
| TC-07 | Remove required quote evidence URL | Route not recommended | Automated |
| TC-08 | Use an expired quote | Quote blocked from qualifying | Automated |
| TC-09 | Enter two routes; cheapest arrives late | Eligible on-time route preferred among entered options | Automated |
| TC-10 | Enter reserve and living-cost protection | Affordability uses protected funds when enabled | Automated |
| TC-11 | Run +10% FX scenario | Scenario increases example payment cost | Automated |
| TC-12 | Submit a payment without explicit sandbox approval | Sandbox action rejected | Automated |
| TC-13 | Repeat same idempotency key | Duplicate test transaction prevented | Automated |
| TC-14 | Submit unsupported/scanned invoice | Reject or warn; no invented invoice amount | Automated/manual |
| TC-15 | Open country credit advice | Appropriate source-based guidance appears | Automated/manual |
| TC-16 | Visit private audit/history endpoints in production | Return 403 | Automated |
| TC-17 | Open website on 390px phone | Navigation/forms remain usable and no horizontal overflow | Manual browser |
| TC-18 | Load actual Aiven or Railway MySQL | Read-only database check works | Manual integration |
| TC-19 | Test Gemini with a valid key | Optional assistant text returns or graceful fallback | Manual integration |
| TC-20 | Deploy Render and open actual URL | Public site loads, health check works, secrets not exposed | Manual integration |

### 20.3 Live MySQL test (separate)

```bash
python scripts/check_mysql.py
```

There is also an **opt-in** MySQL smoke test that creates a **synthetic plan and sandbox payment**. Run it only against a **separate, non-production test database**:

```bash
MYSQL_SMOKE_TEST=YES python scripts/smoke_test_mysql.py
```

**Do not run that write test against production data.** On Windows PowerShell, set the environment variable with `$env:MYSQL_SMOKE_TEST="YES"` before invoking the script.

### 20.4 Evidence for judges

Useful evidence to collect before the submission:

- Screenshot of the successful automated test output.
- Screenshot of `/api/health` showing MySQL health on Render.
- Recorded run through Journey Studio, route comparison, and the Digital Twin.
- Sample Decision Passport JSON with **synthetic** inputs.
- Practice receipt and audit verification output from a private development environment.
- Repository commit history showing independent work and review.
- Source links and the data-accuracy limitations that appear on screen.

Files in this project include `docs/TEST_REPORT.md`, `docs/SECURITY_SELF_ASSESSMENT.md`, and other technical notes. Review their dates before presenting them as current evidence.

---

## 21. Security, privacy, and limitations

### 21.1 What the current code does

- Validates API input with Pydantic and numeric bounds.
- Separates reference FX values from entered provider quotes.
- Refuses unsafe/invalid comparisons and unsupported country pairs.
- Uses SQLAlchemy queries and transactional MySQL storage.
- Requires explicit confirmation for sandbox execution.
- Uses idempotency keys to reduce duplicate test payments.
- Stores event integrity hashes in a linked HMAC chain.
- Rejects oversized/non-PDF invoice uploads and treats PDF text as untrusted.
- Uses an optional **provider-hosted** checkout rather than collecting card numbers directly.
- Restricts shared sandbox-history and audit-list endpoints in production mode.

### 21.2 What the current code does not yet provide

- Full student login, identity verification, and per-user account isolation.
- Certified KYC, AML, sanctions, recipient, or transfer-corridor checks.
- Independently verified live prices from real remittance providers.
- A licensed tuition-payment gateway or confirmed settlement into a university account.
- Fraud verification of invoice beneficiary bank details.
- Real credit scoring, lending approval, or banking integration.
- Automatic email reminders or live calendar-account access.
- End-to-end protection for real financial documents and regulated personal data.
- Guaranteed availability of external FX, Gemini, or cloud hosts.

**This project should be shown using example data only until these gaps are addressed.**

### 21.3 Private information checklist

```text
[ ] .env is NOT committed
[ ] Database passwords and Gemini keys were rotated if previously exposed
[ ] No real student identity, invoice or bank details appear in screenshots
[ ] No payment-card number or CVC is entered into the website
[ ] Production APP_ENV is set to production
[ ] Hosted live checkout flags remain false for the sandbox demo
[ ] Only the required database privileges are granted
[ ] HTTPS and TLS settings are checked for actual deployment
[ ] Database backups and recovery steps exist
```

---

## 22. Data accuracy, sources, and originality

### 22.1 Financial data: show the source and date

The project includes a country catalog, source registry, research CSVs, financial benchmarks and historical FX observations. Some records are explicitly unverified or incomplete. Reference FX from Frankfurter is **not** an executable bank quote.

Before using a value in a public demo, check: (a) where it came from, (b) its publication or observation date, (c) currency and unit, and (d) whether it applies to that student's exact situation. Do not advertise sample or historical numbers as live prices.

**Useful reference:** [Frankfurter API](https://frankfurter.dev/).

### 22.2 Integrity and intellectual property

The competition requires independent work and appropriate licensing. StudentBridge AI V9 includes project-authored UI code and documented third-party dependencies. Studying a competitor's usability does **not** permit copying its HTML/CSS, licensed graphics, trademarks, text, or private data.

**Project checks:**

1. Keep version control history of original contributions.
2. Read the license of each installed dependency and keep any required notices.
3. Verify redistribution rights for the included research CSV files, archived workbooks, PDFs and screenshots.
4. Do not publish downloaded commercial website assets or provider logos without permission.
5. Cite sources, dates, and limits clearly; do not invent partnerships.
6. Keep real credentials and confidential files out of public ZIPs and commits.
7. Review the full official competition rules and privacy policy before submission.

See [`docs/ORIGINALITY_AND_LICENSES.md`](docs/ORIGINALITY_AND_LICENSES.md) for the detailed project checklist. It is **not a legal certificate**. The team owns its original work subject to applicable third-party licenses; the repository does not automatically receive an open-source license merely because it is public.

**Example open-source tools used** (license text and version-specific notices should be verified before publication): FastAPI, Uvicorn, SQLAlchemy, PyMySQL, `pypdf`, pytest, Pydantic, Jinja2, HTTPX, and Python-Dotenv.

---

## 23. Competition demo and presentation guide

The strongest presentation is a **clear, truthful live workflow**. Use one student story instead of showing every screen in random order.

### Suggested five-minute live demo

| Time | What to show | What to explain |
|---|---|---|
| 0:00–0:30 | Homepage | Tuition, FX uncertainty, fees, deadlines, and study budgets are connected problems |
| 0:30–1:20 | Journey Studio | One form checks tuition, savings, living costs, and deadline together |
| 1:20–2:00 | Sample invoice review + source links | Values come from a document or source; they require human verification |
| 2:00–3:00 | Compare Payment Routes | Why one **entered** quote qualifies while another fails on price, deadline or reserve |
| 3:00–3:35 | Budget stress test | How +5% FX and extra fees change the outcome |
| 3:35–4:10 | Decision Passport + credit guidance | Transparent reasoning and next-country readiness |
| 4:10–4:40 | Practice-only payment + receipt | Explicit approval, idempotency and sandbox audit |
| 4:40–5:00 | Close with roadmap | Honest boundaries, research opportunities and future verified integrations |

### Suggested opening (easy English)

> “Many students know their tuition amount but do not know the complete cost of paying it abroad. Fees, exchange rates, delivery time, and living expenses can change the decision. StudentBridge AI brings these checks into one clear plan.”

### Suggested closing

> “StudentBridge AI does not pretend to be a bank. It helps students understand financial choices, check risks, and see why an option is recommended—before making a real payment through an authorized provider.”

### What a judge should be able to verify

- **Task completion:** a student can complete a meaningful financial-planning workflow.
- **Safety:** the interface does not disguise simulated money movement as a real payment.
- **Technical quality:** source code, architecture, API docs, database design, and tests are accessible.
- **Explainability:** calculations have clear inputs, outputs, limits, and source labels.
- **Originality:** the team can explain which parts it developed and which outside tools are used under license.
- **Evidence:** the same workflow can be demonstrated live using a synthetic test story.

**Avoid unsupported claims**, such as a guaranteed annual saving, a verified cheapest bank, approved live remittance routes, or regulatory certification.

---

## 24. Development roadmap

These are **future improvements**, not features already running:

| Priority | Future improvement | What it would add |
|---|---|---|
| High | User accounts and isolated student data | Secure personal dashboards and permission controls |
| High | Verified provider partnerships and quote APIs | Accurate executable transfer offers for eligible routes |
| High | Stronger invoice fraud checks | Beneficiary verification, trusted document handling, OCR |
| High | Production monitoring and backup recovery | More reliable cloud operation |
| Medium | Reminder emails or authorized calendar connection | Opt-in, scheduled reminders |
| Medium | FX alert subscriptions | Notify students if a stated threshold is met |
| Medium | More countries and providers | Broader, evidence-based coverage |
| Medium | University payment integrations | Authorized tuition settlement and provider receipts |
| Later | Credit/loan partner integration | Eligibility guidance from actual authorized partners |
| Later | Consent-based bank-account data integration | Real balances from supported financial institutions |

**Possible business model for future exploration:** university partnerships, provider referral arrangements subject to applicable rules, or institutional planning software. None of these partnerships or fees are currently verified as active in this repository.

---

## 25. Troubleshooting and FAQ

| Problem | Likely cause | First action |
|---|---|---|
| `DATABASE_URL is required` | `.env` missing or variable empty | Copy `.env.example` and configure MySQL privately |
| `Can't connect to MySQL` | Host, port, credentials or database availability | Check managed service status and connection settings |
| `nodename nor servname provided` | Database hostname cannot be resolved | Recheck hostname and DNS; confirm provider service is Running |
| SSL/certificate failure | Wrong CA path/provider certificate or TLS config | Verify `certs/ca.pem` for your **actual** database provider |
| Port `8000` already in use | Another app is running | Stop the old server or use `uvicorn app.main:app --port 8001` |
| Frontend opens but has no data | Backend or API cannot load | Check Terminal logs and `/api/health` |
| Render build succeeds but app fails | Start command/env/database issue | Check Render logs, correct `APP_ENV`, `DATABASE_URL`, start command |
| Gemini does not answer | Key, model, quota or network issue | Check private settings; base financial rules still work |
| Reference rate unavailable | External API cannot be reached | Retry later; do not invent a rate |
| PDF shows no candidates | Scanned/image-only PDF | Enter manually or use future OCR implementation |
| Payment simulation blocked | Missing approval or quote failed conditions | Review rejection explanation and use safe test inputs |
| Audit verification fails | Changed `APP_SECRET` or altered records | Restore correct secret/backup; do not hide failure |
| Railway database not accessible from Render | Railway private host used across platforms | Enable correct external TCP access and TLS |
| Render Free is slow after inactivity | Free instance may sleep | Wait for wake-up or use an appropriate paid plan |
| Old design still visible | Browser cache or old deployment | Check commit/deploy logs and hard refresh |

**Q: Can I use Netlify instead of Render?**  
A: The app is a Python FastAPI service, not just static HTML. Hosting only the frontend on Netlify would require separately deploying and securing the backend; it would not solve database sleep by itself.

**Q: Can the AI pay my tuition for me?**  
A: No. It can prepare information and explain choices. A real payment must use an authorized payment provider and explicit student approval.

**Q: Is a free cloud database guaranteed to run forever?**  
A: No. Check the current provider's inactivity, billing, credit, backup and service policies.

**Q: Can I use real university invoice PDFs in the demo?**  
A: Use a document you are authorized to share, ideally a **synthetic sample** without identifying student or banking details.

**Q: Will V9 work without Gemini?**  
A: Core deterministic calculations and source-based responses do not require a Gemini key.

---

## 26. Submission checklist and useful links

### 26.1 Deliverables

| Deliverable | Where to find it or how to prepare it |
|---|---|
| ✅ Source code | [GitHub repository](https://github.com/Takbir-Al-Tanim/StudentBridge-AI) after the final push |
| ✅ Detailed README | This file (`README.md`) |
| ✅ System architecture | Sections 7, 8, 9, and 10 |
| ✅ Page and feature screenshots | `docs/screenshots/` in this README bundle |
| ✅ Local run instructions | Sections 13–15 |
| ✅ Deployment instructions | Section 16 |
| ⬜ **Verified live website link** | **Add your actual Render URL** after checking deployment |
| ✅ Test descriptions | Section 20 and `tests/` |
| ✅ Security self-assessment | `docs/SECURITY_SELF_ASSESSMENT.md` |
| ✅ Originality/license checklist | `docs/ORIGINALITY_AND_LICENSES.md` |
| ⬜ Recorded successful production demo | Team must record and verify on actual hosted website |
| ⬜ Final official submission requirements | Team must check the latest competition rules and submission portal |

### 26.2 Quick links

- **Project repository:** https://github.com/Takbir-Al-Tanim/StudentBridge-AI
- **Live Render service:** Add your verified service URL before submitting
- **Render dashboard:** https://dashboard.render.com/
- **Aiven console:** https://console.aiven.io/
- **Railway dashboard:** https://railway.com/dashboard
- **Published reference FX service:** https://frankfurter.dev/
- **Local interactive API docs:** `http://127.0.0.1:8000/docs`
- **Technical project docs:** `docs/`
- **Automated tests:** `tests/`

---

## Final note

**StudentBridge AI — Clarity V9** is built to make cross-border student financial planning **clearer, safer, and easier to explain**. It combines budgeting, tuition planning, transparent evidence, practical stress tests, and an explainable decision record in one original interface.

It is a **competition prototype with honest limitations**. The next step toward a real commercial platform is not to remove those warnings—it is to add the verified financial partnerships, user security, compliance reviews, and reliable infrastructure needed to make real student transactions safe.

**Built for Topic C: Cross-border & Student Finance Assistant.**
