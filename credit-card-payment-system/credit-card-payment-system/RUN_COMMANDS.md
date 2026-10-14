# Run Commands

## 1. Create MySQL database (run in MySQL Workbench/CLI)
```sql
CREATE DATABASE credit_card_payment_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'payment_app'@'localhost' IDENTIFIED BY 'replace-with-strong-password';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX ON credit_card_payment_db.* TO 'payment_app'@'localhost';
FLUSH PRIVILEGES;
```
Update `.env` with the same password.

## 2. Configure environment
PowerShell: `Copy-Item .env.example .env` then edit `.env`.
macOS/Linux: `cp .env.example .env` then edit `.env`.

## 3. Django — Terminal 1, from project root
Windows PowerShell:
```powershell
cd django_backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py check
python manage.py makemigrations authentication cards transactions audit_logs
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```
macOS/Linux:
```bash
cd django_backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py check
python manage.py makemigrations authentication cards transactions audit_logs
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

## 4. FastAPI — open a second terminal at project root
Windows PowerShell:
```powershell
py -3.11 -m venv .venv-fastapi
.\.venv-fastapi\Scripts\Activate.ps1
pip install -r fastapi_payment/requirements.txt
uvicorn fastapi_payment.app.main:app --reload --port 8001
```
macOS/Linux:
```bash
python3.11 -m venv .venv-fastapi
source .venv-fastapi/bin/activate
pip install -r fastapi_payment/requirements.txt
uvicorn fastapi_payment.app.main:app --reload --port 8001
```

## 5. URLs
- Django API docs: http://127.0.0.1:8000/api/docs/
- Django admin: http://127.0.0.1:8000/admin/
- FastAPI Swagger: http://127.0.0.1:8001/docs
- FastAPI health: http://127.0.0.1:8001/health

## 6. First API flow
Register `POST /api/auth/register/` with:
```json
{"username":"demo_user","email":"demo@example.com","password":"Strong-Local-Password-123!"}
```
Login `POST /api/auth/login/`, copy `access` token, then add a card at `POST /api/cards/`:
```json
{"card_type":"VISA","last4":"1234","expiry_month":12,"expiry_year":2028,"provider_token":"demo-token-abc"}
```
Simulate payment at FastAPI `POST /api/payments/`, with `Authorization: Bearer YOUR_ACCESS_TOKEN` and `Idempotency-Key: demo-payment-0001`:
```json
{"card_id":1,"amount":"499.00","currency":"INR","description":"Demo purchase"}
```

For the FastAPI Swagger UI, first click **Authorize** and enter the access token returned by Django's `POST http://127.0.0.1:8000/api/auth/login/` request (without the `Bearer ` prefix). Then retry the payment request. Or use PowerShell, replacing the placeholder with the Django access token:
```powershell
curl.exe -X POST http://127.0.0.1:8001/api/payments/ `
  -H "Authorization: Bearer YOUR_DJANGO_ACCESS_TOKEN" `
  -H "Idempotency-Key: demo-payment-0001" `
  -H "Content-Type: application/json" `
  -d '{"card_id":1,"amount":"499.00","currency":"INR","description":"Demo purchase"}'
```

## 7. Tests
From `django_backend/`: `python manage.py test` and `coverage run manage.py test`.
From project root with FastAPI environment active: `pytest`.

Keep both servers running in separate terminals. Ctrl+C stops a server.
