from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import BigInteger,String,Integer,Boolean,Numeric,DateTime


def utcnow_naive() -> datetime:
 return datetime.now(timezone.utc).replace(tzinfo=None)


class Base(DeclarativeBase): pass
class Card(Base):
 __tablename__="cards_card"
 id:Mapped[int]=mapped_column(BigInteger,primary_key=True)
 user_id:Mapped[int]=mapped_column(BigInteger,index=True)
 provider_token:Mapped[str]=mapped_column(String(255)); card_type:Mapped[str]=mapped_column(String(20))
 last4:Mapped[str]=mapped_column(String(4)); expiry_month:Mapped[int]=mapped_column(Integer); expiry_year:Mapped[int]=mapped_column(Integer)
 is_active:Mapped[bool]=mapped_column(Boolean); created_at:Mapped[datetime]=mapped_column(DateTime)
class Transaction(Base):
 __tablename__="transactions_transaction"
 id:Mapped[int]=mapped_column(BigInteger,primary_key=True)
 public_transaction_id:Mapped[str]=mapped_column(String(40),unique=True); user_id:Mapped[int]=mapped_column(BigInteger,index=True)
 card_id:Mapped[int|None]=mapped_column(BigInteger,nullable=True); amount:Mapped[object]=mapped_column(Numeric(12,2))
 currency:Mapped[str]=mapped_column(String(3)); status:Mapped[str]=mapped_column(String(10))
 description:Mapped[str]=mapped_column(String(255)); idempotency_key:Mapped[str]=mapped_column(String(128))
 failure_reason:Mapped[str]=mapped_column(String(100))
 created_at:Mapped[datetime]=mapped_column(DateTime,default=utcnow_naive)
 updated_at:Mapped[datetime]=mapped_column(DateTime,default=utcnow_naive,onupdate=utcnow_naive)
