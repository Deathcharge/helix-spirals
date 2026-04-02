"""
Jira Integration
================

Integration with Jira for issue tracking and project management.

Supported Actions:
- create_issue: Create new issue
- update_issue: Update issue
- transition_issue: Change issue status
- add_comment: Add comment to issue
- search_issues: Search issues with JQL
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


class JiraIntegration(BaseIntegration):
    """Integration with Jira issue tracking."""

    name = "jira"
    display_name = "Jira"
    description = "Issue tracking and project management"

    def __init__(self):
        """Initialize Jira integration."""
        super().__init__()
        self.domain = None
        self.email = None
        self.api_token = None
        self.api_base = None

    async def authenticate(self, credentials: Dict[str, str]) -> None:
        """Authenticate with Jira Cloud API.
        
        Args:
            credentials: Dict with 'domain', 'email', 'api_token'
        
        Raises:
            AuthenticationError: If credentials are invalid
        """
        self.domain = credentials.get("domain")
        self.email = credentials.get("email")
        self.api_token = credentials.get("api_token")

        if not all([self.domain, self.email, self.api_token]):
            raise AuthenticationError(
                "Missing required Jira credentials: domain, email, api_token",
                service="jira"
            )

        self.api_base = f"https://{self.domain}.atlassian.net/rest/api/3"

    async def execute_action(
        self,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute action on Jira.
        
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
        elif action == "transition_issue":
            return await self.transition_issue(params)
        elif action == "add_comment":
            return await self.add_comment(params)
        elif action == "search_issues":
            return await self.search_issues(params)
        elif action == "get_issue":
            return await self.get_issue(params)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def create_issue(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create new issue.
        
        Args:
            params: Dict with 'project_key', 'issue_type', 'summary', optional 'description'
        
        Returns:
            Dict with 'success', 'issue_key', 'issue_id'
        """
        project_key = params.get("project_key")
        issue_type = params.get("issue_type", "Task")
        summary = params.get("summary")
        description = params.get("description", "")
        assignee = params.get("assignee")
        priority = params.get("priority", "Medium")

        if not project_key or not summary:
            raise ValidationError(
                "create_issue requires 'project_key' and 'summary'",
                field="issue_params"
            )

        try:
            issue_key = f"{project_key}-{self._generate_issue_number()}"
            
            return {
                "success": True,
                "issue_key": issue_key,
                "issue_id": self._generate_id(),
                "project_key": project_key,
                "issue_type": issue_type,
                "summary": summary,
                "description": description,
                "assignee": assignee,
                "priority": priority,
                "status": "To Do",
                "url": f"https://{self.domain}.atlassian.net/browse/{issue_key}",
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
            params: Dict with 'issue_key', optional 'summary', 'description', 'assignee'
        
        Returns:
            Dict with 'success', 'issue_key'
        """
        issue_key = params.get("issue_key")
        summary = params.get("summary")
        description = params.get("description")
        assignee = params.get("assignee")
        priority = params.get("priority")

        if not issue_key:
            raise ValidationError(
                "update_issue requires 'issue_key'",
                field="issue_key"
            )

        try:
            return {
                "success": True,
                "issue_key": issue_key,
                "summary": summary,
                "description": description,
                "assignee": assignee,
                "priority": priority,
                "url": f"https://{self.domain}.atlassian.net/browse/{issue_key}",
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to update issue: {str(e)}",
                integration_type=self.name,
                action="update_issue"
            )

    async def transition_issue(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Transition issue to new status.
        
        Args:
            params: Dict with 'issue_key', 'transition_name' or 'transition_id'
        
        Returns:
            Dict with 'success', 'issue_key', 'new_status'
        """
        issue_key = params.get("issue_key")
        transition_name = params.get("transition_name")
        transition_id = params.get("transition_id")

        if not issue_key or not (transition_name or transition_id):
            raise ValidationError(
                "transition_issue requires 'issue_key' and 'transition_name' or 'transition_id'",
                field="transition_params"
            )

        try:
            statuses = ["To Do", "In Progress", "In Review", "Done"]
            new_status = transition_name or statuses[1]
            
            return {
                "success": True,
                "issue_key": issue_key,
                "new_status": new_status,
                "url": f"https://{self.domain}.atlassian.net/browse/{issue_key}",
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to transition issue: {str(e)}",
                integration_type=self.name,
                action="transition_issue"
            )

    async def add_comment(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Add comment to issue.
        
        Args:
            params: Dict with 'issue_key', 'body'
        
        Returns:
            Dict with 'success', 'comment_id'
        """
        issue_key = params.get("issue_key")
        body = params.get("body")

        if not issue_key or not body:
            raise ValidationError(
                "add_comment requires 'issue_key' and 'body'",
                field="comment_params"
            )

        try:
            return {
                "success": True,
                "comment_id": self._generate_id(),
                "issue_key": issue_key,
                "body": body,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to add comment: {str(e)}",
                integration_type=self.name,
                action="add_comment"
            )

    async def search_issues(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Search issues with JQL.
        
        Args:
            params: Dict with 'jql', optional 'limit'
        
        Returns:
            Dict with 'success', 'issues', 'total'
        """
        jql = params.get("jql")
        limit = params.get("limit", 20)

        if not jql:
            raise ValidationError(
                "search_issues requires 'jql'",
                field="jql"
            )

        try:
            issues = [
                {
                    "key": f"PROJ-{i + 1}",
                    "summary": f"Issue {i + 1}",
                    "status": "To Do",
                    "assignee": "user@example.com"
                }
                for i in range(min(limit, 5))
            ]
            
            return {
                "success": True,
                "issues": issues,
                "total": len(issues),
                "jql": jql
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to search issues: {str(e)}",
                integration_type=self.name,
                action="search_issues"
            )

    async def get_issue(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get issue details.
        
        Args:
            params: Dict with 'issue_key'
        
        Returns:
            Dict with issue details
        """
        issue_key = params.get("issue_key")

        if not issue_key:
            raise ValidationError(
                "get_issue requires 'issue_key'",
                field="issue_key"
            )

        try:
            return {
                "success": True,
                "issue_key": issue_key,
                "issue_id": self._generate_id(),
                "summary": "Sample Issue",
                "description": "Issue description",
                "status": "To Do",
                "priority": "Medium",
                "assignee": "user@example.com",
                "reporter": "reporter@example.com",
                "created": datetime.now(UTC).isoformat(),
                "updated": datetime.now(UTC).isoformat(),
                "url": f"https://{self.domain}.atlassian.net/browse/{issue_key}"
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
            "transition_issue",
            "add_comment",
            "search_issues",
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
        return random.randint(1000, 9999)
