from fastapi_payment.app.services import simulate_payment
def test_simulator_returns_supported_status():
 status,reason=simulate_payment("unit-test-idempotency-key")
 assert status in {"SUCCESS","FAILED"}
 assert (reason=="") if status=="SUCCESS" else (reason=="SIMULATED_DECLINE")
