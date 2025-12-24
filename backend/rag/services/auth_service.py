from typing import Optional
from backend.rag.models.user import User, UserCreate
from backend.shared.types import User as SharedUser
from backend.rag.services.user_service import user_service
from backend.rag.core.logging_config import get_logger
import uuid
from datetime import datetime


class AuthService:
    def __init__(self):
        """Initialize the auth service"""
        self.logger = get_logger(__name__)
        self.logger.info("AuthService initialized")

    async def create_user(self, user_create: UserCreate) -> SharedUser:
        """Create a new user"""
        self.logger.info(f"Creating user: {user_create.email}")

        # Use the user_service to create the user
        user = await user_service.create_user(user_create)

        # Convert to SharedUser type if needed
        shared_user = SharedUser(
            id=user.id,
            email=user.email,
            name=user.name,
            background=user.background,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

        self.logger.info(f"User created successfully: {user.email}")
        return shared_user

    async def get_user_by_email(self, email: str) -> Optional[SharedUser]:
        """Get user by email"""
        self.logger.info(f"Getting user by email: {email}")

        # Use the user_service to get the user
        user = await user_service.get_user_by_email(email)
        if user:
            shared_user = SharedUser(
                id=user.id,
                email=user.email,
                name=user.name,
                background=user.background,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            return shared_user
        return None

    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[SharedUser]:
        """Get user by ID"""
        self.logger.info(f"Getting user by ID: {user_id}")

        # Use the user_service to get the user
        user = await user_service.get_user_by_id(user_id)
        if user:
            shared_user = SharedUser(
                id=user.id,
                email=user.email,
                name=user.name,
                background=user.background,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            return shared_user
        return None

    async def update_user(self, user_id: uuid.UUID, **kwargs) -> Optional[SharedUser]:
        """Update user information"""
        self.logger.info(f"Updating user: {user_id}")

        # Use the user_service to update the user
        updated_user = await user_service.update_user(user_id, **kwargs)
        if updated_user:
            shared_user = SharedUser(
                id=updated_user.id,
                email=updated_user.email,
                name=updated_user.name,
                background=updated_user.background,
                created_at=updated_user.created_at,
                updated_at=updated_user.updated_at
            )
            return shared_user
        return None