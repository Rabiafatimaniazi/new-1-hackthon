from datetime import timedelta
import os

# Authentication configuration
class AuthConfig:
    # Secret key for JWT tokens (in production, use a strong secret from environment)
    SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")

    # JWT algorithm
    ALGORITHM = "HS256"

    # Token expiration times
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # Password hashing
    HASHING_ALGORITHM = "bcrypt"
    BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", "12"))

    # Rate limiting
    MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
    LOCKOUT_DURATION_MINUTES = int(os.getenv("LOCKOUT_DURATION_MINUTES", "30"))

    # Session management
    SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))

    # Token refresh window (how early before expiration can token be refreshed)
    REFRESH_WINDOW_MINUTES = int(os.getenv("REFRESH_WINDOW_MINUTES", "5"))

# Create global instance
auth_config = AuthConfig()

def get_access_token_expire_delta():
    """Get timedelta for access token expiration"""
    return timedelta(minutes=auth_config.ACCESS_TOKEN_EXPIRE_MINUTES)

def get_refresh_token_expire_delta():
    """Get timedelta for refresh token expiration"""
    return timedelta(days=auth_config.REFRESH_TOKEN_EXPIRE_DAYS)