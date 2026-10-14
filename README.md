# credit-_payment_system
# 💳 Credit Card Payment System

A demonstration credit/debit card payment application built using **Django, Django REST Framework, FastAPI, and MySQL**. The project provides user authentication, card reference management, simulated payments, transaction history, and administrative functionality.

> **Note:** This project is for learning and demonstration purposes only. It does not process real payments or transfer real money.

## 🚀 Project Overview

The Credit Card Payment System uses Django to manage user authentication, saved card references, transaction history, and administration. FastAPI provides a separate service for simulating payment transactions.

The application uses JWT authentication to protect APIs and MySQL for relational data storage.

## 🎯 Objectives

- Implement user registration, login, logout, and JWT authentication.
- Add and manage saved card references securely.
- Simulate credit/debit card payments through FastAPI.
- Maintain transaction history and payment statuses.
- Prevent duplicate payment processing using idempotency keys.
- Provide administrative tools and transaction reporting.
- Document and test APIs using Swagger UI and Postman.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Authentication, card management, transactions, and administration |
| Django REST Framework | REST API development |
| Simple JWT | Token-based authentication |
| FastAPI | Simulated payment service |
| SQLAlchemy | ORM for the FastAPI service |
| MySQL | Relational database |
| Pydantic | Request and response validation |
| Swagger / OpenAPI | API documentation |
| Postman | API testing |
| pytest / Django TestCase | Automated testing |
| Git and GitHub | Version control and project hosting |

## ✨ Key Features

### 1. User Authentication
- User registration and login.
- JWT access and refresh tokens.
- Logout and refresh-token handling.
- Password hashing.
- Authentication-protected endpoints.

### 2. Card Management
- Add saved card references.
- View saved cards belonging to the authenticated user.
- Delete saved card references.
- Display masked card details.
- Enforce ownership restrictions.

### 3. Simulated Payment Processing
- Submit a payment request using a saved card reference.
- Validate payment amount and currency.
- Create and update transaction statuses.
- Support `PENDING`, `SUCCESS`, and `FAILED` statuses.
- Use idempotency keys to help prevent duplicate payment requests.
- Return transaction details and payment status.

### 4. Transaction Management
- View transaction history.
- Retrieve individual transaction details.
- Filter transactions by status, date, and amount.
- Support administrative CSV export where authorized.

### 5. Administration
- Manage users and review saved card references.
- View and filter transactions.
- Review audit logs.
- View daily payment totals and transaction counts.
- Export authorized transaction data.

## 🏗️ Architecture

The application separates user and transaction management from payment simulation.

```text
                    Client / Postman
                           |
             +-------------+-------------+
             |                           |
             v                           v
      Django REST API              FastAPI Service
         Port 8000                    Port 8001
             |                           |
             v                           v
      Authentication               Payment Simulation
      Card Management               Payment Validation
      Transaction History            Idempotency
      Admin and Audit                       |
             |                           |
             +-------------+-------------+
                           |
                           v
                         MySQL
```

Both services use MySQL. Shared tables must have consistent schemas and clearly defined migration ownership.

## 📁 Project Structure

```text
credit-card-payment-system/
├── django_backend/
│   ├── manage.py
│   ├── config/
│   ├── authentication/
│   ├── cards/
│   ├── transactions/
│   ├── audit_logs/
│   └── requirements.txt
├── fastapi_payment/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── security.py
│   │   └── services.py
│   └── requirements.txt
├── postman/
│   └── credit_card_payment_collection.json
├── .env.example
├── .gitignore
└── README.md
```

*The structure above describes the intended layout; keep it aligned with the actual files in your repository.*

## ⚙️ Prerequisites

Install the following before running the project:

- Python 3.11 or another version compatible with the project's dependencies.
- MySQL Server.
- Git.
- Postman (for API testing).

## 🔧 Installation and Setup

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd credit-card-payment-system
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your GitHub repository URL.

### Step 2: Configure MySQL

Log in to MySQL and create the database:

```sql
CREATE DATABASE credit_card_payment_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Create a dedicated database user and grant the required permissions according to your local environment.

### Step 3: Configure environment variables

Create a local `.env` file based on `.env.example`.

Example:

```dotenv
DJANGO_SECRET_KEY=replace-with-a-long-random-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=credit_card_payment_db
DB_USER=payment_app
DB_PASSWORD=your_local_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306

PAYMENT_SIMULATION_MODE=deterministic
PAYMENT_SUCCESS_RATE=0.85
```

Update the values to match your local configuration. Never commit your real `.env` file, passwords, JWTs, or other secrets to GitHub.

### Step 4: Set up Django

Open a terminal in the `django_backend` directory.

Create and activate a virtual environment if one does not already exist:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run database migrations:

```powershell
python manage.py migrate
```

Create an administrator account:

```powershell
python manage.py createsuperuser
```

Start the Django development server:

```powershell
python manage.py runserver 8000
```

### Step 5: Set up FastAPI

Open a separate terminal in the project root.

Create and activate the FastAPI virtual environment if needed:

```powershell
python -m venv .venv-fastapi
.\.venv-fastapi\Scripts\Activate.ps1
```

Install FastAPI dependencies:

```powershell
python -m pip install -r fastapi_payment/requirements.txt
```

Start the service:

```powershell
python -m uvicorn fastapi_payment.app.main:app --reload --port 8001
```

Run this command from the directory containing the `fastapi_payment` folder. If your dependency file or module path differs, adjust the command to match your repository.

## 🌐 API Documentation

Once the services are running, open the following URLs:

| Service | URL |
|---|---|
| Django development server | http://127.0.0.1:8000/ |
| Django Admin | http://127.0.0.1:8000/admin/ |
| FastAPI Swagger UI | http://127.0.0.1:8001/docs |
| FastAPI OpenAPI schema | http://127.0.0.1:8001/openapi.json |

Django API documentation is available only if a documentation route has been configured in the project.

## 🔑 API Endpoints

The following are the intended endpoint groups. Confirm the exact routes against the implementation before relying on them.

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register a user |
| POST | `/api/auth/login/` | Obtain JWT tokens |
| POST | `/api/auth/refresh/` | Refresh an access token |
| POST | `/api/auth/logout/` | Log out |
| GET | `/api/auth/me/` | Get the current user's profile |

### Card Management

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/cards/` | Add a card reference |
| GET | `/api/cards/` | List the current user's cards |
| DELETE | `/api/cards/{card_id}/` | Delete an owned card |

### Payment Processing

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/payments/` | Simulate a payment |
| GET | `/api/payments/{transaction_id}/` | Retrieve payment details |

### Transactions and Administration

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/transactions/` | View transaction history |
| GET | `/api/transactions/{transaction_id}/` | Retrieve a transaction |
| GET | `/api/admin/transactions/export.csv` | Export transactions, subject to admin permissions |

## 🧪 Sample Payment Request

Example JSON for a simulated payment:

```json
{
  "card_id": 1,
  "amount": "499.00",
  "currency": "INR",
  "description": "Online shopping"
}
```

Replace `card_id` with an existing saved card ID belonging to the authenticated user.

Include the appropriate authorization header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

For endpoints that require idempotency, include:

```text
Idempotency-Key: unique-payment-request-key
```

Reuse the same idempotency key when retrying the same payment. Generate a new key for a new payment.

Example simulated response:

```json
{
  "transaction_id": "txn_example_123",
  "status": "SUCCESS",
  "amount": "499.00",
  "currency": "INR",
  "message": "Simulated payment completed"
}
```

The exact response fields depend on the implemented API schemas. A simulated `SUCCESS` status does not represent a real bank authorization or settlement.

## 🧪 Testing

Run Django tests from the `django_backend` directory:

```powershell
python manage.py test
```

Run FastAPI tests if the test suite is configured:

```powershell
python -m pytest
```

For coverage reporting, if `coverage.py` is installed and configured:

```powershell
coverage run manage.py test
coverage report
```

The project task targets at least **50% test coverage** across the application. Measure both Django and FastAPI code before claiming that the target has been achieved.

## 🔐 Security Considerations

- Never store full card numbers or CVV.
- Use provider-issued tokens or safe test references.
- Hash passwords using Django's password hashers.
- Protect private APIs using JWT authentication.
- Verify card and transaction ownership on every user-facing operation.
- Store secrets in environment variables or a secret manager.
- Use decimal/fixed-precision values for monetary amounts.
- Validate all incoming request data.
- Use idempotency controls for payment retries.
- Avoid logging passwords, tokens, card details, or provider secrets.
- Restrict administrative actions to authorized staff.
- Use HTTPS and appropriate rate limiting outside local development.

## 📌 Current Project Status

This repository is intended to demonstrate a full-stack backend payment workflow using Django, FastAPI, and MySQL.

Before submitting the project, verify that:

- [ ] MySQL connections work for both services.
- [ ] Django migrations complete successfully.
- [ ] User registration and JWT login work.
- [ ] Card creation, listing, and deletion work.
- [ ] Simulated payments return the expected status.
- [ ] Idempotency prevents duplicate processing as intended.
- [ ] Transaction history and filters work.
- [ ] Admin permissions and CSV export work.
- [ ] API documentation is accessible.
- [ ] Automated tests pass and coverage has been measured.

## 🚧 Limitations

This is a demonstration application. It does not connect to a real bank, card network, or payment gateway. It must not be used to collect real cardholder data or process real money.

## 👩‍💻 Author

**BANDI GOUTHAM**

Full Stack Backend Project — Credit Card Payment System

## 📄 License

Add a license such as the MIT License if you intend to distribute the project under those terms.
