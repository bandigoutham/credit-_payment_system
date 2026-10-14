import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[2]/".env")
SECRET_KEY=os.environ.get("DJANGO_SECRET_KEY","unsafe-local-key-change-me")
DB_NAME=os.environ.get("DB_NAME","credit_card_payment_db"); DB_USER=os.environ.get("DB_USER","payment_app")
DB_PASSWORD=os.environ.get("DB_PASSWORD",""); DB_HOST=os.environ.get("DB_HOST","127.0.0.1"); DB_PORT=os.environ.get("DB_PORT","3306")
SIMULATION_MODE=os.environ.get("PAYMENT_SIMULATION_MODE","deterministic")
SUCCESS_RATE=float(os.environ.get("PAYMENT_SUCCESS_RATE","0.85"))
