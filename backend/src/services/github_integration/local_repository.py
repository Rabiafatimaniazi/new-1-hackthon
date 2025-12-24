"""
Local Repository Service
Handles local git repository operations
"""
import os
import git
from git import Repo
from typing import Optional
from ...models.operation_result import OperationResult
from ...utils.logging import get_logger
from ...utils.errors import LocalRepositoryError


class LocalRepository:
    """
    Service class for managing local git repositories
    """

    def __init__(self, local_path: str = "."):
        """
        Initialize the Local Repository service

        Args:
            local_path: Path to the local git repository (default: current directory)
        """
        self.local_path = os.path.abspath(local_path)
        self.logger = get_logger(__name__)

        # Check if path exists
        if not os.path.exists(self.local_path):
            raise LocalRepositoryError(f"Path does not exist: {self.local_path}")

        # Initialize or open git repository
        if not os.path.exists(os.path.join(self.local_path, ".git")):
            self.logger.info(f"Initializing new git repository at: {self.local_path}")
            self.repo = Repo.init(self.local_path)
        else:
            self.logger.info(f"Opening existing git repository at: {self.local_path}")
            self.repo = Repo(self.local_path)

    def configure_remote(self, remote_url: str, remote_name: str = "origin") -> OperationResult:
        """
        Configure a remote for the local repository

        Args:
            remote_url: URL of the remote repository
            remote_name: Name of the remote (default: origin)

        Returns:
            OperationResult: Result of the operation
        """
        try:
            self.logger.info(f"Configuring remote '{remote_name}' with URL: {remote_url}")

            # Check if remote already exists
            existing_remotes = [remote.name for remote in self.repo.remotes]
            if remote_name in existing_remotes:
                # Update existing remote
                origin = self.repo.remotes[remote_name]
                origin.set_url(remote_url)
                self.logger.info(f"Updated existing remote '{remote_name}' to: {remote_url}")
            else:
                # Add new remote
                self.repo.create_remote(remote_name, remote_url)
                self.logger.info(f"Added new remote '{remote_name}' with URL: {remote_url}")

            return OperationResult(
                success=True,
                message=f"Remote '{remote_name}' configured successfully"
            )

        except Exception as e:
            error_msg = f"Error configuring remote '{remote_name}': {str(e)}"
            self.logger.error(error_msg)
            return OperationResult(
                success=False,
                message=error_msg
            )

    def push_changes(self, remote_name: str = "origin", branch: str = "main", commit_message: str = "Initial commit") -> OperationResult:
        """
        Push local changes to the remote repository

        Args:
            remote_name: Name of the remote (default: origin)
            branch: Branch to push to (default: main)
            commit_message: Commit message for changes (default: "Initial commit")

        Returns:
            OperationResult: Result of the operation
        """
        try:
            self.logger.info(f"Pushing changes to {remote_name}/{branch}")

            # Check for uncommitted changes
            if self.repo.is_dirty(untracked_files=True):
                # Add all changes
                self.repo.git.add(A=True)
                self.logger.info("Added all changes to staging")

                # Create commit
                self.repo.index.commit(commit_message)
                self.logger.info(f"Created commit with message: {commit_message}")

            # Get the current branch or create it if it doesn't exist
            try:
                current_branch = self.repo.heads[branch]
            except IndexError:
                # Branch doesn't exist, create it
                current_branch = self.repo.create_head(branch)
                self.logger.info(f"Created new branch: {branch}")

            # Set the current branch as active
            current_branch.checkout(b=True)

            # Push to remote
            origin = self.repo.remotes[remote_name]
            push_info = origin.push(refspec=f"{branch}:{branch}")

            # Check push result
            for info in push_info:
                if info.flags & info.ERROR:
                    return OperationResult(
                        success=False,
                        message=f"Push failed: {info.summary}"
                    )

            commit_hash = str(self.repo.head.commit.hexsha)[:8]  # Short hash
            return OperationResult(
                success=True,
                message=f"Changes pushed successfully to {remote_name}/{branch}",
                data={"commit_hash": commit_hash}
            )

        except Exception as e:
            error_msg = f"Error pushing changes to {remote_name}/{branch}: {str(e)}"
            self.logger.error(error_msg)
            return OperationResult(
                success=False,
                message=error_msg
            )

    def add_and_commit(self, files: list = None, commit_message: str = "Update") -> OperationResult:
        """
        Add and commit files to the local repository

        Args:
            files: List of files to add (if None, adds all changes)
            commit_message: Commit message

        Returns:
            OperationResult: Result of the operation
        """
        try:
            self.logger.info(f"Adding and committing files with message: {commit_message}")

            if files is None:
                # Add all changes
                self.repo.git.add(A=True)
            else:
                # Add specific files
                self.repo.index.add(files)

            # Create commit
            commit = self.repo.index.commit(commit_message)
            commit_hash = str(commit.hexsha)[:8]

            return OperationResult(
                success=True,
                message=f"Files committed successfully",
                data={"commit_hash": commit_hash}
            )

        except Exception as e:
            error_msg = f"Error adding and committing files: {str(e)}"
            self.logger.error(error_msg)
            return OperationResult(
                success=False,
                message=error_msg
            )

    def get_status(self) -> OperationResult:
        """
        Get the status of the local repository

        Returns:
            OperationResult: Result containing repository status
        """
        try:
            status = {
                "is_dirty": self.repo.is_dirty(untracked_files=True),
                "uncommitted_changes": list(self.repo.untracked_files),
                "modified_files": [item.a_path for item in self.repo.index.diff(None)],
                "current_branch": self.repo.active_branch.name if self.repo.active_branch else "unknown"
            }

            return OperationResult(
                success=True,
                message="Status retrieved successfully",
                data=status
            )

        except Exception as e:
            error_msg = f"Error getting repository status: {str(e)}"
            self.logger.error(error_msg)
            return OperationResult(
                success=False,
                message=error_msg
            )