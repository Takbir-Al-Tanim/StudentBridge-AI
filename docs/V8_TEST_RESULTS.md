# StudentBridge AI V8 — test verification

- **Automated tests:** 73 passed (`python -m pytest -q tests`) using a disposable SQLite database that does not contact production MySQL.
- **Python syntax:** compiled successfully (`python -m compileall -q app`).
- **JavaScript syntax:** passed (`node --check app/static/app.js`).
- **Browser interaction:** Chromium + Playwright with **mocked network responses**; Journey Studio navigation, initial catalog, five-step result rendering and three FX-shock cards tested; no JavaScript page exceptions.
- **Responsive:** 390 px mobile viewport showed no horizontal document overflow in the same mocked preview.
- **Visual previews:** `V8_Home_Desktop.png`, `V8_Journey_Desktop.png`, `V8_Journey_Result.png`, `V8_Mobile.png` are browser previews with stubbed financial API responses, **not a live provider quote**.
- **Security checks:** sandbox payment still requires explicit approval; the new journey endpoint does not execute any payment. Production history and audit endpoints return HTTP 403.
- **Licensing:** removed use of AGPL/commercial PyMuPDF; PDF text extraction uses BSD-3-Clause pypdf. See `ORIGINALITY_AND_LICENSES.md`.

**Not tested:** Actual Aiven connection, Render deployment, Stripe authorized checkout, Gemini API key quota, live Frankfurter API availability, OCR for scanned PDFs, per-user authentication. These require independent deployment tests and further implementation.
