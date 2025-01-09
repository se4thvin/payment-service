# main.py

from fastapi import FastAPI, Depends, HTTPException, status
from . import models, schemas, crud, quickbooks_client
from .dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from datetime import datetime, timedelta
from fastapi import FastAPI
from scheduler import scheduler, start_scheduler
import asyncio
from routers.payment_methods import router as payment_methods_router
from routers.subscriptions import router as subscriptions_router
from routers.transactions import router as transactions_router

app = FastAPI(title="Payment Service")

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://localhost:3000",
        "http://coursebite.ai",
        "https://www.coursebite.ai",
        "https://coursebite.ai",
        "http://www.coursebite.ai",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize QuickBooks client
qb_client = quickbooks_client.QuickBooksClient()

# Include routers
app.include_router(payment_methods_router)
app.include_router(subscriptions_router)
app.include_router(transactions_router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# Endpoint to add a new payment method
@app.post("/payment-methods", response_model=schemas.PaymentMethodOut)
async def add_payment_method(
    payment_method: schemas.PaymentMethodCreate,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Ideally, the tokenization should happen on the frontend or via a secure process
    # Here, assume that 'quickbooks_card_id' is already obtained securely
    # For example purposes, we collect minimal info
    # In production, implement full tokenization securely
    # To get card_last4 and card_brand, you might need to query QuickBooks
    # Placeholder values are used here
    card_last4 = "4242"  # Replace with actual data from QuickBooks response
    card_brand = "Visa"   # Replace with actual data from QuickBooks response

    # Create and store the payment method
    db_payment_method = await crud.create_payment_method(
        db, current_user.id, payment_method, card_last4, card_brand
    )
    return db_payment_method

# Endpoint to create a subscription
@app.post("/subscriptions", response_model=schemas.SubscriptionOut)
async def create_subscription_endpoint(
    subscription: schemas.SubscriptionCreate,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Validate payment method belongs to user
    payment_method = await crud.get_payment_method_by_id(db, subscription.payment_method_id)
    if not payment_method or payment_method.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Invalid payment method")

    # Create subscription
    db_subscription = await crud.create_subscription(db, current_user.id, subscription)

    # Set next billing date based on tier (example: monthly)
    db_subscription.next_billing_date = datetime.utcnow() + timedelta(days=30)
    await db.commit()
    await db.refresh(db_subscription)

    return db_subscription

# Endpoint to process a one-time payment
@app.post("/payments/authorize", response_model=schemas.TransactionOut)
async def authorize_payment(
    amount: float,
    token: str,
    currency: str = "USD",  # Token from QuickBooks
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Authorize the payment
    charge_response = await qb_client.authorize_payment(token, amount, currency)
    charge_id = charge_response.get("id")
    status_ = charge_response.get("status")
    
    # Create transaction record
    db_transaction = models.Transaction(
        user_id=current_user.id,
        amount=amount,
        currency=currency,
        status=status_,
        transaction_id=charge_id
    )
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)

    return db_transaction

# Endpoint to capture an authorized payment
@app.post("/payments/capture/{transaction_id}", response_model=schemas.TransactionOut)
async def capture_payment(
    transaction_id: int,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    db_transaction = await db.get(models.Transaction, transaction_id)
    if not db_transaction or db_transaction.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if db_transaction.status != "authorized":
        raise HTTPException(status_code=400, detail="Transaction not eligible for capture")

    # Capture payment via QuickBooks
    captured = await qb_client.capture_payment(db_transaction.transaction_id)
    db_transaction.status = captured.get("status", "captured")
    await db.commit()
    await db.refresh(db_transaction)

    return db_transaction

# Endpoint to view payment history
@app.get("/transactions", response_model=List[schemas.TransactionOut])
async def get_transactions(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    transactions = await crud.get_user_transactions(db, current_user.id)
    return transactions

# Additional endpoints for subscription management, refunds, etc., can be added similarly