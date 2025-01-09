from quickbooks import QuickBooks
from intuitlib.client import AuthClient
from sqlalchemy.orm import Session
from auth_utils import auth_client, get_valid_access_token
from database import get_db
import os

# Load environment variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
COMPANY_ID = os.getenv('COMPANY_ID')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'sandbox')  # 'sandbox' or 'production'


def get_qb_client(db: Session = Depends(get_db)):
    access_token = get_valid_access_token(db)
    # Update the AuthClient with the new access token
    auth_client.access_token = access_token
    # Initialize QuickBooks client
    qb_client = QuickBooks(
        auth_client=auth_client,
        company_id=auth_client.realm_id,
    )
    return qb_client

# Initialize AuthClient
auth_client = AuthClient(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    environment=ENVIRONMENT,
    redirect_uri=REDIRECT_URI,
)

# Initialize QuickBooks client
qb_client = QuickBooks(
    auth_client=auth_client,
    refresh_token=REFRESH_TOKEN,
    company_id=COMPANY_ID,
)

# Refresh the token if needed
refresh_token = qb_client.refresh_token  # Store the new refresh token