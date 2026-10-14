from decimal import Decimal
from typing import Literal
from pydantic import BaseModel,Field,field_validator
class PaymentRequest(BaseModel):
 card_id:int=Field(gt=0)
 amount:Decimal=Field(gt=Decimal("0.00"),le=Decimal("1000000.00"),max_digits=12,decimal_places=2)
 currency:Literal["INR","USD","EUR"]="INR"
 description:str=Field(default="Demo purchase",max_length=255)
 @field_validator("amount")
 @classmethod
 def money(cls,value):
  if value.as_tuple().exponent < -2: raise ValueError("amount supports at most two decimal places")
  return value.quantize(Decimal("0.01"))
class PaymentResponse(BaseModel):
 transaction_id:str; status:Literal["PENDING","SUCCESS","FAILED"]; amount:Decimal; currency:str; message:str
