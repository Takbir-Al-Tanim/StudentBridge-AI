# StudentBridge AI MySQL Edition — Test Report

Date: 15 October 2026. **32 automated unit/API/schema tests passed, 0 failed** in the isolated test suite. Test database: ephemeral SQLite under `STUDENTBRIDGE_TEST_MODE=1` only; the shipped runtime requires MySQL 8. MySQL schema compilation for all ten tables, data reimport idempotency and HMAC audit consistency are tested. A live MySQL server/driver was not available in the build environment, so an actual MySQL connection/integration test still needs to be run with `python scripts/check_mysql.py`, `MYSQL_SMOKE_TEST=YES python scripts/smoke_test_mysql.py` (dedicated test DB only) and a complete demo workflow against your MySQL deployment.

No real payment provider API, KYC, sanctions check or actual remittance is connected; user-submitted provider quotes are not independently verified.


## Version 3 validation (October 2026)

- **44 automated tests passed** in a disposable, isolated test SQLite database.
- Additional assistant tests cover country detection, cited tuition/living costs, credit
  guidance, missing real provider quotes, currency selection and Digital Twin calculations.
- JavaScript syntax check passed using `node --check`.
- Headless Chromium static desktop/mobile screenshots generated, with zero mobile overflow.
- Headless mock API interaction confirmed chat source links, next-step buttons, and
  navigation work without browser errors.
- A fresh live MariaDB/MySQL connection was not tested in the build container; run
  `python scripts/check_mysql.py` on your working XAMPP installation.
