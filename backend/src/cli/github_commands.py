"""
GitHub CLI Commands
"""
import click
from typing import Optional
from backend.src.models.repository_config import RepositoryConfig
from backend.src.services.github_integration.github_client import GithubClient
from backend.src.services.github_integration.repository_manager import RepositoryManager
from backend.src.services.github_integration.local_repository import LocalRepository
from backend.src.services.github_integration.auth_service import AuthService
from backend.src.utils.logging import setup_logger


@click.group()
def github():
    """
    GitHub integration commands
    """
    pass


@github.command()
@click.option('--name', required=True, help='Repository name')
@click.option('--description', default='', help='Repository description')
@click.option('--private', is_flag=True, help='Make repository private')
@click.option('--auto-init', is_flag=True, help='Initialize repository with README')
@click.option('--gitignore', default='', help='Gitignore template to use')
@click.option('--license', default='', help='License template to use')
def create_repo(name: str, description: str, private: bool, auto_init: bool, gitignore: str, license: str):
    """
    Create a new GitHub repository
    """
    logger = setup_logger(__name__)
    logger.info(f"Creating repository: {name}")

    try:
        # Create GitHub client
        client = GithubClient()

        # Validate token
        validation_result = client.validate_token()
        if not validation_result["valid"]:
            click.echo(f"Error: {validation_result['message']}", err=True)
            return

        # Create repository configuration
        config = RepositoryConfig(
            name=name,
            description=description if description else None,
            private=private,
            auto_init=auto_init,
            gitignore_template=gitignore if gitignore else None,
            license_template=license if license else None
        )

        # Create repository manager
        repo_manager = RepositoryManager(client)

        # Check if repository already exists
        if repo_manager.repository_exists(name):
            click.echo(f"Error: Repository '{name}' already exists", err=True)
            return

        # Create repository
        result = repo_manager.create_repository(config)

        if result.success:
            click.echo(f"✓ Repository created successfully!")
            click.echo(f"  URL: {result.data['repository_url']}")
            click.echo(f"  Clone URL: {result.data['clone_url']}")
            click.echo(f"  SSH URL: {result.data['ssh_url']}")
        else:
            click.echo(f"✗ Failed to create repository: {result.message}", err=True)

    except Exception as e:
        click.echo(f"✗ Error creating repository: {str(e)}", err=True)


@github.command()
@click.option('--repo-name', required=True, help='GitHub repository name')
@click.option('--local-path', default='.', help='Local path to git repository (default: current directory)')
def setup_remote(repo_name: str, local_path: str):
    """
    Set up local repository with remote GitHub repository
    """
    logger = setup_logger(__name__)
    logger.info(f"Setting up remote for: {repo_name}")

    try:
        # Create GitHub client
        client = GithubClient()

        # Validate token
        validation_result = client.validate_token()
        if not validation_result["valid"]:
            click.echo(f"Error: {validation_result['message']}", err=True)
            return

        # Get authenticated user
        user = client.client.get_user()

        # Get repository
        try:
            repo = user.get_repo(repo_name)
        except Exception as e:
            click.echo(f"Error: Repository '{repo_name}' does not exist or is not accessible", err=True)
            return

        # Create local repository manager
        local_repo = LocalRepository(local_path)

        # Configure remote
        result = local_repo.configure_remote(repo.ssh_url if repo.ssh_url else repo.clone_url, "origin")

        if result.success:
            click.echo(f"✓ Remote configured successfully!")
            click.echo(f"  Local path: {local_path}")
            click.echo(f"  Remote URL: {repo.ssh_url or repo.clone_url}")
        else:
            click.echo(f"✗ Failed to configure remote: {result.message}", err=True)

    except Exception as e:
        click.echo(f"✗ Error setting up remote: {str(e)}", err=True)


@github.command()
@click.option('--local-path', default='.', help='Local path to git repository (default: current directory)')
@click.option('--remote-name', default='origin', help='Remote name (default: origin)')
@click.option('--branch', default='main', help='Branch to push to (default: main)')
@click.option('--commit-message', default='Initial commit', help='Commit message for changes')
def push_to_github(local_path: str, remote_name: str, branch: str, commit_message: str):
    """
    Push local changes to GitHub repository
    """
    logger = setup_logger(__name__)
    logger.info(f"Pushing changes from: {local_path} to {remote_name}/{branch}")

    try:
        # Create local repository manager
        local_repo = LocalRepository(local_path)

        # Push changes
        result = local_repo.push_changes(remote_name, branch, commit_message)

        if result.success:
            click.echo(f"✓ Changes pushed successfully!")
            click.echo(f"  Local path: {local_path}")
            click.echo(f"  Remote: {remote_name}")
            click.echo(f"  Branch: {branch}")
            if result.data and "commit_hash" in result.data:
                click.echo(f"  Commit: {result.data['commit_hash']}")
        else:
            click.echo(f"✗ Failed to push changes: {result.message}", err=True)

    except Exception as e:
        click.echo(f"✗ Error pushing changes: {str(e)}", err=True)


@github.command()
def validate_token():
    """
    Validate the GitHub token
    """
    logger = setup_logger(__name__)
    logger.info("Validating GitHub token")

    try:
        # Create GitHub client
        client = GithubClient()

        # Create auth service
        auth_service = AuthService(client)

        # Validate token
        result = auth_service.validate_token()

        if result.success:
            click.echo(f"✓ Token is valid!")
            if result.data and "username" in result.data:
                click.echo(f"  Username: {result.data['username']}")
        else:
            click.echo(f"✗ Token validation failed: {result.message}", err=True)

    except Exception as e:
        click.echo(f"✗ Error validating token: {str(e)}", err=True)


if __name__ == '__main__':
    github()