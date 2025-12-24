"""
Configuration management for the GitHub integration
"""
import os
from typing import Optional


class Config:
    """
    Configuration class for GitHub integration settings
    """

    @staticmethod
    def get_github_token() -> Optional[str]:
        """
        Get the GitHub token from environment variables

        Returns:
            Optional[str]: GitHub token or None if not set
        """
        return os.getenv('GITHUB_TOKEN')

    @staticmethod
    def get_github_api_url() -> str:
        """
        Get the GitHub API URL

        Returns:
            str: GitHub API URL (defaults to https://api.github.com)
        """
        return os.getenv('GITHUB_API_URL', 'https://api.github.com')

    @staticmethod
    def get_timeout() -> int:
        """
        Get the timeout for API requests

        Returns:
            int: Timeout in seconds (defaults to 30)
        """
        return int(os.getenv('GITHUB_TIMEOUT', '30'))