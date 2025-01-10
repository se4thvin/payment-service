# payments.py

from quickbooks.objects.payment import Payment
from quickbooks.objects.base import Ref
from quickbooks_client import get_qb_client
from models import PaymentMethod
from sqlalchemy.orm import Session
from dependencies import get_db
from fastapi import Depends

def charge_payment(amount: float, currency: str, token: str, user_id: int, db: Session = Depends(get_db)):
    # Initialize QuickBooks client
    qb_client = get_qb_client(db)

    # Create a Payment object
    payment = Payment()
    
    # Set the customer reference (You'll need to map your user_id to a QuickBooks Customer)
    customer_ref = Ref(value="1")  # Placeholder; implement customer mapping ?

    payment.CustomerRef = customer_ref
    payment.TotalAmt = amount
    payment.PrivateNote = "Subscription payment"

    # Set the payment method
    payment.PaymentMethodRef = Ref(value=token)

    # Save the payment
    payment.save(qb=qb_client)
    return payment