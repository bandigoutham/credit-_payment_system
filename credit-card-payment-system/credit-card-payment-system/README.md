# Credit Card Payment System

Django REST Framework + Simple JWT handles authentication, card references, transaction history, admin, and audit events. FastAPI handles simulated payments. MySQL is the shared database; **Django migrations own the schema**, while SQLAlchemy in FastAPI maps the existing tables.

## Safety
This is an educational payment simulator, not a real payment processor. It does not authorize cards or move money. Never store/send full card numbers or CVV. Use a PCI-compliant payment provider and tokenization for real payments.

## Features
- Register/login/refresh/logout/profile APIs with hashed passwords and JWT.
- Masked card references with ownership checks.
- Payment lifecycle `PENDING` → simulated `SUCCESS`/`FAILED`.
- Amount/currency validation, idempotency keys, transaction history filters.
- Staff-only CSV export and daily summary.
- Django admin, API docs, Postman collection, starter tests.

## Setup
Follow `RUN_COMMANDS.md` exactly. Copy `.env.example` to `.env`, set a strong secret and DB password, create the MySQL database/user, install each service's requirements, run `python manage.py makemigrations authentication cards transactions audit_logs` followed by `python manage.py migrate`, and run both services.

Django docs: `http://127.0.0.1:8000/api/docs/`; admin: `/admin/`.
FastAPI docs: `http://127.0.0.1:8001/docs`.

## Important production gaps
Before real deployment, integrate a PCI-compliant provider with verified webhooks/reconciliation, use TLS and a secret manager, separate least-privilege database users, configure production Django settings, add monitoring/alerting, security/load testing, dependency scanning, backup/restore drills, and a threat model. This project is not PCI certified or ready to process real payments.
