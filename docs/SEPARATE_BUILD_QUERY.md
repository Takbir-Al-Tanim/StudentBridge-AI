# Separate Copy-Paste Query / Build Brief

Use this as a separate query in your preferred coding assistant or future ChatGPT session to extend StudentBridge AI:

> Continue developing StudentBridge AI for the 2026 FinTechathon International Track, Topic C: Cross-border & Student Finance Assistant. Read the repository architecture and competition rules first. The system supports China, UK, Japan, South Korea, Australia and Bangladesh as *both* sending and destination countries (30 ordered combinations), not just Bangladesh outward remittances. Keep the premium responsive interface and working FastAPI APIs. Upgrade the invoice parser, integrate **authenticated real quote APIs only where explicitly supported**, review corridor compliance with primary sources, implement user authentication and per-user roles, improve verifiable invoice data extraction, make all calculations deterministic with Decimal, preserve the Digital Twin, Decision Passport, permission-guarded sandbox and audit logging. Every external datum must show the source, effective date, currency direction and trust status. Never invent real bank fees, unsupported corridors, scholarship awards or payment execution. Add tests and documentation whenever features are added. Explicitly distinguish finished code, user-entered estimates, external official data and simulation. Follow the competition weights: 40% task completion, 30% security/compliance, 30% innovation/interaction. Provide code **inline in copyable cells when asked** and also patch the repository.

For specific next tasks, ask:

1. "Implement official 2026 programme-specific tuition collectors for all six countries and update source provenance."
2. "Add a provider quote verification interface for Japan → UK, with expiry and required data validation."
3. "Make the app production-ready: auth, privacy, cross-user isolation, encryption, rate limits, testing and threat modeling."
4. "Create a controlled research benchmark comparing cost-only selection, deadline-aware selection, and the full EduRoute algorithm."

**Database requirement:** Use MySQL 8/InnoDB through SQLAlchemy and PyMySQL, with `DATABASE_URL` and a corrected CSV research seed. Plan and audit writes must be atomic, idempotency keys unique, and source values NULL when not verified. Do not use an SQLite runtime database.
