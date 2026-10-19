# StudentBridge AI

### Cross-Border & Student Finance Assistant

**A clearer way for international students to plan tuition payments, understand cross-border transfer costs, protect living expenses and prepare financial decisions.**

**2026 Shenzhen International FinTech Competition — International Track, Topic C: Cross-border & Student Finance Assistant**

**Live website:** **https://studentbridge-ai-3.onrender.com/**  
**GitHub repository:** https://github.com/Takbir-Al-Tanim/StudentBridge-AI  
**Online API docs:** https://studentbridge-ai-3.onrender.com/docs  
**Online health check:** https://studentbridge-ai-3.onrender.com/api/health  
**Run on your own computer:** see [Section 13](#13-how-to-run-on-your-own-laptop).

![StudentBridge AI homepage](docs/screenshots/01-home.png)

> [!IMPORTANT]
> **This is a student-built educational finance and competition sandbox, not a licensed bank or remittance provider.** It cannot actually send a transfer, verify beneficiary ownership, issue credit, approve a loan, or settle tuition. Payment records and receipts are marked practice/simulation. The demo profile is not production-grade user authentication. Use fictitious personal and bank details for demonstrations. Optional authorized provider-hosted checkout is disabled by default.

> [!NOTE]
> The site URL was reachable while this README was prepared. The page screenshots are of the supplied frontend rendered with sample/mock API responses where needed; they are **not** proof of real bank prices, successful settlement, live production data or a fully tested cloud deployment. Include `docs/screenshots/` in GitHub for the image links to work.

**Project documentation:** [Architecture](#7-system-architecture) · [Pages and screenshots](#5-complete-page-by-page-guide-with-screenshots) · [Installation](#13-how-to-run-on-your-own-laptop) · [APIs](#18-api-guide-for-developers) · [Tests](#20-testing-commands-test-cases-and-evidence) · [Security assessment](docs/SECURITY_SELF_ASSESSMENT.md) · [Originality and licenses](docs/ORIGINALITY_AND_LICENSES.md).

---

## Contents

1. [The problem and our solution](#1-the-problem-and-our-solution)
2. [What makes StudentBridge AI different?](#2-what-makes-studentbridge-ai-different)
3. [Who can use it? Countries and currencies](#3-who-can-use-it-countries-and-currencies)
4. [Features at a glance](#4-features-at-a-glance)
5. [Complete page-by-page guide with screenshots](#5-complete-page-by-page-guide-with-screenshots)
6. [A student journey: from planning to practice](#6-a-student-journey-from-planning-to-practice)
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
26. [Competition submission checklist and useful links](#26-competition-submission-checklist-and-useful-links)

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

**StudentBridge AI** combines multiple planning tools in one understandable website. It helps a student build a plan, check possible financial risks, compare modeled transfer routes and, through an advanced API, **user-entered** provider quotes, and understand what should be verified before taking any real-world action.

Our aim is simple:

> **Help students make clearer financial plans before moving money across borders.**

### What this project does *not* claim

This software is not a licensed financial institution. It does not promise savings, guarantee delivery times, predict future exchange rates, or verify that any payment route is legally available. This honest limitation is part of the product design.

---

## 2. What makes StudentBridge AI different?

Most transfer websites show a rate or an amount. StudentBridge AI also asks: **Can the student afford it? Will the money be ready before the deadline? Are the source and recipient details trustworthy?**

| Main idea | What it helps with | What the current project actually offers |
|---|---|---|
| **Journey Studio** | Tuition, scholarship, reserve, living expenses, deadline and the next steps in one plan | Guided, read-only preparation and explanatory results |
| **My Profile** | See the active student's name, home country and saved recipients | A **temporary demo sign-in**, not verified identity or a real bank account |
| **Saved beneficiaries** | Avoid retyping a university or recipient's bank details | Recipients stored in the **current server-memory session**; lost when the server restarts |
| **Guided Send Money** | Sender → recipient → payment method → review | Validated transfer **instructions** only, not a bank transfer |
| **Separate bank/card choice** | Keep bank beneficiary steps distinct from card payments | Bank review is prepared in StudentBridge; a merchant-authorized card checkout is separately configured and normally disabled |
| **Tuition Payment Journey** | Learn the process before making a cross-border payment | Four-step practice flow and a **sandbox receipt** |
| **Simple Payment Route Comparison** | Compare cost and delivery trade-offs without a complex banking form | Three **illustrative** route models with published reference FX when available; fees are assumptions, not bank offers |
| **Multi-currency balances** | Estimate a combined total of balances entered by the student | Browser-entered values; no bank integration |
| **Financial Digital Twin** | Stress-test FX, costs and reserve | Hypothetical calculations, not market predictions |
| **Invoice PDF assistant** | Suggest tuition amounts and dates in invoices | Extracts selectable text and requires a human check |
| **Source-aware Bridge AI** | Explain the choices in simple language | Grounded rules and source-based guidance, optional Gemini language assistance |
| **Advanced Decision Passport API** | Explain and fingerprint a detailed, user-quote plan | Developer API capability; **not the default simple comparison screen** |
| **Audit and simulation** | Produce controlled, inspectable evidence for judging | Synthetic transactions, approvals, logs and integrity checks; no financial settlement |

**The main innovation is the combination of understandable interactions, explicit financial rules, clear risk messages and a student-centered workflow.** No real financial partnership or external bank approval should be inferred from the interface.

---

## 3. Who can use it? Countries and currencies

StudentBridge AI supports six countries in its planning forms:

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

| Screen / feature | Input or action | Output | Important limit |
|---|---|---|---|
| Home | Choose a tool, study corridor or quick-start action | Navigates to the relevant form | Country pairs are planning selections, not validated payment channels |
| Journey Studio | Countries, tuition, scholarship, savings, living expenses, deadline | Financial planning brief, stress assumptions and next steps | Planning only; official invoices and provider prices need checking |
| My Profile | Demo name, email, country and a sample password | Session profile and saved-recipient summary | No real password authentication or durable student account |
| Send Money | Sender, beneficiary, account format, route, funding method | Source-dated estimate and signed review/instruction reference | No money sent; account *format* check is not ownership verification |
| Add beneficiary | Sign in and enter recipient details | Select a previously saved recipient during this session | In-memory storage only, not a secure recipient directory |
| Tuition Payments | Tuition details and choice among sample methods | Review, sandbox approval, downloadable test receipt | No real payment or university settlement |
| Compare Payment Routes | Origin, destination, amount, optional deadline and invoice | Ranked **illustrative** cost cards | Fees/route availability are modeled, not real provider quotes |
| My Currencies | Manually entered balances | Estimated combined balance | No linked bank accounts or real wallet |
| My Budget | Change FX, fees, living-cost assumptions | A scenario comparison | Needs a compatible saved plan; outcomes are hypothetical |
| Build Credit | Select destination, check readiness items | Country-specific general steps and links | Not a credit score or product approval |
| Data Sources | Open source cards and published dates | Reference data provenance | May be historical, incomplete, out of date, or jurisdiction-limited |
| Payment History | Open history and activity | Development sandbox/audit records | Public production endpoints are restricted; not a bank statement |
| Ask Bridge AI | Ask a question about tuition, FX, budget, credit | Guidance grounded in supported app data | It cannot approve, verify or move real money |

**What a judge can demonstrate:** a guided plan, protected savings, a server-validated transfer review, a modeled route comparison, a sandbox payment, an explanation of its limitations, and security tests.

---

## 5. Complete page-by-page guide with screenshots

These screenshots were rendered from the **frontend in the supplied project ZIP**, in an isolated browser with locally mocked API data where needed. They document the actual page structure and interaction design. They do **not** show a completed live bank transfer, live provider offers, proof of production authentication or verified settlement. Screenshots using fictional comparison values are specifically called out below.

**For images to appear on GitHub, upload the whole `docs/screenshots/` folder alongside this `README.md`.** The recommended combined documentation ZIP includes those files.

### 5.1 Home — start from a clear dashboard

![StudentBridge AI home](docs/screenshots/01-home.png)

The homepage gives the user a short introduction, a guided plan button, quick transfer/tuition/credit/currency tools, example country pairs, a source-transparency panel and easy sidebar navigation. Select a tool or use **Make a plan**. A route illustration does not guarantee that a real financial provider supports that route.

### 5.2 Journey Studio — a complete tuition-and-living-cost plan

![Journey Studio](docs/screenshots/02-journey-studio.png)

**Inputs:** origin country, study destination, goal, tuition in destination currency, scholarship, money available in origin currency, emergency savings, monthly living costs, months of protected living expenses, and payment deadline.

**Steps:**

1. Open **Journey Studio** and set the country pair.
2. Add verified tuition and scholarship numbers.
3. Enter the amount actually available to spend and the amount you must keep for emergencies.
4. Enter monthly living costs and the months you want to protect.
5. Choose a realistic tuition deadline.
6. Click **Prepare my plan**.
7. Read the summary, affordability warnings, date checks and next-step list.
8. Optionally continue to the simple comparison page or download a `.ics` tuition reminder.

Journey Studio is a **financial preview**, not a guarantee that the bank can deliver the payment. The results may show unavailable information rather than invent a rate.

**Invoice assistance:** click the invoice upload option for a text-selectable university PDF. The application extracts *possible* values, not a verified bill. Verify the amount, currency, deadline and beneficiary against the official invoice before applying any suggestion. The backend supports PDFs up to **4 MB** and **12 pages**; scanned image-only pages are not handled by general OCR.

![Example PDF review UI (illustrative sample)](docs/screenshots/13-pdf-invoice-review.png)

*This additional invoice-review illustration uses synthetic values; its visual styling may differ from the current main-page screenshots. It is included to explain the review process, not to claim automatic invoice validation.*

**Calendar:** the downloaded `.ics` reminder can be imported into Apple Calendar, Google Calendar or Outlook. The software does not send a deadline email by itself.

### 5.3 My Profile — simple sign-in and saved beneficiaries

![My Profile](docs/screenshots/15-my-profile.png)

The profile screen includes **My account**, **Saved beneficiaries**, and **Sign in**. A visitor enters a sample full name, email address, home country and a password of at least six characters to create a session. After that, the profile name and saved recipient summary can appear in the application. The sign-out button ends the session.

![Sample sign-in form](docs/screenshots/17-profile-sign-in-filled.png)

**Security warning:** this is a lightweight **demo session**, not real account registration or password verification. The backend does not check an existing password or offer durable account recovery. Beneficiaries are held in server process memory; data can disappear when the service is restarted or redeployed. Use fictional names, email addresses and bank details when showing this feature publicly. A production student banking website requires proper identity, password, encryption, session, authorization and privacy controls.

### 5.4 Send Money — four connected review steps

![Guided Send Money page](docs/screenshots/03-send-money.png)

Instead of placing everything in one long banking form, the page is organized around four visible steps:

**Step 1 — Sign in and choose corridor.** Choose the sending and receiving countries, enter the sender's name and transfer amount. Signing in allows the demonstration session to keep its temporary list of beneficiaries.

**Step 2 — Add or choose beneficiary.** Select a saved recipient or enter the recipient label, legal name, bank, account number, local routing/branch code, bank city/area and an optional SWIFT/BIC. The expected routing format changes for different destination countries (for example an Australian BSB, UK sort code or Bangladeshi routing number). These checks validate the *format*, not the existence or ownership of the account. A **Save this beneficiary** checkbox and **Add beneficiary + save** action are available to session users.

**Step 3 — Choose method.** Choose **Bank transfer** or **Visa/Mastercard**. The bank selection supports a server-side reference calculation and instruction review. Card payment is a different path that points to the Tuition Payments page; it is only possible with an **authorized payment provider's hosted checkout**, if separately configured. StudentBridge does not collect card number, expiry or CVC.

**Step 4 — Review.** Click **Continue to review**, inspect the reference FX, rate date, masked beneficiary account, recipient, method and warnings. Check the acknowledgement and choose **Prepare transfer instructions**. The backend validates the same details and checks an expiring signed review token; it creates **instructions only**, not a bank payout.

![Beneficiary fields and funding-method choices](docs/screenshots/18-beneficiary-and-method.png)

Never enter a real beneficiary's bank account into a publicly shared competition test. Saving it in this prototype does **not** confirm payee ownership or guarantee permanent storage.

### 5.5 Tuition Payments — four-step simulated payment

![Tuition Payments](docs/screenshots/04-tuition-payments.png)

1. **Details:** choose countries, recipient/university, tuition amount, available funds, emergency savings, deadline and a reference FX rate or user-provided practice rate.
2. **Choose method:** compare the application's **sample payment methods**, fees and approximate times.
3. **Review & pay:** read the warnings and acknowledge that this is a test, then approve the **sandbox** step.
4. **Receipt:** view and download the **practice** confirmation and optionally open payment history or start a new simulation.

An optional provider-hosted card checkout can be connected only by an authorized merchant for a fixed authorized invoice; it is disabled by default. It is **not** a general card-funded cross-border remittance service. Never type card numbers into the application forms.

### 5.6 Compare Payment Routes — simple, banking-relevant fields

![Simple comparison form](docs/screenshots/05-route-comparison.png)

The visible form asks for **sending country**, **university country**, **payable amount**, an **optional deadline**, an **optional recipient/university name**, and an optional **PDF invoice**. This intentionally avoids asking for unrelated details during a basic transfer-price check.

1. Select the two countries.
2. Enter the tuition or amount that must be received.
3. Optionally enter a deadline and invoice.
4. Click **Compare routes**.
5. Review side-by-side modeled transfer options, the estimated sending cost, fees, delivery assumptions, reference exchange rate and publication date.

![Comparison results with explicitly synthetic values](docs/screenshots/16-route-comparison-results.png)

*The results screenshot uses a mocked reference rate and fictional amounts for documentation. The displayed route fees are assumptions made for demonstration and **are not real provider prices**, service guarantees or proof of available banking corridors.*

This simplified screen compares **illustrative partner, bank and card models**. Separately, the backend contains an **advanced `/api/plans`** endpoint for comparing user-supplied provider quotes and generating a **Decision Passport**. The default simple form is **not** that advanced quote-entry workflow; see the API section.

### 5.7 My Currencies — put manually entered balances together

![My Currencies](docs/screenshots/06-my-currencies.png)

Enter amounts in the supported currencies and select the currency for the combined total. The website attempts to use published reference rates and explains missing conversions. This is only a personal estimate. It neither reads bank balances nor stores real money in a wallet.

### 5.8 My Budget — Financial Digital Twin

![Budget stress test](docs/screenshots/07-budget-digital-twin.png)

Create a compatible advanced plan first (or use a development API example), then open **My Budget** and move the FX change, additional fee and living-cost sliders. Click **Run stress test** to compare the baseline and altered scenario. The page can show costs, money remaining and risk to protected savings. With no active plan, the page correctly asks you to create one first. It is **not a prediction** of future exchange rates.

### 5.9 Build Credit — prepare for the destination country

![Credit Guidance](docs/screenshots/08-credit-guidance.png)

Select a country to read entry-level guidance on banking and credit readiness, including documents, local eligibility and responsible repayments where applicable. Use the four-item checklist and open the reference link. It does **not** open accounts, fetch a credit bureau score or decide whether someone qualifies for a card or loan.

### 5.10 Data Sources — understand evidence and its date

![Data Sources](docs/screenshots/09-data-sources.png)

This page provides published student-finance/cost and visa-related references, historical currency data, source metadata, links and status markers. It distinguishes **published references**, **entered values** and **unverified or unavailable information**. Historical sources cannot be treated as today's payable tuition amount or bank exchange quote.

### 5.11 Payment History — sandbox activity only

![Payment History](docs/screenshots/10-practice-history.png)

The development interface can show practice transaction history and audit events. The endpoints for **shared history and audit listing/verification return HTTP 403 in production**, so a public visitor may see a restricted-access message. This is intentional but is **not** equivalent to a secure authenticated multi-user banking statement.

### 5.12 Ask Bridge AI — the source-aware finance helper

![Ask Bridge AI assistant](docs/screenshots/11-ai-assistant.png)

Ask plain-language questions, for example: “How should I plan tuition in the UK?”, “What if the exchange rate worsens?”, “What costs matter in Japan?”, or “How do I compare student transfers?”. The assistant uses program rules and source-linked data to explain the issue; optional Gemini integration can make the writing more conversational. It cannot authenticate a bank, approve money transfers or replace the explicit user confirmations.

### 5.13 Mobile and smaller screens

![Mobile dashboard](docs/screenshots/12-mobile-home.png)

The layout adapts to smaller screens and provides mobile navigation, stacked cards and scrollable forms. For a phone, the easiest access is the **hosted HTTPS website**; the app backend and database must run on a server or computer.

### 5.14 Decision Passport — advanced, explainable developer result

![Illustrative Decision Passport](docs/screenshots/14-decision-passport.png)

For an advanced plan created through `/api/plans`, the `/api/passport/{plan_id}` endpoint can return the plan's selection reasoning, limitations, reference metadata and a SHA-256 fingerprint. The screenshot is an **illustrative archived example**, not a native page of the new simplified comparison UI and not proof that a provider approved the result. See [How the main features work internally](#8-how-the-main-features-work-internally) and [API guide](#18-api-guide-for-developers).

---

## 6. A student journey: from planning to practice

Imagine a **fictional** student, Ayesha, who is preparing to study in Australia while her family has savings in Bangladesh.

```mermaid
flowchart TD
    A["Ayesha opens StudentBridge AI"] --> B["Select Bangladesh to Australia"]
    B --> C["Journey Studio: tuition, scholarship, savings, living costs and deadline"]
    C --> D["Read the budget and deadline checks"]
    D --> E["Compare illustrative payment route costs"]
    E --> F["Review reference date and all assumed fees"]
    F --> G["Optional demo sign-in and sample beneficiary"]
    G --> H["Generate a bank transfer review without sending money"]
    H --> I["Try the separate tuition-payment sandbox"]
    I --> J["Download an explicitly simulated receipt"]
    J --> K["For real payment: verify with university and licensed provider"]
```

**What the student learns:** tuition is not the only cost; keeping money for rent and emergencies matters; a fast method may cost more; a modeled comparison is not a price quotation; a bank's real fees, exchange rate, legal corridor and recipient account must be confirmed outside this prototype.

**What a judge can evaluate:** the quality of the task flow, the clarity of each decision, the enforced sandbox boundary, source provenance and known risks. Always use fictional demonstration details.

---

## 7. System architecture

### 7.1 Overall application diagram

```mermaid
flowchart TB
    USER["Student / competition judge"] --> WEB["Browser on desktop or mobile"]
    WEB --> UI["HTML + CSS + JavaScript frontend"]
    UI --> API["FastAPI application · app/main.py"]
    API --> VAL["Pydantic validation + input safeguards"]
    VAL --> JOURNEY["Journey and invoice planning"]
    VAL --> TRANSFER["Bank transfer instruction flow + signed review token"]
    VAL --> ROUTES["Simple modeled route comparison"]
    VAL --> FINANCE["Advanced deterministic finance engine"]
    VAL --> PROFILE["Temporary demo sessions + saved beneficiaries"]
    VAL --> AGENT["Source-aware finance assistant"]
    JOURNEY --> DATA["Published FX and referenced research"]
    TRANSFER --> DATA
    ROUTES --> DATA
    FINANCE --> DB[("MySQL research, plans, sandbox and audit")]
    PROFILE --> MEMORY["Server memory - temporary / not a real bank login"]
    AGENT -. "optional explanation wording" .-> GEMINI["Google Gemini API"]
    API --> AUDIT["Sandbox simulation + HMAC audit events"]
    AUDIT --> DB
    API -. "authorized merchant only; off by default" .-> CHECKOUT["Provider-hosted card checkout"]
    API --> UI
```

**In simple words:** the user clicks a page, the browser asks the Python server for information, and Python checks it. MySQL keeps research, plans and simulated audit data. The temporary profile/beneficiary feature lives in the running application's memory, not in a production banking account database. External published rates are observations, not executable quotes.

### 7.2 Transfer review — not a real transfer

```mermaid
sequenceDiagram
    actor Student
    participant Frontend as Browser
    participant Backend as FastAPI
    participant FX as Reference FX source
    Student->>Frontend: Enter corridor and beneficiary
    Student->>Frontend: Select bank transfer
    Frontend->>Backend: POST /api/transfers/quote
    Backend->>Backend: Validate fields, country routing formats
    Backend->>FX: Obtain a dated reference rate
    FX-->>Backend: Reference rate, date, source (if available)
    Backend-->>Frontend: Masked review + expiring signed token
    Frontend-->>Student: Show account last digits and warnings
    Student->>Frontend: Acknowledge details
    Frontend->>Backend: POST /api/transfers/prepare
    Backend->>Backend: Verify signed token and unchanged inputs
    Backend-->>Frontend: Instructions prepared only
    Note over Backend,Frontend: No settlement provider is called and no funds are moved
```

The review token is an integrity/expiry safeguard, **not a bank payment authorization**. The bank details must be checked with a licensed provider before a real transfer.

### 7.3 Demo account and beneficiary flow

```mermaid
flowchart LR
    SIGN["Sample name, email, country, password field"] --> SESSION["Create temporary in-memory session"]
    SESSION --> COOKIE["Browser session cookie"]
    COOKIE --> PROFILE["Profile summary"]
    PROFILE --> SAVE["Save or select example beneficiary"]
    SAVE --> RAM["Recipients in server memory"]
    RAM --> RESET["Lost when session/server state ends"]
```

This is **demonstration identity UI** only. In the current code, the password field does not verify a registered user. No sensitive personal bank data should be used.

### 7.4 Financial decision and safety boundary

```mermaid
flowchart TD
    INPUT["Amount / deadline / financial assumptions"] --> CHECK["Pydantic checks and financial rules"]
    CHECK --> PLAN["Planning result and explicit caveats"]
    PLAN --> SIMPLE["Modeled route comparison (not bank prices)"]
    PLAN --> ADV["Advanced user-entered quote evaluation API"]
    ADV --> PASS["Optional Decision Passport and scenarios"]
    ADV --> GATE{"Eligible quote + explicit sandbox approval?"}
    GATE -->|No| BLOCK["Reject simulated action"]
    GATE -->|Yes| SIM["Create test transaction + audit hash"]
    SIM --> RECEIPT["Sandbox receipt: zero real funds moved"]
```

### 7.5 Deployment architecture

```mermaid
flowchart LR
    DEV["Development computer"] -->|git push| GIT["GitHub repository"]
    GIT -->|Deploy branch| RENDER["Render: FastAPI + frontend"]
    BROWSER["Visitors via HTTPS"] --> RENDER
    RENDER <-->|SQL / TLS when supported| MYSQL[("Managed MySQL: Aiven or Railway")]
    RENDER -. "HTTPS" .-> FX["Published reference FX"]
    RENDER -. "optional API" .-> AI["Gemini"]
    OPS["Private environment variables"] --> RENDER
    MYSQL --> BACKUPS["Database backups operated separately"]
```

**Your live website:** https://studentbridge-ai-3.onrender.com/

### 7.6 Main code responsibilities

| File | Role |
|---|---|
| `app/main.py` | FastAPI routes, validation, demo sessions, transfers and page serving |
| `app/transfer_flow.py` | Recipient/account format checks, transfer details and review logic |
| `app/journey.py` | Tuition / living expense planning, steps and calendar reminders |
| `app/logic.py` | Advanced route finance math, affordability, deadlines, scenario checks |
| `app/assistant.py` | Source-aware Bridge AI response logic |
| `app/database.py` | MySQL data, plans and HMAC audit chain |
| `app/secure_card.py` | Guardrails for optional authorized, provider-hosted card checkout |
| `app/templates/index.html` | HTML for all app screens |
| `app/static/app.js` | Navigation, forms, local interactions and API integration |
| `app/static/*.css` | Styles and responsive layouts |

---

## 8. How the main features work internally

### 8.1 Journey Studio and living-cost shield

`app/journey.py` reads tuition, scholarship, savings, reserves and living-cost assumptions. Where a suitable published reference rate is available, the code estimates the origin-currency cost; it can also describe what-if FX changes and reminders. This planning request itself is not a bank transfer.

### 8.2 Invoice reader

`POST /api/invoices/analyze` accepts a PDF and uses `pypdf` to extract selectable text. It checks the upload size, file signature/type and page limit, then produces *candidate* amounts and dates. The visitor verifies the official invoice. Scanned PDFs may require manual entry. An invoice is untrusted input; document instructions must never become financial authority.

### 8.3 Temporary demo login and beneficiaries

`POST /api/auth/login` creates a server-memory session based on submitted demo details. A cookie points to the temporary record; `GET /api/auth/profile` displays a summary. `POST /api/beneficiaries` stores a bounded list of beneficiaries within that session; list responses mask full account numbers. The entries disappear on server restart or logout. **The password is not compared with a registered password database.** This is not secure production authentication.

### 8.4 Bank transfer preparation

`app/transfer_flow.py` and `/api/transfers/quote` validate the corridor, required account/routing formatting, amount and data types. The backend requests a published reference FX observation and creates a time-limited signed review token. `/api/transfers/prepare` verifies the unchanged data and explicit confirmation; the result is a prepared-instructions reference, **not settlement**. Full account numbers are not intentionally written into the MySQL plan/audit record by this transfer flow.

### 8.5 Simpler payment route cards

`POST /api/routes/compare` computes example partner, bank and card route costs based on the **published reference exchange rate plus hard-coded modeled fees, percentages and markups**. It returns comparative cards and a suggested route under those assumptions. These costs and arrival-time labels are **not obtained from the named real financial institutions**, and the suggestion is not proof of eligibility or actual cost. An approaching deadline can change which sample route the model highlights.

### 8.6 Advanced quote evaluation is separate

`POST /api/plans` remains available for developers/tests. It accepts user-provided provider quotes, dates, fee fields, declared eligibility, budget and protected reserve. `app/logic.py` uses Python `Decimal` for fee calculations and evaluates affordability and deadline conditions. `/api/passport/{plan_id}` returns reasoning and a SHA-256 integrity fingerprint. The **visible simple route comparison does not expose the entire advanced quote editor**.

### 8.7 Sandbox tuition payment and receipts

The separate Tuition Payments UI walks through details, sample payment methods, review and explicit approval. The backend creates **simulated transactions** and can produce a test receipt; an idempotency key reduces accidental duplicate test entries. Do not submit actual tuition payments or bank credentials in the public demo.

### 8.8 HMAC-linked audit events

An audit event contains a hash linked to the previous event and derived using an application secret. This makes accidental/unauthorized record changes easier to detect in the local evidence flow. It is **not a blockchain**, not an independent bank ledger and not proof of settlement. Rotating `APP_SECRET` without planning can invalidate old HMAC verification.

### 8.9 Reference FX data and fallback

The project uses public financial reference feeds, preferring Frankfurter and using a fallback feed in supported cases. Every rate must be treated as **a published observation**, not a bank's executable spread-inclusive quote. If no acceptable reference is available, the relevant calculation can fail safely or ask for later retry.

### 8.10 Optional hosted card flow

`app/secure_card.py` guards a merchant-authorized Stripe-hosted checkout. The application does not display or process raw card credentials. Merchant authorization, approved payee/invoice, configuration and payment-provider confirmation are required; competition demonstrations should keep real charging disabled.

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

> The project has **demo session login, not full verified multi-user authentication or durable per-student data isolation**. Do not store real confidential student documents in a publicly accessible copy.

---

## 11. Project folder structure

```text
StudentBridge_AI/
│
├── app/
│   ├── main.py                  # FastAPI server and API routes
│   ├── logic.py                 # Financial comparison and stress calculations
│   ├── transfer_flow.py           # Beneficiary formats and transfer preparation
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
│       ├── clarity-v9.css       # Style asset filename retained by code
│       └── finance-v10.css      # Banking layouts and step forms
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

**Never upload:** `.env`, `.venv/`, Git secrets, database password files, private keys, real student invoices, or account data. **The uploaded ZIP contained a private `.env` and a `.venv/` directory. These are intentionally excluded from the clean documentation/project bundle. Rotate any secrets that were ever exposed or committed; `.gitignore` cannot erase prior Git history.**

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
| Reference FX | Frankfurter and supported fallback reference feed | Published exchange-rate observations, not bank prices |
| PDF | `pypdf` | Extract text from selectable invoices |
| Calendar | iCalendar `.ics` file | Download a deadline reminder |
| Optional checkout | Stripe-hosted Checkout | Provider-managed card flow only if separately authorized |
| Temporary profile | In-memory application sessions and browser cookie | Demo sign-in and beneficiaries; not bank authentication |
| Transfer review | Format validation, HMAC-signed expiring token | Prepare a validated instruction only |
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

The setup script creates the required MySQL tables and imports the packaged research CSV values. It is designed not to drop an existing database. If `DATABASE_URL` is wrong or the MySQL service is stopped, the server cannot initialize normally.

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

A sample `.env.example` is included. **The published URL is `https://studentbridge-ai-3.onrender.com/` and can be used without installing Python on a visitor's device.** For local development, create a **private** `.env`. For hosting, enter the same necessary values in Render's secret settings; do not upload the `.env` file.

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
https://studentbridge-ai-3.onrender.com/
https://studentbridge-ai-3.onrender.com/api/health
https://studentbridge-ai-3.onrender.com/docs
```

Check that the health API returns an `ok` status and a **MySQL** database engine. Test the financial forms with sample data, and verify that sensitive production audit/history endpoints are restricted.

### 16.4 Public service link

**Website: https://studentbridge-ai-3.onrender.com/**

The page was reachable during documentation review. **Reachability does not independently confirm live MySQL health, correct credentials, secure accounts or working third-party integrations.** Before the presentation, check the live site and `/api/health` in an incognito window; verify the database engine is `mysql` and the service logs show no errors.

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

git commit -m "Update StudentBridge AI documentation and screenshots"
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
| GET | `/api/auth/profile` | Read temporary demo session profile |
| POST | `/api/auth/login` | Create a temporary demo session; **not verified authentication** |
| POST | `/api/auth/logout` | End temporary session |
| GET | `/api/beneficiaries` | List session beneficiaries (requires demo session) |
| GET | `/api/beneficiaries/{beneficiary_id}` | Read a session recipient for prefill (requires demo session) |
| POST | `/api/beneficiaries` | Save a temporary session recipient |
| GET | `/api/transfers/requirements` | Bank-routing code guidance by country |
| POST | `/api/transfers/quote` | Get validated beneficiary review with reference FX and signed token |
| POST | `/api/transfers/prepare` | Prepare review instructions only; **no transfer** |
| POST | `/api/routes/compare` | Compare the built-in **illustrative** route models |
| POST | `/api/plans` | Advanced evaluation of **user-entered** provider quotes (developer API) |
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

**Example selected fields** (the real response can contain other metadata):

```json
{
  "status": "ok",
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

### 18.5 Basic curl example: country and rate requirements

```bash
curl http://127.0.0.1:8000/api/transfers/requirements
```

This explains country-specific bank routing fields. It **does not** verify the bank or create an account.

### 18.6 Basic curl example: simple route comparison

```bash
curl -X POST http://127.0.0.1:8000/api/routes/compare \
  -H 'Content-Type: application/json' \
  -d '{"origin":"Bangladesh","destination":"Australia","tuition_amount":8000,"deadline":"2026-12-10","recipient_name":"Example University"}'
```

The route values are **modeled examples**. A working reference-rate source is required. Use a sample date that is still in the future when testing deadline suitability. On Windows PowerShell, use `Invoke-RestMethod` or escape JSON according to your shell.

---

## 19. Financial rules and example calculations

### 19.1 Cost calculation

For the **advanced developer API using student-entered quotes** (not the simple on-screen model):

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

### 19.4 Simplified on-screen route calculation

The simple comparator instead applies example fixed fees, percent charges and rate markups to a published reference FX observation. The three example routes are not obtained through real bank pricing APIs. When deadline information is provided, it can change the highlighted model. A displayed "recommended" card means **best among these modeled examples under coded assumptions**—not an approval to use that bank or provider.

### 19.5 Financial Digital Twin

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

**Fresh verification on the supplied project source (19 October 2026):**

```text
85 passed in 6.16s
JavaScript syntax check: passed
Python compilation check: passed
```

The archived `evidence/TEST_RESULTS.txt` records an earlier run with **76 passed**; the results above are from a new run against the source used for this README. Both use an isolated disposable test database, not live MySQL or bank networks.

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
| TC-20 | Open the shared Render URL | Public site loads, health check works, secrets not exposed | Manual integration |

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

### 20.5 Additional checks for the guided banking flow

| Test | Steps | Expected result |
|---|---|---|
| TC-21: navigation | Open Home, Profile, Send money and Compare | Each page responds to navigation; no dead buttons |
| TC-22: demo session | Sign in with fictional data, open Profile, log out | Profile changes for the temporary session; sign-out clears it |
| TC-23: save example beneficiary | Sign in, use valid fictional recipient fields, click save | Recipient available in current session; account masked in list |
| TC-24: destination routing format | Enter unsupported or incorrectly formatted routing number | Server returns readable validation warning |
| TC-25: review token | Re-submit changed details or an expired token | `/api/transfers/prepare` rejects altered/expired review |
| TC-26: card separation | Select Visa/Mastercard in Send money | Directed toward merchant-hosted tuition checkout flow; no card fields in app |
| TC-27: simple comparison | Enter country pair and payable amount | Returns model cards with source/date if reference FX available |
| TC-28: restart session | Restart backend after a demo beneficiary is saved | In-memory recipient is lost; cannot be described as durable account storage |
| TC-29: sensitive production endpoints | Set `APP_ENV=production` with safe non-production test deployment | Public shared history/audit endpoints return 403 |
| TC-30: mobile | Verify 390px and desktop screens | Content readable with responsive layout |

**Executed-documentation check:** screenshots were captured from the supplied frontend using an isolated Chromium page and synthetic API data. This verifies page rendering and navigation in that environment, **not** deployment, provider availability or banking settlement.

---

## 21. Security, privacy, and limitations

### 21.1 What the current code does

- Validates API input with Pydantic and numeric bounds.
- Separates published reference FX from both user-entered advanced quotes and hard-coded example routes.
- Supports server-validated beneficiary format checks and time-limited HMAC-signed transfer reviews (instructions only).
- Keeps demo beneficiaries in server process memory; beneficiary list responses mask account details.
- Refuses unsafe/invalid comparisons and unsupported country pairs.
- Uses SQLAlchemy queries and transactional MySQL storage.
- Requires explicit confirmation for sandbox execution.
- Uses idempotency keys to reduce duplicate test payments.
- Stores event integrity hashes in a linked HMAC chain.
- Rejects oversized/non-PDF invoice uploads and treats PDF text as untrusted.
- Uses an optional **provider-hosted** checkout rather than collecting card numbers directly.
- Restricts shared sandbox-history and audit-list endpoints in production mode.

### 21.2 What the current code does not yet provide

- Production-grade registered student accounts, password verification, MFA, persistent storage and verified identity. **The demo login is not a secure account system.**
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

### 21.5 Specific caution about the demo login

The current `POST /api/auth/login` endpoint creates an application session using the provided form values. It is not backed by a registered password database, and the demo cookie is created with `secure=False` in the code. Beneficiary records are stored temporarily in process memory and some API operations are publicly accessible as designed for a competition sandbox. **Do not collect real identity documents, banking credentials, genuine bank account numbers or private invoices in this public demo.** For any real pilot, use secure authentication, HTTPS-only cookies, session expiration and revocation, per-user ownership checks, encryption/data minimization, rate limiting, deletion policies, monitored audit access and a security review.

### 21.6 Financial and legal limitations

StudentBridge AI is an educational competition prototype, **not a bank, lender, regulated money transmitter or licensed investment adviser**. It does not implement real transfers, KYC/AML/sanctions checks, approved bank connectivity, verified beneficiary ownership, live bank cost quotes, credit approval or guaranteed settlement. Published reference FX rates can be old, different from provider buy/sell rates, or unavailable. Route illustrations are pricing assumptions. A public HTTPS address alone does not make the product safe for real financial data.

---

## 22. Data accuracy, sources, and originality

### 22.1 Financial data: show the source and date

The project includes a country catalog, source registry, research CSVs, financial benchmarks and historical FX observations. Some records are explicitly unverified or incomplete. Reference FX from Frankfurter is **not** an executable bank quote.

Before using a value in a public demo, check: (a) where it came from, (b) its publication or observation date, (c) currency and unit, and (d) whether it applies to that student's exact situation. Do not advertise sample or historical numbers as live prices.

**Useful reference:** [Frankfurter API](https://frankfurter.dev/).

### 22.2 Integrity and intellectual property

The competition requires independent work and appropriate licensing. StudentBridge AI includes project-authored UI code and documented third-party dependencies. Studying a competitor's usability does **not** permit copying its HTML/CSS, licensed graphics, trademarks, text, or private data.

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

### 22.5 Competition intellectual-property and originality conditions

The supplied Appendix 2 (page 4, **Integrity and IP**) says entries must be **independently completed**, with no plagiarism or infringement. It requires third-party data, code and open-source components to be **appropriately licensed**. Contestants keep their intellectual-property ownership, while the organizer may use entry and team information for **non-commercial promotional activity** on a non-exclusive, royalty-free basis, subject to the official Competition Rules and Privacy Policy.

This README documents the project; it does **not** certify that all data permissions, third-party license obligations or team author contributions have been cleared. **The contestants must check them before final submission.** Keep `docs/ORIGINALITY_AND_LICENSES.md` and `docs/THIRD_PARTY_REVIEW.md` together with the source.

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

### 23.4 Project team

| Team member | Student ID | University | Department |
|---|---|---|---|
| Md. Takbir Al Tanim | 2331694 | Independent University, Bangladesh | Computer Science and Engineering |
| Tahura Anzum Toa | 2230230 | Independent University, Bangladesh | Computer Science |
| Md. Mohiul Alam | 2311959 | Independent University, Bangladesh | Computer Science and Engineering |
| Mosfiqa Akter Sohely | 2331557 | Independent University, Bangladesh | Computer Science and Engineering |

This roster is based on the team information provided for the presentation. Confirm exact registration spellings and eligibility in the official submission form.

### 23.5 What the official International Track asks for

According to the attached **PBCSF Appendix 2** (pages 2–4):

- **Theme:** “AI as a Financial Participant”; build an agent capable of doing useful work in a financial scenario.
- **Our chosen topic:** **Topic C — Cross-border & Student Finance Assistant**, covering tuition, remittances, credit readiness and multiple currencies.
- **Scoring:** **Task completion 40%**, **security & compliance 30%**, **innovation & interaction 30%**. The optional on-chain challenge bonus does not describe this project's scope.
- **Team:** 2–5 eligible full-time students; the International Track expects at least **60% non-Chinese nationals** and university affiliation outside the stated Chinese regions. Consult full eligibility terms.
- **Language:** English for submission, presentation and review.
- **Deadline:** **20 October 2026, 23:59 Beijing (UTC+8)**; **20 October 2026, 21:59 Bangladesh (UTC+6)**.
- **Required submission materials:** technical documentation describing architecture, algorithms and security; slide deck for a presentation no longer than **10 minutes**; source code with README, GitHub URL, deployment directions and test cases; **security self-assessment** with permission tiers and known risks; **execution evidence**. For Topic C, sandbox/simulated-account operations and logs are acceptable proof of the demonstration workflow.
- **Optional video:** no more than **5 minutes**.
- **Originality and IP:** independent work, valid third-party licenses, no plagiarism or infringement (see Section 22).

These are summarized requirements from the uploaded appendix; the complete organizer rules and privacy policy on the official website control.

**Official website:** https://fintechathon.g-ican.com/  
**Contact listed in appendix:** wangyr@pbcsf.tsinghua.edu.cn

---

## 24. Development roadmap

These are **future improvements**, not features already running:

| Priority | Future improvement | What it would add |
|---|---|---|
| High | Replace demo login with verified, persistent user accounts and isolated student data | Secure personal dashboards and permission controls |
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

**Q: Will StudentBridge AI work without Gemini?**  
A: Core deterministic calculations and source-based responses do not require a Gemini key.

---

**Q: Does my profile mean I have a real bank account?**  
A: No. Profile creation is a temporary demo session. It does not verify a password or identity, and it does not store a secure financial account.

**Q: Where did my saved beneficiary go after restart?**  
A: Saved beneficiaries live in server process memory. They disappear when the relevant session/server state ends. This is expected for the demonstration implementation.

**Q: Is a "recommended route" a real bank offer?**  
A: No. The simplified comparison applies example fees and published reference rates. Confirm availability, prices, requirements, timing and beneficiary details with a licensed provider.

**Q: Does the 4-step transfer page actually send money?**  
A: No. It prepares validated transfer review instructions. The tuition-payment page also runs a practice sandbox unless a separate merchant-authorized hosted checkout has explicitly been configured.

**Q: Why can I not see payment history on the public hosted website?**  
A: The shared list and audit endpoints are blocked in production. That is safer than exposing everyone's demonstration records, but it does not replace a proper private student activity dashboard.

**Q: Can I unzip the ZIP and double-click index.html?**  
A: No. The frontend needs the FastAPI backend. Run `python run.py` after configuring MySQL, or open the existing published URL.

---

## 26. Competition submission checklist and useful links

### 26.1 Official submission package requirements

| Requirement | Location or action | Status |
|---|---|---|
| Project title and topic | StudentBridge AI, Topic C | Documented |
| Source code | `app/`, `scripts/`, `tests/`, `data/`, root Python files | Included in supplied project |
| Detailed `README.md` | This file, replacing root README | Created |
| All page screenshots | `docs/screenshots/` | Current frontend screenshots plus clearly labeled archived examples |
| System architecture | Sections 7–10, `docs/SYSTEM_DESIGN.md` | Documented |
| Core algorithms | Sections 8, 9, 19 | Documented |
| Security design/permission tiers | Sections 21–22, `docs/SECURITY_SELF_ASSESSMENT.md` | Documented; known gaps remain |
| Test cases and executable tests | `tests/`, Section 20, `evidence/` | Included; live integration requires independent check |
| Live website URL | https://studentbridge-ai-3.onrender.com/ | Reachable at documentation review; test again before submission |
| GitHub repository | https://github.com/Takbir-Al-Tanim/StudentBridge-AI | Repository address supplied; confirm final files pushed |
| Deployment instructions | Sections 13–17 | Included |
| Presentation deck ≤10 minutes | `docs/submission/` | Bundled presentation; rehearse/check latest deck |
| Optional demo video ≤5 minutes | Produce a short screen recording if desired | Needs team recording |
| Execution evidence for Topic C | `evidence/` + fresh sandbox log/recording | Synthetic example included; actual deployed evidence must be created |
| Originality + third-party licenses | `docs/ORIGINALITY_AND_LICENSES.md`, `docs/THIRD_PARTY_REVIEW.md` | Team must finish permission review |
| Submission deadline | 20 Oct 2026, 23:59 Beijing / 21:59 Bangladesh | Organizer-controlled |

### 26.2 Final steps before giving the repository to judges

1. Replace the repository-root `README.md` with this one and include the entire `docs/screenshots/` folder.
2. Check the site at **https://studentbridge-ai-3.onrender.com/** from another device and test the `/api/health` endpoint.
3. Confirm all sidebar pages, profile demo, beneficiary selection, Send Money steps, invoice review, simple route comparison and simulated tuition payment actually work.
4. Use fake identities and fake account data. Never display a database password, private `.env`, payment card details, genuine invoice or service key in the demo.
5. Run the automated tests and confirm the current Render/MySQL environment separately.
6. Review all open-source/dependency licenses and research-data redistribution permissions. Preserve notices where required.
7. Include architecture, permission tiers, known risks, test cases and **sandbox execution logs**. Clearly distinguish simulated evidence from real-money transfer.
8. Ensure presentation is no more than 10 minutes; optional demo video is no more than 5 minutes.
9. Push the final source to GitHub, let Render redeploy, and verify the commit and frontend assets match the screenshots.
10. Submit before the official deadline and review the official Competition Rules and Privacy Policy.

### 26.3 Important URLs

| Resource | Link |
|---|---|
| Live StudentBridge AI website | https://studentbridge-ai-3.onrender.com/ |
| GitHub source repository | https://github.com/Takbir-Al-Tanim/StudentBridge-AI |
| Hosted API reference | https://studentbridge-ai-3.onrender.com/docs |
| Hosted health check | https://studentbridge-ai-3.onrender.com/api/health |
| Local website | http://127.0.0.1:8000 |
| Local API documentation | http://127.0.0.1:8000/docs |
| Official competition website | https://fintechathon.g-ican.com/ |
| Render | https://dashboard.render.com/ |
| Aiven | https://console.aiven.io/ |
| Railway | https://railway.com/dashboard |
| Frankfurter reference FX | https://frankfurter.dev/ |

---

## Final note

**StudentBridge AI** brings tuition planning, explained reference rates, beneficiary review, modeled transfer route choices, living-cost protection, country-level credit readiness and sandbox testing into one interface. The core project goal is to make a complex student-finance decision **understandable and auditable** without claiming financial capabilities that have not been implemented.

**Built for Topic C: Cross-border & Student Finance Assistant.**
