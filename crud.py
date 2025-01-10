from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
import models
from datetime import datetime, timedelta

# Payment Methods
async def create_payment_method(db: AsyncSession, user_id: int, token_info: dict):
    payment_method = models.PaymentMethod(
        user_id=user_id,
        token=token_info['value'],
        card_last_four=token_info['card']['number'][-4:],
        card_brand=token_info['card']['type'],
        expiration_date=f"{token_info['card']['expireMonth']}/{token_info['card']['expireYear']}",
        is_default=True
    )
    db.add(payment_method)
    await db.commit()
    await db.refresh(payment_method)
    return payment_method

async def get_payment_methods(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.PaymentMethod).where(models.PaymentMethod.user_id == user_id))
    return result.scalars().all()

async def delete_payment_method(db: AsyncSession, payment_method_id: int, user_id: int):
    result = await db.execute(
        delete(models.PaymentMethod)
        .where(
            models.PaymentMethod.id == payment_method_id,
            models.PaymentMethod.user_id == user_id
        )
    )
    await db.commit()
    return result.rowcount > 0

# Subscriptions
async def create_subscription(db: AsyncSession, user_id: int, tier: str):
    subscription = models.Subscription(
        user_id=user_id,
        tier=tier,
        is_active=True,
        next_billing_date=datetime.utcnow() + timedelta(days=30)
    )
    db.add(subscription)
    await db.commit()
    await db.refresh(subscription)
    return subscription

async def get_subscription(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Subscription).where(models.Subscription.user_id == user_id))
    return result.scalars().first()

async def update_subscription(db: AsyncSession, subscription: models.Subscription):
    await db.commit()
    await db.refresh(subscription)
    return subscription

async def cancel_subscription(db: AsyncSession, user_id: int):
    subscription = await get_subscription(db, user_id)
    if subscription:
        subscription.is_active = False
        await db.commit()
        await db.refresh(subscription)
        return subscription
    return None

# Transactions
async def create_transaction(db: AsyncSession, user_id: int, amount: int, status: str, transaction_id: str = None):
    transaction = models.Transaction(
        user_id=user_id,
        amount=amount,
        status=status,
        date=datetime.utcnow(),
        transaction_id=transaction_id
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction

async def get_transactions(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Transaction).where(models.Transaction.user_id == user_id))
    return result.scalars().all()


#Rev 1 
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from sqlalchemy import update, delete
# import models
# from datetime import datetime, timedelta

# # Payment Methods
# async def create_payment_method(db: AsyncSession, user_id: int, token_info: dict):
#     payment_method = models.PaymentMethod(
#         user_id=user_id,
#         token=token_info['value'],
#         card_last_four=token_info['card']['number'][-4:],
#         card_brand=token_info['card']['type'],
#         expiration_date=f"{token_info['card']['expireMonth']}/{token_info['card']['expireYear']}",
#         is_default=True
#     )
#     db.add(payment_method)
#     await db.commit()
#     await db.refresh(payment_method)
#     return payment_method

# async def get_payment_methods(db: AsyncSession, user_id: int):
#     result = await db.execute(select(models.PaymentMethod).where(models.PaymentMethod.user_id == user_id))
#     return result.scalars().all()

# async def delete_payment_method(db: AsyncSession, payment_method_id: int, user_id: int):
#     result = await db.execute(
#         delete(models.PaymentMethod)
#         .where(
#             models.PaymentMethod.id == payment_method_id,
#             models.PaymentMethod.user_id == user_id
#         )
#     )
#     await db.commit()
#     return result.rowcount > 0

# # Subscriptions
# async def create_subscription(db: AsyncSession, user_id: int, tier: str):
#     subscription = models.Subscription(
#         user_id=user_id,
#         tier=tier,
#         is_active=True,
#         next_billing_date=datetime.utcnow() + timedelta(days=30)
#     )
#     db.add(subscription)
#     await db.commit()
#     await db.refresh(subscription)
#     return subscription

# async def get_subscription(db: AsyncSession, user_id: int):
#     result = await db.execute(select(models.Subscription).where(models.Subscription.user_id == user_id))
#     return result.scalars().first()

# async def update_subscription(db: AsyncSession, subscription: models.Subscription):
#     await db.commit()
#     await db.refresh(subscription)
#     return subscription

# async def cancel_subscription(db: AsyncSession, user_id: int):
#     subscription = await get_subscription(db, user_id)
#     if subscription:
#         subscription.is_active = False
#         await db.commit()
#         await db.refresh(subscription)
#         return subscription
#     return None

# # Transactions
# async def create_transaction(db: AsyncSession, user_id: int, amount: int, status: str):
#     transaction = models.Transaction(
#         user_id=user_id,
#         amount=amount,
#         status=status,
#         date=datetime.utcnow()
#     )
#     db.add(transaction)
#     await db.commit()
#     await db.refresh(transaction)
#     return transaction

# async def get_transactions(db: AsyncSession, user_id: int):
#     result = await db.execute(select(models.Transaction).where(models.Transaction.user_id == user_id))
#     return result.scalars().all()


# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from . import models, schemas
# from typing import Optional

# async def get_payment_method_by_id(db: AsyncSession, payment_method_id: int):
#     result = await db.execute(select(models.PaymentMethod).filter(models.PaymentMethod.id == payment_method_id))
#     return result.scalars().first()

# async def create_payment_method(db: AsyncSession, user_id: int, payment_method: schemas.PaymentMethodCreate, card_last4: str, card_brand: str):
#     db_payment_method = models.PaymentMethod(
#         user_id=user_id,
#         quickbooks_card_id=payment_method.quickbooks_card_id,
#         card_last4=card_last4,
#         card_brand=card_brand,
#         is_default=True  # Set as default; handle previous defaults if needed
#     )
#     db.add(db_payment_method)
#     await db.commit()
#     await db.refresh(db_payment_method)
#     return db_payment_method

# async def get_user_subscriptions(db: AsyncSession, user_id: int):
#     result = await db.execute(select(models.Subscription).filter(models.Subscription.user_id == user_id))
#     return result.scalars().all()

# async def create_subscription(db: AsyncSession, user_id: int, subscription: schemas.SubscriptionCreate):
#     db_subscription = models.Subscription(
#         user_id=user_id,
#         tier=subscription.tier,
#         payment_method_id=subscription.payment_method_id,
#         # Set next_billing_date based on tier's billing cycle
#     )
#     db.add(db_subscription)
#     await db.commit()
#     await db.refresh(db_subscription)
#     return db_subscription

# async def get_user_transactions(db: AsyncSession, user_id: int):
#     result = await db.execute(select(models.Transaction).filter(models.Transaction.user_id == user_id).order_by(models.Transaction.created_at.desc()))
#     return result.scalars().all()

# # Add more CRUD functions as needed