# Demo Payment Logic and Safety

The separate demo checkout exists so judges and students can experience a real website-style flow without real banking credentials.

**Input:** origin/destination among six countries; destination-currency tuition amount; origin-currency available balance; protected reserve; deadline; university; one origin-currency-per-destination-currency rate.

**FX provenance:** When available, `/api/fx` returns a server-signed, short-lived Frankfurter reference rate. `/api/demo/prepare` verifies the signature. A manually supplied rate is stored as `USER_ENTERED_DEMO_RATE`; both kinds are non-executable references.

**Fictional demonstration options:** Demo Bank Transfer (example 1% fee, 2 days), Demo Card Payment (example 1.8% fee, 0 days), Demo Student Transfer (example 0.6% fee, 4 days). THESE ARE NOT BANKS, VERIFIED FEES OR GUARANTEED TIMES. The server defines them; users cannot give normal quotes `simulation_only` bypass privileges.

**Calculations:** base cost = tuition due × chosen rate; sample fee = base cost × sample fee percentage; total amount = base cost + fee. Compare total with available balance − protected reserve, and sample ETA with days remaining until deadline. A demo option is disabled if either condition fails.

**Payment:** A valid stored plan, a viable chosen demo option, explicit confirmation and the exact approval phrase are required. MySQL records the sandbox transaction and HMAC-linked audit event in one database transaction. A unique idempotency key prevents repeat execution. No money leaves any bank account.

**Receipt:** `/api/sandbox/receipt/{transaction_id}` reconstructs an on-screen and downloadable test receipt using the stored transaction and original plan. It clearly says simulation-only.

**Data separation:** Real tuition and regulatory references remain in the research tables. Fictional demo methods live only in individual sandbox plans; they are not written as official payment quotes in research tables.
