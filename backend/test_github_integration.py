"""
Basic test to verify GitHub integration functionality
"""
import os
import sys
from unittest.mock import Mock, patch

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.github_integration.github_client import GithubClient
from services.github_integration.repository_manager import RepositoryManager
from models.repository_config import RepositoryConfig


def test_github_client_initialization():
    """
    Test that GithubClient can be initialized
    """
    print("Testing GitHub Client initialization...")

    # Mock the GitHub token environment variable
    with patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token'}):
        try:
            client = GithubClient()
            print("✓ GithubClient initialized successfully")
            return True
        except Exception as e:
            print(f"✗ Failed to initialize GithubClient: {e}")
            return False


def test_repository_config_creation():
    """
    Test that RepositoryConfig can be created
    """
    print("Testing RepositoryConfig creation...")

    try:
        config = RepositoryConfig(
            name="test-repo",
            description="Test repository for integration",
            private=True
        )
        print(f"✓ RepositoryConfig created: {config.name}")
        return True
    except Exception as e:
        print(f"✗ Failed to create RepositoryConfig: {e}")
        return False


def test_repository_config_to_dict():
    """
    Test that RepositoryConfig can be converted to dictionary
    """
    print("Testing RepositoryConfig to_dict conversion...")

    try:
        config = RepositoryConfig(
            name="test-repo",
            description="Test repository for integration",
            private=True,
            auto_init=True
        )
        config_dict = config.to_dict()

        expected_keys = ["name", "description", "private", "auto_init"]
        for key in expected_keys:
            if key not in config_dict:
                print(f"✗ Missing key '{key}' in config dict")
                return False

        print("✓ RepositoryConfig converted to dictionary successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to convert RepositoryConfig to dict: {e}")
        return False


def main():
    """
    Main test function
    """
    print("Starting GitHub Integration Tests")
    print("=" * 40)

    tests = [
        test_github_client_initialization,
        test_repository_config_creation,
        test_repository_config_to_dict
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()  # Add blank line between tests

    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("✓ All tests passed!")
        return True
    else:
        print("✗ Some tests failed!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)