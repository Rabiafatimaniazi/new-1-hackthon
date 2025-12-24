"""
Authentication configuration model
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class AuthConfig:
    """
    Configuration for GitHub authentication
    """
    token: str
    username: Optional[str] = None
    api_url: str = "https://api.github.com"

    def to_dict(self) -> dict:
        """
        Convert the configuration to a dictionary

        Returns:
            dict: Configuration as dictionary
        """
        return {
            "token": self.token,
            "username": self.username,
            "api_url": self.api_url
        }