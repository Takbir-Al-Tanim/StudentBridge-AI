# Real Financial Data Collection - Exact Instructions

## Scope and data status

Support country selection for China (CNY), United Kingdom (GBP), Japan (JPY), South Korea (KRW), Australia (AUD) and Bangladesh (BDT). There are 30 ordered directions, not 30 proven bank routes. All data must include source URLs, observation/effective dates and `source_type`. Missing data stays missing. Real student financial information requires consent, minimum necessary fields and secure treatment; none is bundled.

## 1. Live reference FX (six currencies)

**Source:** https://frankfurter.dev/ (v2). API example: `GET https://api.frankfurter.dev/v2/rate/JPY/GBP` returns a numerical rate and publication date, when available. The backend fetches only on demand; if internet is unreachable, it returns `available=false` with no invented rate.

**Fields:** `base_currency, quote_currency, published_rate, observation_date, retrieved_at, source_url, rate_type=market_reference`.

**Never:** call it a provider sell rate or guarantee that customers can transfer at that price.

## 2. Real 2026 university tuition

**Sources:**
- Australia (specific numeric data): https://students.unimelb.edu.au/__data/assets/pdf_file/0020/5423033/2026-International-Course-Tuition-Fees-OF_20260507.pdf
- United Kingdom: https://www.manchester.ac.uk/study/masters/courses/list//13005/ma-international-education/overview/ and https://www.ucl.ac.uk/prospective-students/graduate/taught-degrees/management-complex-projects-msc
- China: https://masters.sem.tsinghua.edu.cn/en/info/1007/2103.htm
- Japan: https://ipads.a.u-tokyo.ac.jp/admissions/cost-scholarship/ and https://www.s.u-tokyo.ac.jp/en/admission/research-students.html
- South Korea: https://ee.kaist.ac.kr/en/admission-08/
- Bangladesh: https://www.bracu.ac.bd/admissions/tuition-and-fees (per-credit published data; individual fee status matters).

**Fields:** `institution, country, programme, year, student_fee_status, tuition_amount, currency, payment_period, campus, source_url, updated_at, exact_invoice_confirmed`.

University-published annual/cost-per-EFTSL data must never be automatically confused with the student's actual payable invoice. The catalog now includes selected 2026 official published fee examples for all six countries; it always shows period, source and any student-status restrictions.

## 3. Bank and cross-border provider offers

**Source:** actual bank/provider customer quotation applicable to **the exact two countries and currency direction**. Ask the bank for documented tuition-purpose eligibility, payment method, signed/net beneficiary amount, quoted rate, flat fees, percentage fees, intermediary fees, cut-off time, expected settlement, quote expiry and beneficiary validation rules. A general price page is *not* a customer-specific quote.

**Fields:** `provider, source_country, destination_country, corridor_currency_pair, declared_eligibility, quote_rate, fixed_fee, percent_fee, correspondent_fees, beneficiary_deductions, expected_eta, quote_timestamp, expiry, reference_url_or_document_id, verification_status`.

**If missing:** `quote_unavailable`. Do not generate fictional "real" bank offers. Some information may require a licensed API, bank relationship, or logged-in customer account.

## 4. Regulatory references

Start from the official national regulators: China SAFE (`safe.gov.cn/en`), UK FCA (`fca.org.uk`), Japan FSA (`fsa.go.jp/en`), Korea FSC (`fsc.go.kr/eng/index`), Australia AUSTRAC (`austrac.gov.au`), Bangladesh Bank (`bb.org.bd`). These are *research starting points* rather than machine-readable verified eligibility for each route.

**Fields:** `origin, destination, type, relevant_entity, law_or_rule, allowed_conditions, document_checklist, applicable_thresholds, effective_date, source_url, reviewed_by, legal_review_status`.

The current system cannot assert that a cross-border transfer is legally compliant. Do not replace proper KYC/AML with a source URL.

## 5. Living costs and formal visa funds

**Real examples:** UK Student visa London GBP 1,529 per month / outside London GBP 1,171 per month up to 9 months, with applicable exceptions, from https://www.gov.uk/student-visa/money. JASSO Student Guide 2025-26: 2023 privately financed international student living costs JPY 105,000 monthly national average; source https://www.studyinjapan.go.jp/en/assets/pdf/sgtj_2025_english.pdf.

**Fields:** `country, city, amount, currency, month, category, scope, observation_year, publication_date, source_url, is_visa_rule`. Do not present visa bank-balance requirements as a guarantee of actual living affordability.

## 6. Credit readiness

Official/principal examples: UK MoneyHelper (`moneyhelper.org.uk`), Australian Government Moneysmart (`moneysmart.gov.au`), Japan CIC (`cic.co.jp/en/credit-report/`). Add China, South Korea and Bangladesh details only from verified local institutions. Store `country, consumer_action, document_requirement, eligibility_caveat, official_url, effective_date`.

Credit score prediction is out of scope. Do not invent students' private credit profiles.

## 7. Student-provided information

The user can enter destination university, confirmed tuition amount and deadline, scholarship already awarded, actual *self-reported* available money, protected reserve and living-expense estimates. The project does not request passwords, card PIN, OTP, government identifier, passport scan or real bank credentials. The sandbox DB must not be treated as secure storage for sensitive real data.

## 8. Practical collection order

**Day 1:** load FX API reference and 6-country catalog; collect a narrow set of university fees with original links. **Day 2:** enter bank/provider quotes for actual supported routes, explicitly recording gaps and confirming expiry. **Day 3:** map tuition document conditions and visa/living references. **Day 4:** review student credit guidance and build additional institution coverage. **Day 5:** revalidate source timestamps and run financial/error tests.

## 9. Provenance checklist

For each record ask: Is this a *primary* source? Is it applicable to 2026 and the intended customer? Is the value a price, an estimate, a statutory requirement, or a quote? Does it specify which way the currency converts? Is it available for the requested pair? Has it expired? Is any charge missing? Are there redistribution/licensing restrictions? If any answer is unknown, display a verification-needed label.
