from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from passlib.context import CryptContext
from backend.rag.models.user import User, UserCreate, UserUpdate
from backend.rag.core.logging_config import get_logger

logger = get_logger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self):
        # In-memory storage for demo purposes
        # In production, this would connect to a database
        self.users: List[User] = []
        self.email_to_user: dict = {}  # For fast email lookup

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password"""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Generate a hash for a plain password"""
        return pwd_context.hash(password)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        return self.email_to_user.get(email)

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by ID"""
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if user already exists
        existing_user = await self.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError(f"User with email {user_data.email} already exists")

        user = User(
            id=uuid4(),
            email=user_data.email,
            name=user_data.name,
            background=user_data.background,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.users.append(user)
        self.email_to_user[user.email] = user

        logger.info(f"Created user: {user.email} (ID: {user.id})")
        return user

    async def update_user(self, user_id: UUID, **kwargs) -> Optional[User]:
        """Update an existing user"""
        for i, user in enumerate(self.users):
            if user.id == user_id:
                # Update the user object
                update_data = {k: v for k, v in kwargs.items() if v is not None}
                updated_user = user.copy(update=update_data)
                updated_user.updated_at = datetime.utcnow()

                self.users[i] = updated_user

                # If email was updated, update the email index
                if 'email' in update_data and user.email != updated_user.email:
                    del self.email_to_user[user.email]
                    self.email_to_user[updated_user.email] = updated_user

                logger.info(f"Updated user: {updated_user.email} (ID: {updated_user.id})")
                return updated_user
        return None

    async def delete_user(self, user_id: UUID) -> bool:
        """Delete a user"""
        for i, user in enumerate(self.users):
            if user.id == user_id:
                del self.users[i]
                del self.email_to_user[user.email]
                logger.info(f"Deleted user with ID: {user_id}")
                return True
        return False

# Global instance
user_service = UserService()