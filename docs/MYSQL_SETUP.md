## If you already use XAMPP and your MySQL connection works

**Skip the database-creation and research-seed steps below.** This UI/assistant update
requires **no SQL migration**. Your existing `studentbridge_ai` tables and records are
unchanged. Keep your current `.env` privately and copy it into the new extracted folder.
Then install requirements, run `python scripts/check_mysql.py`, and `python run.py`.

XAMPP typically provides MariaDB 10.4, which has been used successfully with the previous
10-table structure. Your database port/credentials remain whatever already works in your `.env`.
Do not repeat `mysql_research_seed.sql` without a specific reason.

---

# MySQL 8 Setup for StudentBridge AI (Mac / Windows / Linux)

The application now uses **MySQL 8.0+** for **all persistent application and research records**. It does not use an on-disk SQLite database in normal operation. SQLite is used only by disposable automated unit tests, never for deployment. Official sources and design catalog remain in read-only JSON/CSV files as an offline reference; the corrected six-country financial research seed is also imported to MySQL.

## Step 1: Install MySQL and create the database

Use MySQL Community Server 8.x / MySQL Workbench, a MySQL 8.4 Docker container, or managed MySQL (Railway/Aiven/etc.). Keep the database private; never expose port 3306 to the public Internet.

Run in MySQL Workbench with an administrator account (replace both placeholders):

```sql
CREATE DATABASE IF NOT EXISTS studentbridge_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'studentbridge_app'@'localhost' IDENTIFIED BY 'REPLACE_WITH_A_LONG_PRIVATE_PASSWORD';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX, REFERENCES
ON studentbridge_ai.* TO 'studentbridge_app'@'localhost';
```

For a Docker-based local DB, you can instead set `MYSQL_ROOT_PASSWORD` and `MYSQL_APP_PASSWORD` in your private `.env`, run `docker compose up -d mysql`, and use the automatically created user and database. NOTE: `.env.example` contains the Python DATABASE_URL settings and should be copied to `.env` first.

If the application runs on a different server, its MySQL user host must match the deployed environment. Prefer the host's managed MySQL connection configuration and TLS rather than allowing anonymous/public access.

## Step 2: Install Python requirements

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell activation is `.venv\Scripts\Activate.ps1`.

## Step 3: Configure .env

```bash
cp .env.example .env
```

Change the URL to the MySQL host, port, user, password and database name. Example:

```env
DATABASE_URL=mysql+pymysql://studentbridge_app:YOUR_URL_ENCODED_PASSWORD@127.0.0.1:3306/studentbridge_ai?charset=utf8mb4
APP_ENV=development
APP_SECRET=CHOOSE_A_RANDOM_32_CHARACTER_OR_LONGER_SECRET
```

If your password contains `@`, `:`, `/`, `#`, `%`, or spaces, URL-encode those characters in DATABASE_URL. Never commit `.env` or credentials to GitHub. Use a unique MySQL login with limited privileges and set secure secret values for deployment. The app loads `.env` automatically using python-dotenv.

## Step 4: Initialize and import verified research rows

```bash
python scripts/setup_mysql.py
```

This creates 10 tables (4 operational/audit and 6 research tables) and imports the corrected CSV records without filling missing payment quotes. It uses an upsert for existing research IDs and never deletes saved plans or transactions. A *fresh* app startup also imports the research CSVs automatically when the country table is empty.

Alternative manual SQL import in MySQL Workbench: run `scripts/mysql_schema.sql` followed by `scripts/mysql_research_seed.sql`. The SQL seed is **INSERT IGNORE**, so it preserves existing rows; use the Python importer to update research rows by ID.

## Step 5: Run and verify

```bash
python scripts/check_mysql.py
python run.py
```

Visit `http://127.0.0.1:8000`. Visit `http://127.0.0.1:8000/api/health` to confirm the `database_engine` field is `mysql`.

For an actual **write/read MySQL integration check** (use a disposable MySQL database):

```bash
MYSQL_SMOKE_TEST=YES python scripts/smoke_test_mysql.py
```

This creates one clearly labeled synthetic plan and simulated transaction and tests replay protection. Never run against production.

For full sandbox evidence (non-production test DB only), run:

```bash
python scripts/seed_sandbox.py
```

This creates an example `evidence/mysql_sandbox_example.json` from obviously hypothetical student/payment inputs. It is NOT a real provider quote and does NOT move money.

## Step 6: Tests and deployment

```bash
python -m pytest -q
```

Unit and API tests deliberately run with a new disposable test-only SQLite database, so they **do not prove a real MySQL service is available**. Use `python scripts/check_mysql.py` and a real web-app walkthrough against a separate MySQL test database for MySQL integration testing. Never use production data in integration tests.

For deployment use a service that can host Python FastAPI and a managed MySQL 8 database, with a private connection and automatic backups. **Netlify cannot run the Python backend and MySQL itself**; hosting the current app (HTML served directly by FastAPI) as a single backend app is simpler than splitting the frontend. This prototype has NO user login/role isolation and MUST NOT be publicly deployed with real financial or personally identifying data. Add authentication, session isolation, TLS, rate limits, and privacy controls before real users.

## Known limitations

- No provider-specific verified real payment quotes for arbitrary pairs; user-entered quote claims are NOT independently verified.
- No live bank integration; the payment ledger is sandbox only.
- Country-specific regulations are informational, not official compliance verification.
- Existing generated historical evidence from the SQLite version is labeled legacy and is NOT evidence of a new MySQL run.
- Financial data provenance, collection dates and NULL missing values are preserved in imported research tables.
