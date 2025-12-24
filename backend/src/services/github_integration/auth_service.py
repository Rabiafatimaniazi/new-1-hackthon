"""
Authentication Service
Handles GitHub authentication operations
"""
from typing import Optional
from backend.src.models.operation_result import OperationResult
from backend.src.services.github_integration.github_client import GithubClient
from backend.src.utils.logging import get_logger
from backend.src.utils.errors import AuthenticationError


class AuthService:
    """
    Service class for handling GitHub authentication
    """

    def __init__(self, github_client: GithubClient):
        """
        Initialize the Authentication Service

        Args:
            github_client: Instance of GithubClient
        """
        self.github_client = github_client
        self.logger = get_logger(__name__)

    def validate_token(self) -> OperationResult:
        """
        Validate the GitHub token

        Returns:
            OperationResult: Result of the token validation
        """
        try:
            self.logger.info("Validating GitHub token")

            # Use the existing validate_token method from GithubClient
            result = self.github_client.validate_token()

            if result["valid"]:
                return OperationResult(
                    success=True,
                    message="Token is valid",
                    data={
                        "username": result["username"],
                        "scopes": result.get("scopes", [])
                    }
                )
            else:
                return OperationResult(
                    success=False,
                    message=result["message"]
                )

        except Exception as e:
            error_msg = f"Error validating token: {str(e)}"
            self.logger.error(error_msg)
            return OperationResult(
                success=False,
                message=error_msg
            )

    def get_user_info(self) -> OperationResult:
        """
        Get user information from GitHub

        Returns:
            OperationResult: Result containing user information
        """
        try:
            self.logger.info("Getting user information")

            user = self.github_client.client.get_user()

            user_info = {
                "login": user.login,
                "name": user.name,
                "email": user.email,
                "bio": user.bio,
                "company": user.company,
                "location": user.location,
                "public_repos": user.public_repos,
                "followers": user.followers,
                "following": user.following,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }

            return OperationResult(
                success=True,
                message="User information retrieved successfully",
                data=user_info
            )

        except Exception as e:
            error_msg = f"Error getting user information: {str(e)}"
            self.logger.error(error_msg)
            return OperationResult(
                success=False,
                message=error_msg
            )

    def check_permissions(self, scopes_needed: list = None) -> OperationResult:
        """
        Check if the token has the required permissions

        Args:
            scopes_needed: List of required scopes (optional)

        Returns:
            OperationResult: Result of the permission check
        """
        try:
            self.logger.info("Checking token permissions")

            # For now, just validate the token since PyGithub doesn't directly expose scopes
            validation_result = self.github_client.validate_token()

            if not validation_result["valid"]:
                return OperationResult(
                    success=False,
                    message=validation_result["message"]
                )

            # If specific scopes are needed, we'd need to implement a different approach
            # since PyGithub doesn't directly provide scope information
            result_data = {
                "username": validation_result["username"],
                "has_basic_access": True  # If token is valid, user has basic access
            }

            if scopes_needed:
                result_data["scopes_needed"] = scopes_needed
                result_data["warning"] = "Scope validation not implemented in this version"

            return OperationResult(
                success=True,
                message="Token has basic access",
                data=result_data
            )

        except Exception as e:
            error_msg = f"Error checking permissions: {str(e)}"
            self.logger.error(error_msg)
            return OperationResult(
                success=False,
                message=error_msg
            )

    def store_token_securely(self, token: str, filepath: str = ".env") -> OperationResult:
        """
        Store the token securely in a file (like .env)

        Args:
            token: GitHub token to store
            filepath: Path to the file where token should be stored (default: .env)

        Returns:
            OperationResult: Result of the operation
        """
        try:
            import os
            from pathlib import Path

            self.logger.info(f"Storing token securely in {filepath}")

            # Create the file if it doesn't exist
            env_path = Path(filepath)
            if not env_path.exists():
                env_path.touch(mode=0o600)  # Read/write for owner only
            else:
                # Ensure file has secure permissions
                os.chmod(filepath, 0o600)

            # Read existing content
            with open(filepath, 'r') as f:
                content = f.read()

            # Check if GITHUB_TOKEN already exists
            lines = content.split('\n') if content else []
            token_exists = False

            for i, line in enumerate(lines):
                if line.startswith('GITHUB_TOKEN='):
                    lines[i] = f'GITHUB_TOKEN={token}'
                    token_exists = True
                    break

            # If token doesn't exist, add it
            if not token_exists:
                lines.append(f'GITHUB_TOKEN={token}')

            # Write back to file
            with open(filepath, 'w') as f:
                f.write('\n'.join(lines))

            return OperationResult(
                success=True,
                message=f"Token stored securely in {filepath}"
            )

        except Exception as e:
            error_msg = f"Error storing token securely: {str(e)}"
            self.logger.error(error_msg)
            return OperationResult(
                success=False,
                message=error_msg
            )

    def retrieve_token_securely(self, filepath: str = ".env") -> OperationResult:
        """
        Retrieve the token from a secure file (like .env)

        Args:
            filepath: Path to the file where token is stored (default: .env)

        Returns:
            OperationResult: Result containing the token
        """
        try:
            import os
            from pathlib import Path

            self.logger.info(f"Retrieving token from {filepath}")

            # Check if file exists
            env_path = Path(filepath)
            if not env_path.exists():
                return OperationResult(
                    success=False,
                    message=f"Token file {filepath} does not exist"
                )

            # Read the file
            with open(filepath, 'r') as f:
                content = f.read()

            # Find the GITHUB_TOKEN line
            lines = content.split('\n') if content else []
            for line in lines:
                if line.startswith('GITHUB_TOKEN='):
                    token = line.split('=', 1)[1]
                    return OperationResult(
                        success=True,
                        message="Token retrieved successfully",
                        data={"token": token}
                    )

            return OperationResult(
                success=False,
                message="GITHUB_TOKEN not found in the file"
            )

        except Exception as e:
            error_msg = f"Error retrieving token: {str(e)}"
            self.logger.error(error_msg)
            return OperationResult(
                success=False,
                message=error_msg
            )