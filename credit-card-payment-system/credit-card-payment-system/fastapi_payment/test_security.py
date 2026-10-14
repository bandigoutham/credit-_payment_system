from fastapi.testclient import TestClient

from fastapi_payment.app.main import app
from fastapi_payment.app.models import Transaction


def test_payment_requires_bearer_access_token():
    response = TestClient(app).post(
        "/api/payments/",
        headers={"Idempotency-Key": "payment-test-001"},
        json={
            "card_id": 1,
            "amount": 100,
            "currency": "INR",
            "description": "Demo purchase",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Bearer access token required"}


def test_openapi_documents_bearer_authentication():
    openapi = app.openapi()
    operation = openapi["paths"]["/api/payments/"]["post"]
    security_scheme = openapi["components"]["securitySchemes"]["HTTPBearer"]

    assert operation["security"] == [{"HTTPBearer": []}]
    assert security_scheme["type"] == "http"
    assert security_scheme["scheme"] == "bearer"


def test_transaction_timestamp_defaults_are_configured():
    created_at = Transaction.__table__.c.created_at.default
    updated_at = Transaction.__table__.c.updated_at.default

    assert created_at is not None
    assert callable(created_at.arg)
    assert updated_at is not None
    assert callable(updated_at.arg)
    assert callable(Transaction.__table__.c.updated_at.onupdate.arg)
