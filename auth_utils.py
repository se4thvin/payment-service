from sqlalchemy.orm import Session
from dependencies import get_db
from intuitlib.client import AuthClient
from config import settings
from models import OAuthToken
from datetime import datetime
from fastapi import Depends

auth_client = AuthClient(
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    environment=settings.ENVIRONMENT,
    redirect_uri=settings.REDIRECT_URI,
)

def get_valid_access_token(db: Session = Depends(get_db)):
    # Fetch the tokens from the database
    token = db.query(OAuthToken).first()

    if not token:
        raise Exception("No OAuth token found. Please authenticate.")

    if token.access_token_expiry <= datetime.utcnow():
        # Access token has expired, refresh it
        auth_client.refresh(refresh_token=token.refresh_token)
        # Update tokens in the database
        token.access_token = auth_client.access_token
        token.refresh_token = auth_client.refresh_token
        token.expires_in = auth_client.expires_in
        token.x_refresh_token_expires_in = auth_client.x_refresh_token_expires_in
        token.created_at = datetime.utcnow()
        db.commit()
    else:
        auth_client.access_token = token.access_token
        auth_client.refresh_token = token.refresh_token
    return token.access_token