from uuid import uuid4
from fastapi import FastAPI,Depends,Header,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from .database import get_db
from .models import Card,Transaction
from .schemas import PaymentRequest,PaymentResponse
from .security import current_user_id
from .services import simulate_payment
app=FastAPI(title="Credit Card Payment Service",version="1.0.0",description="Demo simulator only; no real authorization or money movement.")
@app.get("/health",tags=["operations"])
def health(): return {"status":"ok","service":"payment-simulator","mode":"simulation"}
@app.post("/api/payments/",response_model=PaymentResponse,status_code=201,tags=["payments"])
def create_payment(payload:PaymentRequest,idempotency_key:str=Header(alias="Idempotency-Key",min_length=8,max_length=128),user_id:int=Depends(current_user_id),db:Session=Depends(get_db)):
 existing=db.scalar(select(Transaction).where(Transaction.user_id==user_id,Transaction.idempotency_key==idempotency_key))
 if existing:
  if existing.card_id!=payload.card_id or existing.amount!=payload.amount or existing.currency!=payload.currency: raise HTTPException(409,"Idempotency-Key reused with different request")
  return PaymentResponse(transaction_id=existing.public_transaction_id,status=existing.status,amount=existing.amount,currency=existing.currency,message="Existing idempotent payment result")
 card=db.scalar(select(Card).where(Card.id==payload.card_id,Card.user_id==user_id,Card.is_active.is_(True)))
 if not card: raise HTTPException(404,"Active card reference not found")
 tx=Transaction(public_transaction_id="txn_"+uuid4().hex,user_id=user_id,card_id=card.id,amount=payload.amount,currency=payload.currency,status="PENDING",description=payload.description,idempotency_key=idempotency_key,failure_reason="")
 db.add(tx)
 try:
  db.commit(); db.refresh(tx)
 except IntegrityError:
  db.rollback()
  existing=db.scalar(select(Transaction).where(Transaction.user_id==user_id,Transaction.idempotency_key==idempotency_key))
  if existing: return PaymentResponse(transaction_id=existing.public_transaction_id,status=existing.status,amount=existing.amount,currency=existing.currency,message="Existing idempotent payment result")
  raise HTTPException(409,"Could not create payment; retry with a new key")
 tx.status,tx.failure_reason=simulate_payment(idempotency_key); db.commit(); db.refresh(tx)
 return PaymentResponse(transaction_id=tx.public_transaction_id,status=tx.status,amount=tx.amount,currency=tx.currency,message="Simulated payment completed" if tx.status=="SUCCESS" else "Simulated payment failed")
@app.get("/api/payments/{transaction_id}/",tags=["payments"])
def get_payment(transaction_id:str,user_id:int=Depends(current_user_id),db:Session=Depends(get_db)):
 tx=db.scalar(select(Transaction).where(Transaction.public_transaction_id==transaction_id,Transaction.user_id==user_id))
 if not tx: raise HTTPException(404,"Transaction not found")
 return {"transaction_id":tx.public_transaction_id,"status":tx.status,"amount":str(tx.amount),"currency":tx.currency,"description":tx.description,"failure_reason":tx.failure_reason,"created_at":tx.created_at.isoformat() if tx.created_at else None}
