# schemas.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PaymentMethodBase(BaseModel):
    card_last_four: str
    card_brand: str
    expiration_date: str
    is_default: bool

class PaymentMethodCreate(BaseModel):
    token: str  # Tokenized card data

class PaymentMethodOut(PaymentMethodBase):
    id: int

    class Config:
        orm_mode = True

class SubscriptionBase(BaseModel):
    tier: str
    is_active: bool
    next_billing_date: datetime

class SubscriptionCreate(BaseModel):
    tier: str
    payment_method_id: int

class SubscriptionOut(SubscriptionBase):
    id: int

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    amount: int
    currency: str
    status: str
    date: datetime
    transaction_id: Optional[str]

class TransactionOut(TransactionBase):
    id: int

    class Config:
        orm_mode = True