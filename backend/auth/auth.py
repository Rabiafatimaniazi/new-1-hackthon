from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from backend.rag.models.user import User
from backend.rag.services.auth_service import AuthService

# Security scheme for API docs
security = HTTPBearer()

# Secret key for JWT tokens (in production, use a strong secret from environment)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthHandler:
    def __init__(self):
        self.auth_service = AuthService()

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create a new access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def verify_token(self, token: str) -> Optional[User]:
        """Verify the access token and return the user"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            # In a real implementation, you would fetch the user from the database
            # For this demo, we'll use the in-memory store in the auth service
            user = await self.auth_service.get_user_by_id(user_id)
            return user
        except JWTError:
            return None

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
        """Get the current user from the token in the request"""
        token = credentials.credentials
        user = await self.verify_token(token)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user


# Create a global instance of the auth handler
auth_handler = AuthHandler()