from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from datetime import timedelta
from backend.rag.models.user import UserCreate, UserUpdate
from backend.shared.types import User as SharedUser
from backend.auth.auth import auth_handler, security
from backend.rag.services.user_service import user_service
from backend.auth.config import get_access_token_expire_delta
from backend.rag.core.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=SharedUser)
async def signup(user_create: UserCreate):
    """User registration"""
    logger.info(f"User registration attempt for email: {user_create.email}")

    # Check if user already exists
    existing_user = await user_service.get_user_by_email(user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Create new user
    user = await user_service.create_user(user_create)

    # Create access token for the new user
    access_token_expires = get_access_token_expire_delta()
    access_token = auth_handler.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    logger.info(f"User created successfully: {user.email}")

    # Return user with token
    return {**user.dict(), "access_token": access_token}


@router.post("/login")
async def login(email: str, password: str):
    """User login"""
    logger.info(f"Login attempt for email: {email}")

    # In a real implementation, this would verify password
    # For demo, we'll just check if user exists
    user = await user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create access token for the user
    access_token_expires = get_access_token_expire_delta()
    access_token = auth_handler.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    logger.info(f"User logged in successfully: {email}")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name
        }
    }


@router.get("/profile", response_model=SharedUser)
async def get_profile(current_user: SharedUser = Depends(auth_handler.get_current_user)):
    """Get user profile"""
    logger.info(f"Getting profile for user: {current_user.email}")

    # Return the current user's profile
    return current_user


@router.put("/profile", response_model=SharedUser)
async def update_profile(
    user_update: UserUpdate,
    current_user: SharedUser = Depends(auth_handler.get_current_user)
):
    """Update user profile with background info"""
    logger.info(f"Updating profile for user: {current_user.email}")

    # Update the current user's information
    updated_user = await user_service.update_user(
        current_user.id,
        name=user_update.name or current_user.name,
        background=user_update.background or current_user.background
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logger.info(f"User profile updated successfully: {updated_user.email}")
    return updated_user