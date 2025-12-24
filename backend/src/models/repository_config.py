"""
Repository configuration model
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class RepositoryConfig:
    """
    Configuration for a GitHub repository
    """
    name: str
    description: Optional[str] = None
    private: bool = False
    has_issues: bool = True
    has_projects: bool = True
    has_wiki: bool = True
    team_id: Optional[int] = None
    auto_init: bool = False
    gitignore_template: Optional[str] = None
    license_template: Optional[str] = None
    allow_squash_merge: bool = True
    allow_merge_commit: bool = True
    allow_rebase_merge: bool = True

    def to_dict(self) -> dict:
        """
        Convert the configuration to a dictionary

        Returns:
            dict: Configuration as dictionary
        """
        return {
            "name": self.name,
            "description": self.description,
            "private": self.private,
            "has_issues": self.has_issues,
            "has_projects": self.has_projects,
            "has_wiki": self.has_wiki,
            "team_id": self.team_id,
            "auto_init": self.auto_init,
            "gitignore_template": self.gitignore_template,
            "license_template": self.license_template,
            "allow_squash_merge": self.allow_squash_merge,
            "allow_merge_commit": self.allow_merge_commit,
            "allow_rebase_merge": self.allow_rebase_merge
        }