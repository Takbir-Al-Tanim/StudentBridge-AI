PRAGMA foreign_keys = ON;
CREATE TABLE countries(country_code TEXT PRIMARY KEY, country_name TEXT NOT NULL, currency_code TEXT, currency_name TEXT, data_status TEXT NOT NULL, notes TEXT);
CREATE TABLE sources(source_id INTEGER PRIMARY KEY, publisher TEXT NOT NULL, title TEXT NOT NULL, source_url TEXT NOT NULL, source_type TEXT NOT NULL, published_or_updated_date TEXT, collection_date TEXT NOT NULL, notes TEXT);
CREATE TABLE financial_benchmarks(benchmark_id INTEGER PRIMARY KEY, country_code TEXT NOT NULL REFERENCES countries(country_code), benchmark_type TEXT NOT NULL, context TEXT NOT NULL, amount NUMERIC, currency_code TEXT, unit TEXT, period TEXT, geography TEXT, reference_date TEXT, source_id INTEGER REFERENCES sources(source_id), verification_status TEXT NOT NULL, notes TEXT);
CREATE TABLE tuition_benchmarks(tuition_id INTEGER PRIMARY KEY, country_code TEXT NOT NULL REFERENCES countries(country_code), institution TEXT, program TEXT NOT NULL, level TEXT, student_type TEXT, amount NUMERIC, currency_code TEXT, fee_basis TEXT, academic_year TEXT, source_id INTEGER REFERENCES sources(source_id), verification_status TEXT NOT NULL, notes TEXT);
CREATE TABLE fx_rates(fx_id INTEGER PRIMARY KEY, base_currency TEXT NOT NULL, quote_currency TEXT NOT NULL, rate NUMERIC, rate_date TEXT, rate_type TEXT, source_id INTEGER REFERENCES sources(source_id), verification_status TEXT NOT NULL, notes TEXT);
CREATE TABLE payment_quotes(quote_id INTEGER PRIMARY KEY, origin_country_code TEXT NOT NULL REFERENCES countries(country_code), destination_country_code TEXT NOT NULL REFERENCES countries(country_code), provider_name TEXT, origin_currency TEXT, destination_currency TEXT, send_amount NUMERIC, receive_amount NUMERIC, fee_amount NUMERIC, fee_currency TEXT, quoted_fx_rate NUMERIC, delivery_time TEXT, quote_timestamp TEXT, quote_expiry TEXT, source_url TEXT, verification_status TEXT NOT NULL, notes TEXT);


-- Seed data collected on 2026-10-15. NULL means missing/unverified, never zero.

INSERT INTO countries (country_code,country_name,currency_code,currency_name,data_status,notes) VALUES
('CN','China','CNY','Chinese yuan','partial','Historical tuition reference only; current national living-cost benchmark not verified.'),
('GB','United Kingdom','GBP','Pound sterling','partial','Official visa maintenance values and a course-specific tuition value included.'),
('JP','Japan','JPY','Japanese yen','partial','JASSO living-cost data are from the 2023 survey.'),
('KR','South Korea','KRW','South Korean won','partial','Official portal tuition and living-cost estimates included.'),
('AU','Australia','AUD','Australian dollar','partial','Official visa financial-capacity requirement and one course fee included.'),
('BD','Bangladesh','BDT','Bangladeshi taka','partial','Official central-bank FX reference values included; national student living-cost benchmark not verified.');

INSERT INTO sources (source_id,publisher,title,source_url,source_type,published_or_updated_date,collection_date,notes) VALUES
(1,'Bangladesh Bank','FX Rate Sheet effective for 14 October 2026','https://www.bb.org.bd/en/index.php/econdata/exchangerate','central_bank_fx','2026-10-14','2026-10-15','Reference cross-rates, not consumer transfer quotes.'),
(2,'GOV.UK / UK Visas and Immigration','Student visa: Money you need','https://www.gov.uk/student-visa/money','visa_financial_requirement','updated 2025-12-31','2026-10-15','Visa evidence requirement, not actual spending.'),
(3,'Australian Department of Home Affairs','Subclass 500 Student visa','https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/student-500','visa_financial_requirement','current page as accessed','2026-10-15','Official financial-capacity requirement.'),
(4,'Study in Japan / JASSO','Living Costs and Expenses','https://www.studyinjapan.go.jp/en/life/cost-of-living/','student_living_cost_survey','2023 survey','2026-10-15','Monthly estimates from 2023 survey.'),
(5,'Study in Korea / Academy Info','Study Expenses in Korea','https://studyinkorea.go.kr/ko/plan/abroadExpenses.do','tuition_statistics','current page as accessed','2026-10-15','Official portal averages; institution fees vary.'),
(6,'Study in Korea','Living Costs and Expenses','https://www.studyinkorea.go.kr/ko/life/livingExpense.do','student_living_cost_estimate','current page as accessed','2026-10-15','Official portal monthly estimates.'),
(7,'Ministry of Education of the People''s Republic of China','Application for Studying in China — Expenses','https://en.moe.gov.cn/cooperation_exchanges/201506/t20150626_191374.html','tuition_reference','historical page','2026-10-15','Official but old tuition ranges; not a current price quote.'),
(8,'University College London','Computer Science BSc 2026','https://www.ucl.ac.uk/prospective-students/undergraduate/degrees/computer-science-bsc-2026','institution_tuition_fee','2026/27 entry','2026-10-15','Overseas first-year course fee.'),
(9,'The University of Melbourne','2026 International Course Tuition Fees','https://students.unimelb.edu.au/__data/assets/pdf_file/0020/5423033/2026-International-Course-Tuition-Fees-OF_20260422.pdf','institution_tuition_fee','2026-04-22','2026-10-15','Master of Supply Chain Management fee per EFTSL.'),
(10,'Bank of Japan','Foreign Exchange Rates (Daily)','https://www.boj.or.jp/en/statistics/market/forex/fxdaily/index.htm','central_bank_fx','daily series','2026-10-15','Official daily rates page; direct JPY/GBP rate not seeded.');

INSERT INTO financial_benchmarks (benchmark_id,country_code,benchmark_type,context,amount,currency_code,unit,period,geography,reference_date,source_id,verification_status,notes) VALUES
(1,'GB','visa_maintenance_requirement','Student visa applicant; London',1529,'GBP','per_month','up to 9 months','London','','2','verified_official','Required funds, not actual monthly spending.'),
(2,'GB','visa_maintenance_requirement','Student visa applicant; outside London',1171,'GBP','per_month','up to 9 months','Outside London','','2','verified_official','Required funds, not actual monthly spending.'),
(3,'AU','visa_financial_capacity_requirement','Student visa applicant',29710,'AUD','per_12_months','12 months','Australia','','3','verified_official','Financial-capacity requirement, not actual spending.'),
(4,'JP','student_living_cost_estimate','Privately financed international students; excludes tuition',105000,'JPY','per_month','monthly','Japan national average','2023 survey','4','verified_official_historical','JASSO 2023 estimate; historical benchmark.'),
(5,'JP','student_rent_estimate','Privately financed international students',41000,'JPY','per_month','monthly','Japan national average','2023 survey','4','verified_official_historical','JASSO 2023 estimate.'),
(6,'JP','student_rent_estimate','Privately financed international students',57000,'JPY','per_month','monthly','Tokyo','2023 survey','4','verified_official_historical','JASSO 2023 estimate.'),
(7,'KR','student_living_cost_estimate_lower','International students',750000,'KRW','per_month','monthly','South Korea','','6','verified_official_estimate','Lower end of official approximate KRW 750,000–1,000,000 range.'),
(8,'KR','student_living_cost_estimate_upper','International students',1000000,'KRW','per_month','monthly','South Korea','','6','verified_official_estimate','Upper end of official approximate KRW 750,000–1,000,000 range.'),
(9,'CN','student_living_cost_estimate','International students; general',NULL,'CNY','per_month','monthly','China','','','missing_official_value','No current nationally applicable official value verified in this collection.'),
(10,'BD','student_living_cost_estimate','International students; general',NULL,'BDT','per_month','monthly','Bangladesh','','','missing_official_value','No current nationally applicable official value verified in this collection.');

INSERT INTO tuition_benchmarks (tuition_id,country_code,institution,program,level,student_type,amount,currency_code,fee_basis,academic_year,source_id,verification_status,notes) VALUES
(1,'CN','','Liberal arts undergraduate tuition (minimum of published range)','undergraduate','self-financed international students',14000,'CNY','per_academic_year','historical MOE reference','7','official_but_historical','Official page gives CNY 14,000–26,000/year; historical, not current pricing.'),
(2,'CN','','Liberal arts undergraduate tuition (maximum of published range)','undergraduate','self-financed international students',26000,'CNY','per_academic_year','historical MOE reference','7','official_but_historical','Official page gives CNY 14,000–26,000/year; historical, not current pricing.'),
(3,'KR','','Average annual university tuition','undergraduate','national average',6820243.8,'KRW','per_academic_year','current official portal page','5','verified_official_statistic','National average; not international-student-specific.'),
(4,'KR','','Average annual university tuition','undergraduate','national/public average',4265841.8,'KRW','per_academic_year','current official portal page','5','verified_official_statistic','National/public average.'),
(5,'KR','','Average annual university tuition','undergraduate','private average',7625335.6,'KRW','per_academic_year','current official portal page','5','verified_official_statistic','Private average.'),
(6,'KR','','Average annual graduate tuition','graduate','national average',4216103.2,'KRW','per_academic_year','current official portal page','5','verified_official_statistic','National average; verify individual university/program.'),
(7,'GB','University College London','Computer Science BSc','undergraduate','overseas',46700,'GBP','first_year_tuition','2026/27','8','verified_official_institution_fee','Course-specific fee; not a UK-wide average.'),
(8,'AU','The University of Melbourne','Master of Supply Chain Management','masters','international',32000,'AUD','per_EFTSL','2026','9','verified_official_institution_fee','Fee per EFTSL as listed in official 2026 schedule.');

INSERT INTO fx_rates (fx_id,base_currency,quote_currency,rate,rate_date,rate_type,source_id,verification_status,notes) VALUES
(1,'GBP','BDT',163.4634,'2026-10-14','Bangladesh Bank cross-rate; BDT per 1 GBP','1','verified_official_reference','Published bid-side cross-rate; not a remittance quote.'),
(2,'AUD','BDT',86.0983,'2026-10-14','Bangladesh Bank cross-rate; BDT per 1 AUD','1','verified_official_reference','Published bid-side cross-rate; not a remittance quote.'),
(3,'JPY','BDT',0.779,'2026-10-14','Bangladesh Bank cross-rate; BDT per 1 JPY','1','verified_official_reference','Published cross-rate; not a remittance quote.'),
(4,'CNH','BDT',18.4281,'2026-10-14','Bangladesh Bank cross-rate; BDT per 1 CNH','1','verified_official_reference','CNH is offshore yuan, not identical to onshore CNY.'),
(5,'KRW','BDT',NULL,'','required pair; value not verified','','missing_official_value','Do not infer or substitute an unverified rate.'),
(6,'CNY','AUD',NULL,'','StudentBridge demo corridor','','missing_official_value','No direct rate verified in this collection.'),
(7,'JPY','GBP',NULL,'','StudentBridge demo corridor','10','missing_official_value','No direct rate verified in this collection.');

INSERT INTO payment_quotes (quote_id,origin_country_code,destination_country_code,provider_name,origin_currency,destination_currency,send_amount,receive_amount,fee_amount,fee_currency,quoted_fx_rate,delivery_time,quote_timestamp,quote_expiry,source_url,verification_status,notes) VALUES
(1,'CN','AU','','CNY','AUD',NULL,NULL,NULL,'',NULL,'','','','','','unverified_quote_required','No provider-specific, timestamped CNY-to-AUD payout quote verified; route support must be confirmed.'),
(2,'JP','GB','','JPY','GBP',NULL,NULL,NULL,'',NULL,'','','','','','unverified_quote_required','No provider-specific, timestamped JPY-to-GBP payout quote verified; route support must be confirmed.'),
(3,'BD','GB','','BDT','GBP',NULL,NULL,NULL,'',NULL,'','','','','','unverified_quote_required','No provider-specific BDT-origin tuition transfer quote verified.'),
(4,'BD','AU','','BDT','AUD',NULL,NULL,NULL,'',NULL,'','','','','','unverified_quote_required','No provider-specific BDT-origin tuition transfer quote verified.'),
(5,'BD','JP','','BDT','JPY',NULL,NULL,NULL,'',NULL,'','','','','','unverified_quote_required','No provider-specific BDT-origin tuition transfer quote verified.'),
(6,'BD','KR','','BDT','KRW',NULL,NULL,NULL,'',NULL,'','','','','','unverified_quote_required','No provider-specific BDT-origin tuition transfer quote verified.'),
(7,'BD','CN','','BDT','CNY',NULL,NULL,NULL,'',NULL,'','','','','','unverified_quote_required','No provider-specific BDT-origin tuition transfer quote verified.');
