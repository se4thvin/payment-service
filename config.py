from pydantic import BaseSettings

class Settings(BaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET: str
    REDIRECT_URI: str
    ENVIRONMENT: str  # 'sandbox' or 'production'
    COMPANY_ID: str
    PAYMENT_DB_URI: str
    SECRET_KEY: str  # For JWT; should match auth-service
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()