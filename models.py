from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timedelta

class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    token = Column(String, unique=True)
    card_last_four = Column(String(4))
    card_brand = Column(String)
    expiration_date = Column(String)
    is_default = Column(Boolean, default=False)

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    tier = Column(String)
    is_active = Column(Boolean, default=True)
    next_billing_date = Column(DateTime)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    amount = Column(Integer)
    currency = Column(String, default='USD')
    status = Column(String)
    date = Column(DateTime, default=func.now())
    transaction_id = Column(String, nullable=True)

class OAuthToken(Base):
    __tablename__ = 'oauth_tokens'

    id = Column(Integer, primary_key=True)
    access_token = Column(String)
    refresh_token = Column(String)
    realm_id = Column(String)
    expires_in = Column(Integer)
    x_refresh_token_expires_in = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    @property
    def access_token_expiry(self):
        return self.created_at + timedelta(seconds=self.expires_in)

    @property
    def refresh_token_expiry(self):
        return self.created_at + timedelta(seconds=self.x_refresh_token_expires_in)