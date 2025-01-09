# routers/transactions.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_current_user
from database import get_db
import schemas, crud
from typing import List

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/", response_model=List[schemas.TransactionOut])
async def get_transactions(
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    transactions = await crud.get_transactions(db, user["user_id"])
    return transactions