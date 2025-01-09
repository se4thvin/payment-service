# scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
from database import AsyncSessionLocal
from sqlalchemy.future import select
import payments
import models
import crud
import asyncio

scheduler = AsyncIOScheduler()

async def start_scheduler():
    # Schedule existing subscriptions
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(models.Subscription).where(models.Subscription.is_active == True))
        subscriptions = result.scalars().all()
        for subscription in subscriptions:
            schedule_subscription_payment(subscription)

def schedule_subscription_payment(subscription: models.Subscription):
    scheduler.add_job(
        process_subscription_payment,
        trigger=DateTrigger(run_date=subscription.next_billing_date),
        args=[subscription.user_id],
        id=f"subscription_{subscription.user_id}",
        replace_existing=True
    )

async def process_subscription_payment(user_id: int):
    async with AsyncSessionLocal() as db:
        # Get subscription
        subscription = await crud.get_subscription(db, user_id)
        if not subscription or not subscription.is_active:
            return

        # Get default payment method
        payment_methods = await crud.get_payment_methods(db, user_id)
        payment_method = next((pm for pm in payment_methods if pm.is_default), None)
        if not payment_method:
            # Handle missing payment method
            subscription.is_active = False
            await crud.update_subscription(db, subscription)
            return

        # Determine amount based on tier
        amount = 0
        if subscription.tier == 'bronze':
            amount = 1000
        elif subscription.tier == 'silver':
            amount = 2000
        elif subscription.tier == 'gold':
            amount = 3000

        # Process payment
        try:
            charge_response = payments.charge_payment(
                amount=str(amount / 100),
                currency='USD',
                token=payment_method.token
            )
            # Record transaction
            await crud.create_transaction(db, user_id, amount, 'succeeded')
            # Update next billing date
            subscription.next_billing_date += timedelta(days=30)
            await crud.update_subscription(db, subscription)
            # Reschedule the job
            schedule_subscription_payment(subscription)
        except Exception as e:
            # Handle payment failure
            await crud.create_transaction(db, user_id, amount, 'failed')
            subscription.is_active = False
            await crud.update_subscription(db, subscription)