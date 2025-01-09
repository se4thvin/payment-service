# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    QUICKBOOKS_CLIENT_ID: str
    QUICKBOOKS_CLIENT_SECRET: str
    QUICKBOOKS_REDIRECT_URI: str
    QUICKBOOKS_ENVIRONMENT: str  # 'sandbox' or 'production'
    QUICKBOOKS_COMPANY_ID: str
    DATABASE_URL: str
    SECRET_KEY: str  # For JWT; should match Auth-service
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()