from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from dependencies import get_current_user
from database import get_db
import schemas, crud
from typing import List

router = APIRouter(prefix="/payment-methods", tags=["Payment Methods"])

@router.post("/", response_model=schemas.PaymentMethodOut)
async def add_payment_method(
    payment_method: schemas.PaymentMethodCreate,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Tokenization should already be done on the frontend or via a secure endpoint
    token_info = {"value": payment_method.token}
    # Assuming card details are provided or retrieved via QuickBooks
    card_info = {
        "card": {
            "number": "4111111111111111",
            "type": "Visa",
            "expireMonth": "12",
            "expireYear": "2025"
        }
    }
    token_info.update(card_info)
    new_payment_method = await crud.create_payment_method(db, user["user_id"], token_info)
    return new_payment_method

@router.get("/", response_model=List[schemas.PaymentMethodOut])
async def get_payment_methods(
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    payment_methods = await crud.get_payment_methods(db, user["user_id"])
    return payment_methods

@router.delete("/{payment_method_id}")
async def delete_payment_method(
    payment_method_id: int,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    success = await crud.delete_payment_method(db, payment_method_id, user["user_id"])
    if not success:
        raise HTTPException(status_code=404, detail="Payment method not found")
    return {"detail": "Payment method deleted"}