from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_current_user
from database import get_db
import schemas, crud
from scheduler import schedule_subscription_payment

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

@router.post("/", response_model=schemas.SubscriptionOut)
async def create_subscription(
    subscription: schemas.SubscriptionCreate,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Validate payment method
    payment_methods = await crud.get_payment_methods(db, user["user_id"])
    payment_method = next((pm for pm in payment_methods if pm.id == subscription.payment_method_id), None)
    if not payment_method:
        raise HTTPException(status_code=404, detail="Payment method not found")

    # Determine amount based on tier
    amount = 0
    if subscription.tier == 'bronze':
        amount = 1000
    elif subscription.tier == 'silver':
        amount = 2000
    elif subscription.tier == 'gold':
        amount = 3000
    else:
        raise HTTPException(status_code=400, detail="Invalid subscription tier")

    # Process initial payment
    try:
        charge_response = charge_payment(
            amount=amount / 100.0,  # Convert cents to dollars
            currency='USD',
            token=payment_method.token,
            user_id=user["user_id"],  # Placeholder for customer mapping
            db=db
        )
        # Record transaction
        await crud.create_transaction(db, user["user_id"], amount, 'succeeded')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Payment processing failed: {e}")

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