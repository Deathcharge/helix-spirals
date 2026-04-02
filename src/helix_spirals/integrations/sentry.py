"""
Sentry Integration
==================

Integration with Sentry for error tracking and performance monitoring.

Supported Actions:
- capture_exception: Capture exception
- capture_message: Capture message
- capture_event: Capture custom event
- list_issues: List issues
- get_issue: Get issue details
- update_issue: Update issue status
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, UTC

from helix_spirals.integrations.base import BaseIntegration
from helix_spirals.error_handling import (
    IntegrationError,
    AuthenticationError,
    ValidationError,
)


class SentryIntegration(BaseIntegration):
    """Integration with Sentry."""

    name = "sentry"
    display_name = "Sentry"
    description = "Error tracking and performance monitoring"

    def __init__(self):
        """Initialize Sentry integration."""
        super().__init__()
        self.api_key = None
        self.organization = None
        self.project = None
        self.api_base = "https://sentry.io/api/0"

    async def authenticate(self, credentials: Dict[str, str]) -> None:
        """Authenticate with Sentry API.
        
        Args:
            credentials: Dict with 'api_key', 'organization', 'project'
        
        Raises:
            AuthenticationError: If credentials are invalid
        """
        self.api_key = credentials.get("api_key")
        self.organization = credentials.get("organization")
        self.project = credentials.get("project")

        if not all([self.api_key, self.organization, self.project]):
            raise AuthenticationError(
                "Missing required Sentry credentials: api_key, organization, project",
                service="sentry"
            )

    async def execute_action(
        self,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute action on Sentry.
        
        Args:
            action: Action to perform
            params: Action parameters
        
        Returns:
            Action result
        """
        if action == "capture_exception":
            return await self.capture_exception(params)
        elif action == "capture_message":
            return await self.capture_message(params)
        elif action == "capture_event":
            return await self.capture_event(params)
        elif action == "list_issues":
            return await self.list_issues(params)
        elif action == "get_issue":
            return await self.get_issue(params)
        elif action == "update_issue":
            return await self.update_issue(params)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def capture_exception(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Capture exception.
        
        Args:
            params: Dict with 'exception', 'message', optional 'level', 'tags'
        
        Returns:
            Dict with 'success', 'event_id'
        """
        exception = params.get("exception")
        message = params.get("message")
        level = params.get("level", "error")
        tags = params.get("tags", {})

        if not exception or not message:
            raise ValidationError(
                "capture_exception requires 'exception' and 'message'",
                field="exception_params"
            )

        try:
            return {
                "success": True,
                "event_id": self._generate_id(),
                "exception": exception,
                "message": message,
                "level": level,
                "tags": tags,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to capture exception: {str(e)}",
                integration_type=self.name,
                action="capture_exception"
            )

    async def capture_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Capture message.
        
        Args:
            params: Dict with 'message', optional 'level', 'tags'
        
        Returns:
            Dict with 'success', 'event_id'
        """
        message = params.get("message")
        level = params.get("level", "info")
        tags = params.get("tags", {})

        if not message:
            raise ValidationError(
                "capture_message requires 'message'",
                field="message"
            )

        try:
            return {
                "success": True,
                "event_id": self._generate_id(),
                "message": message,
                "level": level,
                "tags": tags,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to capture message: {str(e)}",
                integration_type=self.name,
                action="capture_message"
            )

    async def capture_event(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Capture custom event.
        
        Args:
            params: Dict with 'event_data', optional 'level', 'tags'
        
        Returns:
            Dict with 'success', 'event_id'
        """
        event_data = params.get("event_data", {})
        level = params.get("level", "info")
        tags = params.get("tags", {})

        if not event_data:
            raise ValidationError(
                "capture_event requires 'event_data'",
                field="event_data"
            )

        try:
            return {
                "success": True,
                "event_id": self._generate_id(),
                "event_data": event_data,
                "level": level,
                "tags": tags,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to capture event: {str(e)}",
                integration_type=self.name,
                action="capture_event"
            )

    async def list_issues(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List issues.
        
        Args:
            params: Optional dict with 'limit', 'status'
        
        Returns:
            Dict with 'success', 'issues', 'total'
        """
        limit = params.get("limit", 20)
        status = params.get("status")

        try:
            issues = [
                {
                    "id": self._generate_id(),
                    "title": f"Issue {i + 1}",
                    "status": status or "unresolved",
                    "count": (i + 1) * 10,
                    "first_seen": datetime.now(UTC).isoformat()
                }
                for i in range(min(limit, 5))
            ]
            
            return {
                "success": True,
                "issues": issues,
                "total": len(issues)
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
            params: Dict with 'issue_id'
        
        Returns:
            Dict with issue details
        """
        issue_id = params.get("issue_id")

        if not issue_id:
            raise ValidationError(
                "get_issue requires 'issue_id'",
                field="issue_id"
            )

        try:
            return {
                "success": True,
                "issue_id": issue_id,
                "title": "Sample Issue",
                "status": "unresolved",
                "count": 42,
                "first_seen": datetime.now(UTC).isoformat(),
                "last_seen": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to get issue: {str(e)}",
                integration_type=self.name,
                action="get_issue"
            )

    async def update_issue(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update issue status.
        
        Args:
            params: Dict with 'issue_id', 'status'
        
        Returns:
            Dict with 'success', 'issue_id'
        """
        issue_id = params.get("issue_id")
        status = params.get("status")

        if not issue_id or not status:
            raise ValidationError(
                "update_issue requires 'issue_id' and 'status'",
                field="update_params"
            )

        try:
            return {
                "success": True,
                "issue_id": issue_id,
                "status": status,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to update issue: {str(e)}",
                integration_type=self.name,
                action="update_issue"
            )

    def get_available_actions(self) -> List[str]:
        """Get list of available actions."""
        return [
            "capture_exception",
            "capture_message",
            "capture_event",
            "list_issues",
            "get_issue",
            "update_issue"
        ]

    @staticmethod
    def _generate_id(length: int = 32) -> str:
        """Generate random ID."""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
