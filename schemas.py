# schemas.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PaymentMethodBase(BaseModel):
    card_last_four: str
    card_brand: str
    expiration_date: str
    is_default: bool

class PaymentMethodCreate(BaseModel):
    token: str

class PaymentMethodOut(PaymentMethodBase):
    id: int

class SubscriptionBase(BaseModel):
    tier: str
    is_active: bool
    next_billing_date: datetime

class SubscriptionCreate(BaseModel):
    tier: str

class SubscriptionOut(SubscriptionBase):
    id: int

class TransactionBase(BaseModel):
    amount: int
    currency: str
    status: str
    date: datetime

class TransactionOut(TransactionBase):
    id: int





# schemas.py
# from pydantic import BaseModel, EmailStr, constr
# from typing import Optional, List
# from datetime import datetime

# class PaymentMethodBase(BaseModel):
#     card_last4: str
#     card_brand: str
#     is_default: bool = False

# class PaymentMethodCreate(BaseModel):
#     # No raw card data; handled via QuickBooks tokenization
#     quickbooks_card_id: str

# class PaymentMethodOut(PaymentMethodBase):
#     id: int
#     created_at: datetime

#     class Config:
#         orm_mode = True

# class SubscriptionBase(BaseModel):
#     tier: str

# class SubscriptionCreate(SubscriptionBase):
#     payment_method_id: int

# class SubscriptionOut(SubscriptionBase):
#     id: int
#     status: str
#     start_date: datetime
#     next_billing_date: datetime
#     payment_method: PaymentMethodOut

#     class Config:
#         orm_mode = True

# class TransactionOut(BaseModel):
#     id: int
#     amount: float
#     currency: str
#     status: str
#     transaction_id: str
#     created_at: datetime

#     class Config:
#         orm_mode = True

# class UserOut(BaseModel):
#     id: int
#     email: EmailStr
#     name: str

#     class Config:
#         orm_mode = True

# class Token(BaseModel):
#     access_token: str
#     token_type: str