# crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas
from typing import Optional

async def get_payment_method_by_id(db: AsyncSession, payment_method_id: int):
    result = await db.execute(select(models.PaymentMethod).filter(models.PaymentMethod.id == payment_method_id))
    return result.scalars().first()

async def create_payment_method(db: AsyncSession, user_id: int, payment_method: schemas.PaymentMethodCreate, card_last4: str, card_brand: str):
    db_payment_method = models.PaymentMethod(
        user_id=user_id,
        quickbooks_card_id=payment_method.quickbooks_card_id,
        card_last4=card_last4,
        card_brand=card_brand,
        is_default=True  # Set as default; handle previous defaults if needed
    )
    db.add(db_payment_method)
    await db.commit()
    await db.refresh(db_payment_method)
    return db_payment_method

async def get_user_subscriptions(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Subscription).filter(models.Subscription.user_id == user_id))
    return result.scalars().all()

async def create_subscription(db: AsyncSession, user_id: int, subscription: schemas.SubscriptionCreate):
    db_subscription = models.Subscription(
        user_id=user_id,
        tier=subscription.tier,
        payment_method_id=subscription.payment_method_id,
        # Set next_billing_date based on tier's billing cycle
    )
    db.add(db_subscription)
    await db.commit()
    await db.refresh(db_subscription)
    return db_subscription

async def get_user_transactions(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Transaction).filter(models.Transaction.user_id == user_id).order_by(models.Transaction.created_at.desc()))
    return result.scalars().all()

# Add more CRUD functions as needed