# dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import get_user_by_email
from .config import settings
from .models import User
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession as SQLAlchemyAsyncSession
from sqlalchemy.orm import sessionmaker

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth-service/api/auth/token")

# Database setup (similar to Auth-service)
engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, class_=SQLAlchemyAsyncSession, expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        yield session

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    if not user:
        raise credentials_exception
    return user