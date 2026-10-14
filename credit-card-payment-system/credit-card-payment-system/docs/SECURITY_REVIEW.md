# Security Review

Safeguards included: Django password hashing, short-lived JWTs and refresh blacklist, owner-scoped resources, masked card metadata only, Decimal amounts, bounded amount/currency validation, idempotency key uniqueness, sanitized simulation errors, staff-only CSV export, environment-based configuration, Django throttling defaults.

Not production-certified: the simulator must be replaced by a PCI-compliant payment provider and verified webhooks/reconciliation. Add TLS, secret manager, separate least-privilege DB users, WAF/API gateway limits, production Django hardening, monitoring, dependency scanning, threat modeling, penetration testing, backup/restore drills, incident response, and operational reviews. Never store PAN/CVV.
