from quickbooks import QuickBooks
from intuitlib.client import AuthClient
from config import settings
from auth_utils import get_valid_access_token
from sqlalchemy.orm import Session
from dependencies import get_db
from fastapi import Depends

def get_qb_client(db: Session = Depends(get_db)):
    access_token = get_valid_access_token(db)
    auth_client = AuthClient(
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET,
        environment=settings.ENVIRONMENT,
        redirect_uri=settings.REDIRECT_URI,
    )
    auth_client.access_token = access_token
    qb_client = QuickBooks(
        auth_client=auth_client,
        company_id=settings.COMPANY_ID,
    )
    return qb_client