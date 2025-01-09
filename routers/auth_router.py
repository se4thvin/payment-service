# main.py or auth_router.py

from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
from auth_utils import auth_client
from intuitlib.enums import Scopes

app = FastAPI()

@app.get("/auth/authorize")
def authorize():
    scopes = [
        Scopes.OPENID,
        Scopes.EMAIL,
        Scopes.PROFILE,
        Scopes.PHONE,
        Scopes.ADDRESS,
        Scopes.ACCOUNTING,
        # Add other scopes as needed
    ]
    authorization_url = auth_client.get_authorization_url(scopes)
    return RedirectResponse(authorization_url)

@app.get("/auth/callback")
def callback(request: Request):
    state = request.query_params.get('state')
    code = request.query_params.get('code')
    realm_id = request.query_params.get('realmId')

    if state != auth_client.state_token:
        # Handle CSRF error
        return {"error": "State token mismatch"}

    # Exchange authorization code for access token
    try:
        auth_client.get_bearer_token(code, realm_id=realm_id)
    except Exception as e:
        # Handle error
        return {"error": str(e)}

    # Store tokens securely
    access_token = auth_client.access_token
    refresh_token = auth_client.refresh_token
    # Save tokens to persistent storage (e.g., database)

    return {"detail": "Authorization successful"}