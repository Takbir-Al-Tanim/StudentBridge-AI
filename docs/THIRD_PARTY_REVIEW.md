# Third-party source and license review register

This register documents due diligence. It is not a legal certification and cannot replace the original license/terms for each bundled source or resolved package version.

## Included or referenced materials

| Category | Materials | Action before public release |
|---|---|---|
| Application source and visual design | StudentBridge AI original frontend and backend implementation | Contestants confirm independent authorship and preserve commit history |
| Open-source Python packages | `requirements.txt` (`fastapi`, `uvicorn`, `httpx`, `pydantic`, `pypdf`, SQLAlchemy, `pymysql`, `python-dotenv`, `jinja2`, Stripe SDK, pytest, etc.) | Verify license terms for pinned installed versions; retain copyright/notice files when required |
| Third-party JSON and CSV data | `app/data/*.json`, `data/research/corrected/*.csv` | Verify accuracy, original publisher, update date and permission to redistribute individual data sets |
| Historical imported workbooks and archives | `data/research/uploaded_originals/` and `data/research/legacy_archive/` | **Not included in the public final submission package** pending team review of underlying permission; corrected runtime CSVs are retained |
| Frankfurter reference FX | `https://frankfurter.dev/` | Follow API usage and attribution terms; reference rate is not a bank quote |
| Country/university and regulatory facts | Public source registry links | Cite the publisher, do not reproduce unlicensed full texts, screenshots or trademarks |
| Google Gemini and optional Stripe | External services not bundled | Follow service and merchant terms; keep secrets out of source code |
| Screenshots | `docs/screenshots/` of **StudentBridge AI itself**, captured with mock test data | Not screenshots of competitor websites; no real customer data or settlement proof |
| Official competition rules | User-supplied PDF for reference | **Not included** in release package; consult controlling version from organizer's official site |

## Contestant sign-off

- [ ] Source code authorship reviewed by all team members.
- [ ] Original data and workbook permissions verified. Historical archives are excluded pending review.
- [ ] Exact installed package versions and license conditions checked; notices included if needed.
- [ ] Public repository and all Git history scanned for exposed secrets and unlicensed material.
- [ ] Public demo uses fictional data; no claim of real money, legal compliance or verified provider eligibility.

See `docs/ORIGINALITY_AND_LICENSES.md` for links to individual library licenses and further original-design information.
