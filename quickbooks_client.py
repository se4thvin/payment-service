# quickbooks_client.py
import httpx
from .config import settings

class QuickBooksClient:
    def __init__(self):
        self.base_url = "https://api.intuit.com/quickbooks/v4/payments"
        self.client_id = settings.QUICKBOOKS_CLIENT_ID
        self.client_secret = settings.QUICKBOOKS_CLIENT_SECRET
        self.redirect_uri = settings.QUICKBOOKS_REDIRECT_URI
        self.environment = settings.QUICKBOOKS_ENVIRONMENT  # 'sandbox' or 'production'
        self.company_id = settings.QUICKBOOKS_COMPANY_ID
        self.access_token = self.obtain_access_token()
    
    def obtain_access_token(self):
        # Implement OAuth2 flow to obtain access token 
        # This is a simplified placeholder; implement securely with token refresh
        return "your_access_token"

    async def create_token(self, card_details: dict) -> dict:
        url = f"{self.base_url}/tokens"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "card": {
                "number": card_details["number"],
                "expMonth": card_details["exp_month"],
                "expYear": card_details["exp_year"],
                "cvc": card_details["cvc"],
                "name": card_details["name"],
                "address": {
                    "line1": card_details.get("address_line1"),
                    "city": card_details.get("city"),
                    "state": card_details.get("state"),
                    "postalCode": card_details.get("postal_code"),
                    "country": card_details.get("country")
                }
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()

    async def authorize_payment(self, token: str, amount: float, currency: str = "USD") -> dict:
        url = f"{self.base_url}/charges"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "amount": f"{amount:.2f}",
            "currency": currency,
            "source": {
                "token": token
            },
            "capture": False  # Authorization only
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()

    async def capture_payment(self, charge_id: str) -> dict:
        url = f"{self.base_url}/charges/{charge_id}/capture"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers)
            response.raise_for_status()
            return response.json()

    async def refund_payment(self, charge_id: str, amount: float) -> dict:
        url = f"{self.base_url}/charges/{charge_id}/refund"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "amount": f"{amount:.2f}"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()

    # Implement other QuickBooks API interactions as needed