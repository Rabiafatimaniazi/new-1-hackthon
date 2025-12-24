"""
Repository Manager Service
Handles GitHub repository creation and management
"""
from github import Github, GithubException
from typing import Optional
from ...models.repository_config import RepositoryConfig
from ...models.operation_result import OperationResult
from .github_client import GithubClient
from ...utils.logging import get_logger
from ...utils.errors import RepositoryCreationError


class RepositoryManager:
    """
    Service class for managing GitHub repositories
    """

    def __init__(self, github_client: GithubClient):
        """
        Initialize the Repository Manager

        Args:
            github_client: Instance of GithubClient
        """
        self.github_client = github_client
        self.logger = get_logger(__name__)

    def create_repository(self, config: RepositoryConfig) -> OperationResult:
        """
        Create a new GitHub repository

        Args:
            config: Repository configuration

        Returns:
            OperationResult: Result of the operation
        """
        try:
            self.logger.info(f"Creating repository: {config.name}")

            # Get authenticated user
            user = self.github_client.client.get_user()

            # Create the repository
            repo = user.create_repo(
                name=config.name,
                description=config.description,
                private=config.private,
                has_issues=config.has_issues,
                has_projects=config.has_projects,
                has_wiki=config.has_wiki,
                team_id=config.team_id,
                auto_init=config.auto_init,
                gitignore_template=config.gitignore_template,
                license_template=config.license_template,
                allow_squash_merge=config.allow_squash_merge,
                allow_merge_commit=config.allow_merge_commit,
                allow_rebase_merge=config.allow_rebase_merge
            )

            # Success result
            result_data = {
                "repository_url": repo.html_url,
                "clone_url": repo.clone_url,
                "ssh_url": repo.ssh_url
            }

            self.logger.info(f"Repository created successfully: {repo.html_url}")
            return OperationResult(
                success=True,
                message=f"Repository '{config.name}' created successfully",
                data=result_data
            )

        except GithubException as e:
            error_msg = f"GitHub API error creating repository '{config.name}': {str(e)}"
            self.logger.error(error_msg)
            return OperationResult(
                success=False,
                message=error_msg,
                error_code=f"GH_{e.status}"
            )

        except RepositoryCreationError as e:
            self.logger.error(f"Repository creation error: {e.message}")
            return OperationResult(
                success=False,
                message=e.message,
                error_code=e.error_code
            )

        except Exception as e:
            error_msg = f"Unexpected error creating repository '{config.name}': {str(e)}"
            self.logger.error(error_msg)
            return OperationResult(
                success=False,
                message=error_msg
            )

    def repository_exists(self, name: str) -> bool:
        """
        Check if a repository exists

        Args:
            name: Repository name

        Returns:
            bool: True if repository exists, False otherwise
        """
        try:
            user = self.github_client.client.get_user()
            user.get_repo(name)
            return True
        except GithubException:
            # Repository doesn't exist or user doesn't have access
            return False
        except Exception:
            # Any other error
            return False