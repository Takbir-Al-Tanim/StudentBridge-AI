-- MySQL 8 research & sandbox queries. Run after setting up studentbridge_ai.
USE studentbridge_ai;
SELECT * FROM countries ORDER BY country_name;
SELECT * FROM financial_benchmarks WHERE country_code='JP';
SELECT t.institution,t.program,t.amount,t.currency_code,s.source_url
FROM tuition_benchmarks t LEFT JOIN sources s ON t.source_id=s.source_id;
SELECT origin_country_code,destination_country_code,verification_status FROM payment_quotes;
SELECT id,plan_id,status,approved_amount,currency FROM transactions ORDER BY created_at DESC LIMIT 30;
SELECT event_type,object_id,previous_hash,event_hash FROM audit ORDER BY id DESC LIMIT 50;
SELECT a.country_code AS origin,b.country_code AS destination FROM countries a
CROSS JOIN countries b WHERE a.country_code<>b.country_code;
