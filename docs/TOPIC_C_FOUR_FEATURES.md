# Topic C: four competition features (V7)

| Requirement | Website page | Functional evidence | Limitations |
|---|---|---|---|
| Remittances | Send money | Any ordered pair of 6 countries; live published reference rate; optional bank fee and markup; estimation with source date | Not a provider quote or a transfer order |
| Tuition payments | Tuition payments + Compare payment routes | Invoice reading, fee data, payment planning, review, receipt, separate provider-hosted card checkout | Provider checkout requires authorized merchant; practice receipts cannot settle tuition |
| Credit building | Build credit | Official-source guidance by destination; clickable 4-step student checklist | No actual credit report or product underwriting |
| Multi-currency management | My currencies | User-entered balances in 6 currencies converted to one target with observation dates; missing FX shown openly | No bank integration, no persistence of balances |

Other innovations: Financial Digital Twin (what-if scenarios), EduRoute decision engine (budget/deadline/provider eligibility), Decision Passport (calculations and sources), HMAC audit.

Data: existing 2026 tuition, country benchmarks and verified reference-rate sources. Published FX rates are used only for estimates, not executable prices.

Evaluation path: test each feature; document missing official data; check all six countries in UI and the 30 ordered pairs. Never represent the 30 pairs as 30 provider-verified transfer services.
