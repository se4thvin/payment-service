from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

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

# models.py
# from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.sql import func

# Base = declarative_base()
# #Assuming we import user from the user auth service here
# class PaymentMethod(Base):
#     __tablename__ = "payment_methods"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     quickbooks_card_id = Column(String, unique=True, index=True)  # From QuickBooks
#     card_last4 = Column(String(4))
#     card_brand = Column(String)
#     is_default = Column(Boolean, default=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())

#     user = relationship("User", back_populates="payment_methods")

# class Subscription(Base):
#     __tablename__ = "subscriptions"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     tier = Column(String)  # e.g., 'Basic', 'Pro', 'Enterprise'
#     status = Column(String, default="active")  # active, canceled, etc.
#     payment_method_id = Column(Integer, ForeignKey('payment_methods.id'))
#     start_date = Column(DateTime(timezone=True), server_default=func.now())
#     next_billing_date = Column(DateTime(timezone=True))
#     created_at = Column(DateTime(timezone=True), server_default=func.now())

#     user = relationship("User", back_populates="subscriptions")
#     payment_method = relationship("PaymentMethod")

# class Transaction(Base):
#     __tablename__ = "transactions"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     subscription_id = Column(Integer, ForeignKey('subscriptions.id'), nullable=True)
#     amount = Column(Float)
#     currency = Column(String, default="USD")
#     status = Column(String)  # authorized, captured, refunded, etc.
#     transaction_id = Column(String, unique=True, index=True)  # QuickBooks transaction ID
#     created_at = Column(DateTime(timezone=True), server_default=func.now())

#     user = relationship("User")
#     subscription = relationship("Subscription")