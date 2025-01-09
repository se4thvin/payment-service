# routers/subscriptions.py

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_current_user
from database import get_db
import schemas, crud
import models
import payments
from scheduler import schedule_subscription_payment

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

@router.post("/", response_model=schemas.SubscriptionOut)
async def create_subscription(
    subscription: schemas.SubscriptionCreate,
    payment_method_id: int = Body(),
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Validate payment method
    payment_methods = await crud.get_payment_methods(db, user["user_id"])
    payment_method = next((pm for pm in payment_methods if pm.id == payment_method_id), None)
    if not payment_method:
        raise HTTPException(status_code=404, detail="Payment method not found")

    # Determine amount based on tier
    amount = 0
    if subscription.tier == 'basic':
        amount = 1000
    elif subscription.tier == 'standard':
        amount = 2000
    elif subscription.tier == 'premium':
        amount = 3000
    else:
        raise HTTPException(status_code=400, detail="Invalid subscription tier")

    # Process payment
    try:
        charge_response = payments.charge_payment(
            amount=str(amount / 100),
            currency='USD',
            token=payment_method.token
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Payment processing failed")

    # Record transaction
    await crud.create_transaction(db, user["user_id"], amount, 'succeeded')

    # Create subscription
    new_subscription = await crud.create_subscription(db, user["user_id"], subscription.tier)

    # Schedule next billing
    schedule_subscription_payment(new_subscription)

    return new_subscription

@router.get("/", response_model=schemas.SubscriptionOut)
async def get_subscription(
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    subscription = await crud.get_subscription(db, user["user_id"])
    if not subscription:
        raise HTTPException(status_code=404, detail="No active subscription")
    return subscription

@router.post("/cancel/", response_model=schemas.SubscriptionOut)
async def cancel_subscription(
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    subscription = await crud.cancel_subscription(db, user["user_id"])
    if not subscription:
        raise HTTPException(status_code=404, detail="No active subscription")
    return subscription