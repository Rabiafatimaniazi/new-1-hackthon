"""
Error handling utilities for GitHub integration
"""


class GithubIntegrationError(Exception):
    """
    Base exception for GitHub integration errors
    """
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class RepositoryCreationError(GithubIntegrationError):
    """
    Exception raised when repository creation fails
    """
    pass


class AuthenticationError(GithubIntegrationError):
    """
    Exception raised when authentication fails
    """
    pass


class LocalRepositoryError(GithubIntegrationError):
    """
    Exception raised when local repository operations fail
    """
    pass