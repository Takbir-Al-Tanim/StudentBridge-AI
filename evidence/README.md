# MySQL sandbox evidence

Run `python scripts/seed_sandbox.py` with a dedicated **non-production MySQL database** to generate `mysql_sandbox_example.json` from two explicitly hypothetical quotes. This is not evidence of a bank transfer and does not use real money. The archived `examples/old_SQLite_sample_evidence.json` comes from the previous SQLite edition; do NOT present it as new MySQL evidence.

Use `GET /api/audit/verify` for a hash-chain integrity check after recording the new demo. Human approval in this application is a shared-demo action only: there is NO user login or identity check; do not expose publicly as a real finance platform.
