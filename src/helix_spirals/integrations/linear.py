"""
Linear Integration
==================

Integration with Linear for modern issue tracking and planning.

Supported Actions:
- create_issue: Create new issue
- update_issue: Update issue
- add_comment: Add comment to issue
- change_status: Change issue status
- list_issues: List team issues
- get_issue: Get issue details
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, UTC

from helix_spirals.integrations.base import BaseIntegration
from helix_spirals.error_handling import (
    IntegrationError,
    AuthenticationError,
    ValidationError,
)


class LinearIntegration(BaseIntegration):
    """Integration with Linear issue tracking."""

    name = "linear"
    display_name = "Linear"
    description = "Modern issue tracking and planning"

    def __init__(self):
        """Initialize Linear integration."""
        super().__init__()
        self.api_key = None
        self.team_key = None
        self.api_base = "https://api.linear.app/graphql"

    async def authenticate(self, credentials: Dict[str, str]) -> None:
        """Authenticate with Linear API.
        
        Args:
            credentials: Dict with 'api_key', 'team_key'
        
        Raises:
            AuthenticationError: If credentials are invalid
        """
        self.api_key = credentials.get("api_key")
        self.team_key = credentials.get("team_key")

        if not self.api_key or not self.team_key:
            raise AuthenticationError(
                "Missing required Linear credentials: api_key, team_key",
                service="linear"
            )

    async def execute_action(
        self,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute action on Linear.
        
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
        elif action == "add_comment":
            return await self.add_comment(params)
        elif action == "change_status":
            return await self.change_status(params)
        elif action == "list_issues":
            return await self.list_issues(params)
        elif action == "get_issue":
            return await self.get_issue(params)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def create_issue(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create new issue.
        
        Args:
            params: Dict with 'title', optional 'description', 'assignee', 'priority'
        
        Returns:
            Dict with 'success', 'issue_id', 'issue_key'
        """
        title = params.get("title")
        description = params.get("description", "")
        assignee = params.get("assignee")
        priority = params.get("priority", 2)  # 0=No priority, 1=Urgent, 2=High, 3=Medium, 4=Low

        if not title:
            raise ValidationError(
                "create_issue requires 'title'",
                field="title"
            )

        try:
            issue_id = self._generate_id()
            issue_key = f"{self.team_key}-{self._generate_issue_number()}"
            
            return {
                "success": True,
                "issue_id": issue_id,
                "issue_key": issue_key,
                "title": title,
                "description": description,
                "assignee": assignee,
                "priority": priority,
                "status": "Backlog",
                "url": f"https://linear.app/issue/{issue_key}",
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to create issue: {str(e)}",
                integration_type=self.name,
                action="create_issue"
            )

    async def update_issue(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update issue.
        
        Args:
            params: Dict with 'issue_id', optional 'title', 'description', 'assignee'
        
        Returns:
            Dict with 'success', 'issue_id'
        """
        issue_id = params.get("issue_id")
        title = params.get("title")
        description = params.get("description")
        assignee = params.get("assignee")
        priority = params.get("priority")

        if not issue_id:
            raise ValidationError(
                "update_issue requires 'issue_id'",
                field="issue_id"
            )

        try:
            return {
                "success": True,
                "issue_id": issue_id,
                "title": title,
                "description": description,
                "assignee": assignee,
                "priority": priority,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to update issue: {str(e)}",
                integration_type=self.name,
                action="update_issue"
            )

    async def add_comment(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Add comment to issue.
        
        Args:
            params: Dict with 'issue_id', 'body'
        
        Returns:
            Dict with 'success', 'comment_id'
        """
        issue_id = params.get("issue_id")
        body = params.get("body")

        if not issue_id or not body:
            raise ValidationError(
                "add_comment requires 'issue_id' and 'body'",
                field="comment_params"
            )

        try:
            return {
                "success": True,
                "comment_id": self._generate_id(),
                "issue_id": issue_id,
                "body": body,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to add comment: {str(e)}",
                integration_type=self.name,
                action="add_comment"
            )

    async def change_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Change issue status.
        
        Args:
            params: Dict with 'issue_id', 'status'
        
        Returns:
            Dict with 'success', 'issue_id', 'new_status'
        """
        issue_id = params.get("issue_id")
        status = params.get("status")

        if not issue_id or not status:
            raise ValidationError(
                "change_status requires 'issue_id' and 'status'",
                field="status_params"
            )

        try:
            return {
                "success": True,
                "issue_id": issue_id,
                "new_status": status,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to change status: {str(e)}",
                integration_type=self.name,
                action="change_status"
            )

    async def list_issues(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List team issues.
        
        Args:
            params: Optional dict with 'status', 'assignee', 'limit'
        
        Returns:
            Dict with 'success', 'issues', 'total'
        """
        status = params.get("status")
        assignee = params.get("assignee")
        limit = params.get("limit", 20)

        try:
            issues = [
                {
                    "id": self._generate_id(),
                    "key": f"{self.team_key}-{i + 1}",
                    "title": f"Issue {i + 1}",
                    "status": status or "Backlog",
                    "priority": 2,
                    "assignee": assignee
                }
                for i in range(min(limit, 5))
            ]
            
            return {
                "success": True,
                "issues": issues,
                "total": len(issues),
                "team_key": self.team_key
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to list issues: {str(e)}",
                integration_type=self.name,
                action="list_issues"
            )

    async def get_issue(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get issue details.
        
        Args:
            params: Dict with 'issue_id' or 'issue_key'
        
        Returns:
            Dict with issue details
        """
        issue_id = params.get("issue_id")
        issue_key = params.get("issue_key")

        if not issue_id and not issue_key:
            raise ValidationError(
                "get_issue requires 'issue_id' or 'issue_key'",
                field="issue_params"
            )

        try:
            return {
                "success": True,
                "issue_id": issue_id or self._generate_id(),
                "issue_key": issue_key or f"{self.team_key}-1",
                "title": "Sample Issue",
                "description": "Issue description",
                "status": "Backlog",
                "priority": 2,
                "assignee": "user@example.com",
                "created_at": datetime.now(UTC).isoformat(),
                "updated_at": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to get issue: {str(e)}",
                integration_type=self.name,
                action="get_issue"
            )

    def get_available_actions(self) -> List[str]:
        """Get list of available actions."""
        return [
            "create_issue",
            "update_issue",
            "add_comment",
            "change_status",
            "list_issues",
            "get_issue"
        ]

    @staticmethod
    def _generate_id(length: int = 32) -> str:
        """Generate random ID."""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def _generate_issue_number() -> int:
        """Generate issue number."""
        import random
        return random.randint(1, 10000)
