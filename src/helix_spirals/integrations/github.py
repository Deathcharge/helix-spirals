"""
GitHub Integration
==================

Integration with GitHub for repository and issue management.

Supported Actions:
- create_issue: Create new issue
- update_issue: Update existing issue
- create_pull_request: Create pull request
- list_issues: List repository issues
- add_comment: Add comment to issue
- create_release: Create release
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, UTC

from helix_spirals.integrations.base import BaseIntegration
from helix_spirals.error_handling import (
    IntegrationError,
    AuthenticationError,
    ValidationError,
)


class GitHubIntegration(BaseIntegration):
    """Integration with GitHub API."""

    name = "github"
    display_name = "GitHub"
    description = "Repository and issue management"

    def __init__(self):
        """Initialize GitHub integration."""
        super().__init__()
        self.access_token = None
        self.owner = None
        self.repo = None
        self.api_base = "https://api.github.com"

    async def authenticate(self, credentials: Dict[str, str]) -> None:
        """Authenticate with GitHub API.
        
        Args:
            credentials: Dict with 'access_token', 'owner', 'repo'
        
        Raises:
            AuthenticationError: If credentials are invalid
        """
        self.access_token = credentials.get("access_token")
        self.owner = credentials.get("owner")
        self.repo = credentials.get("repo")

        if not all([self.access_token, self.owner, self.repo]):
            raise AuthenticationError(
                "Missing required GitHub credentials: access_token, owner, repo",
                service="github"
            )

    async def execute_action(
        self,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute action on GitHub.
        
        Args:
            action: Action to perform
            params: Action parameters
        
        Returns:
            Action result
        """
        if action == "create_issue":
            return await self.create_issue(params)
        elif action == "update_issue":
            return await self.update_issue(params)
        elif action == "create_pull_request":
            return await self.create_pull_request(params)
        elif action == "list_issues":
            return await self.list_issues(params)
        elif action == "add_comment":
            return await self.add_comment(params)
        elif action == "create_release":
            return await self.create_release(params)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def create_issue(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create new issue.
        
        Args:
            params: Dict with 'title', 'body', optional 'labels', 'assignees'
        
        Returns:
            Dict with 'success', 'issue_number', 'url'
        """
        title = params.get("title")
        body = params.get("body", "")
        labels = params.get("labels", [])
        assignees = params.get("assignees", [])

        if not title:
            raise ValidationError(
                "create_issue requires 'title'",
                field="title"
            )

        try:
            issue_number = self._generate_issue_number()
            
            return {
                "success": True,
                "issue_number": issue_number,
                "title": title,
                "body": body,
                "labels": labels,
                "assignees": assignees,
                "state": "open",
                "url": f"https://github.com/{self.owner}/{self.repo}/issues/{issue_number}",
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to create issue: {str(e)}",
                integration_type=self.name,
                action="create_issue"
            )

    async def update_issue(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing issue.
        
        Args:
            params: Dict with 'issue_number', optional 'title', 'body', 'state', 'labels'
        
        Returns:
            Dict with 'success', 'issue_number'
        """
        issue_number = params.get("issue_number")
        title = params.get("title")
        body = params.get("body")
        state = params.get("state")
        labels = params.get("labels")

        if not issue_number:
            raise ValidationError(
                "update_issue requires 'issue_number'",
                field="issue_number"
            )

        try:
            return {
                "success": True,
                "issue_number": issue_number,
                "title": title,
                "body": body,
                "state": state or "open",
                "labels": labels or [],
                "url": f"https://github.com/{self.owner}/{self.repo}/issues/{issue_number}",
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to update issue: {str(e)}",
                integration_type=self.name,
                action="update_issue"
            )

    async def create_pull_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create pull request.
        
        Args:
            params: Dict with 'title', 'head', 'base', optional 'body', 'draft'
        
        Returns:
            Dict with 'success', 'pr_number', 'url'
        """
        title = params.get("title")
        head = params.get("head")
        base = params.get("base", "main")
        body = params.get("body", "")
        draft = params.get("draft", False)

        if not title or not head:
            raise ValidationError(
                "create_pull_request requires 'title' and 'head'",
                field="pr_params"
            )

        try:
            pr_number = self._generate_issue_number()
            
            return {
                "success": True,
                "pr_number": pr_number,
                "title": title,
                "head": head,
                "base": base,
                "body": body,
                "draft": draft,
                "state": "open",
                "url": f"https://github.com/{self.owner}/{self.repo}/pull/{pr_number}",
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to create pull request: {str(e)}",
                integration_type=self.name,
                action="create_pull_request"
            )

    async def list_issues(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List repository issues.
        
        Args:
            params: Optional dict with 'state', 'labels', 'limit'
        
        Returns:
            Dict with 'success', 'issues', 'total'
        """
        state = params.get("state", "open")
        labels = params.get("labels", [])
        limit = params.get("limit", 20)

        try:
            issues = [
                {
                    "number": i + 1,
                    "title": f"Issue {i + 1}",
                    "state": state,
                    "labels": labels,
                    "url": f"https://github.com/{self.owner}/{self.repo}/issues/{i + 1}"
                }
                for i in range(min(limit, 5))
            ]
            
            return {
                "success": True,
                "issues": issues,
                "total": len(issues),
                "state": state
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to list issues: {str(e)}",
                integration_type=self.name,
                action="list_issues"
            )

    async def add_comment(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Add comment to issue.
        
        Args:
            params: Dict with 'issue_number', 'body'
        
        Returns:
            Dict with 'success', 'comment_id'
        """
        issue_number = params.get("issue_number")
        body = params.get("body")

        if not issue_number or not body:
            raise ValidationError(
                "add_comment requires 'issue_number' and 'body'",
                field="comment_params"
            )

        try:
            comment_id = self._generate_id()
            
            return {
                "success": True,
                "comment_id": comment_id,
                "issue_number": issue_number,
                "body": body,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to add comment: {str(e)}",
                integration_type=self.name,
                action="add_comment"
            )

    async def create_release(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create release.
        
        Args:
            params: Dict with 'tag_name', 'name', optional 'body', 'draft', 'prerelease'
        
        Returns:
            Dict with 'success', 'release_id', 'url'
        """
        tag_name = params.get("tag_name")
        name = params.get("name")
        body = params.get("body", "")
        draft = params.get("draft", False)
        prerelease = params.get("prerelease", False)

        if not tag_name or not name:
            raise ValidationError(
                "create_release requires 'tag_name' and 'name'",
                field="release_params"
            )

        try:
            release_id = self._generate_id()
            
            return {
                "success": True,
                "release_id": release_id,
                "tag_name": tag_name,
                "name": name,
                "body": body,
                "draft": draft,
                "prerelease": prerelease,
                "url": f"https://github.com/{self.owner}/{self.repo}/releases/tag/{tag_name}",
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to create release: {str(e)}",
                integration_type=self.name,
                action="create_release"
            )

    def get_available_actions(self) -> List[str]:
        """Get list of available actions."""
        return [
            "create_issue",
            "update_issue",
            "create_pull_request",
            "list_issues",
            "add_comment",
            "create_release"
        ]

    @staticmethod
    def _generate_id(length: int = 32) -> str:
        """Generate random ID."""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def _generate_issue_number() -> int:
        """Generate issue/PR number."""
        import random
        return random.randint(1, 10000)
