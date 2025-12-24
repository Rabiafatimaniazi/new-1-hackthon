"""
GitHub Client Service
Handles communication with the GitHub API
"""
import os
from typing import Optional
from github import Github
from github.GithubException import GithubException
from ...config import Config


class GithubClient:
    """
    Service class for interacting with GitHub API
    """

    def __init__(self, token: Optional[str] = None):
        """
        Initialize the GitHub client

        Args:
            token: GitHub Personal Access Token. If not provided,
                   will try to read from GITHUB_TOKEN environment variable
        """
        if token is None:
            token = Config.get_github_token()

        if not token:
            raise ValueError("GitHub token is required. Set GITHUB_TOKEN environment variable or pass as parameter.")

        self.token = token
        self.client = Github(token)

    def validate_token(self) -> dict:
        """
        Validate the GitHub token and return user information

        Returns:
            dict: User information including username and scopes
        """
        try:
            user = self.client.get_user()
            # For now, return basic user info
            return {
                "valid": True,
                "username": user.login,
                "scopes": []  # GitHub API doesn't directly provide scopes, would need to check differently
            }
        except GithubException as e:
            return {
                "valid": False,
                "message": f"Invalid token: {str(e)}"
            }
        except Exception as e:
            return {
                "valid": False,
                "message": f"Error validating token: {str(e)}"
            }

    def get_client(self):
        """
        Get the underlying GitHub client instance

        Returns:
            Github: PyGithub client instance
        """
        return self.client