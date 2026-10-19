# Review of the uploaded real financial data (15 October 2026)

## Decision
The dataset improves the existing project: four source-checked 2026/27 UCL tuition figures, official UK visa requirements, the 2023 Japanese student living-cost survey and rent breakdown, and official Korean tuition/living estimates. These have been integrated into the data catalog or research archive without treating a typical cost as an invoice amount.

## What was not promoted as a usable quote
- Seven `payment_quotes.csv` rows have **no provider, fee, FX rate, or quote validity**. They are unverified placeholders, not actionable payment quotes.
- `fx_rates.csv` provides **dated reference FX**, not executable bank offers; CNH is not CNY. Missing CNY/AUD and JPY/GBP observations remain NULL.
- The `20260422.pdf` University of Melbourne link for Supply Chain Management returned HTTP 404 when checked. It remains in the archived research files, **not** as a newly selectable tuition amount. The older catalog contains separate Melbourne programs with their own different cited values.
- China Ministry of Education general tuition range is historical, not a current institution-specific quotation. Korean national averages are statistics, not a particular student's tuition invoice.
- UK/Australia visa financial-capacity requirements are **not** actual monthly expenses.

## Repairs made
- Fixed extra CSV comma shifting `payment_quotes.csv` data into the wrong columns.
- Built `studentbridge_research.db` with all six data tables and verified foreign-key integrity.
- Exported a replacement `studentbridge_seed_database_fixed.sql` that imports without foreign-key errors.
- Added the available historical and country-specific numbers to the application's **Data & Sources** view and program catalog. Preserved all original uploads in `uploaded_originals/`.
- No live transfer rates were invented. Provider-quote inputs still require the user to provide the relevant transfer evidence.

## Core verification links
- UCL Computer Science 2026: https://www.ucl.ac.uk/prospective-students/undergraduate/degrees/computer-science-bsc-2026
- UCL MEng 2026: https://www.ucl.ac.uk/prospective-students/undergraduate/degrees/computer-science-meng-2026
- UCL Data Science 2026: https://www.ucl.ac.uk/prospective-students/undergraduate/degrees/data-science-bsc-2026
- UCL Philosophy and Computer Science 2026: https://www.ucl.ac.uk/prospective-students/undergraduate/degrees/philosophy-and-computer-science-ba-2026
- UK Government maintenance: https://www.gov.uk/student-visa/money
- Study in Japan/JASSO: https://www.studyinjapan.go.jp/en/life/cost-of-living/
- Study in Korea: https://studyinkorea.go.kr/ko/life/livingExpense.do
- Korea tuition statistics: https://studyinkorea.go.kr/ko/plan/abroadExpenses.do

**MySQL migration:** This corrected CSV data is imported with `scripts/setup_mysql.py`; see `docs/MYSQL_SETUP.md`. Legacy SQLite SQL is under `data/research/legacy_archive/` and must not be used for a MySQL import.
