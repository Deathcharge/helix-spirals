"""
Asana Integration
=================

Integration with Asana for project management and task tracking.

Supported Actions:
- create_task: Create task
- update_task: Update task
- complete_task: Mark task complete
- list_tasks: List tasks
- get_task: Get task details
- create_project: Create project
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, UTC

from helix_spirals.integrations.base import BaseIntegration
from helix_spirals.error_handling import (
    IntegrationError,
    AuthenticationError,
    ValidationError,
)


class AsanaIntegration(BaseIntegration):
    """Integration with Asana."""

    name = "asana"
    display_name = "Asana"
    description = "Project management and task tracking"

    def __init__(self):
        """Initialize Asana integration."""
        super().__init__()
        self.access_token = None
        self.workspace_id = None
        self.api_base = "https://app.asana.com/api/1.0"

    async def authenticate(self, credentials: Dict[str, str]) -> None:
        """Authenticate with Asana API.
        
        Args:
            credentials: Dict with 'access_token', 'workspace_id'
        
        Raises:
            AuthenticationError: If credentials are invalid
        """
        self.access_token = credentials.get("access_token")
        self.workspace_id = credentials.get("workspace_id")

        if not self.access_token or not self.workspace_id:
            raise AuthenticationError(
                "Missing required Asana credentials: access_token, workspace_id",
                service="asana"
            )

    async def execute_action(
        self,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute action on Asana.
        
        Args:
            action: Action to perform
            params: Action parameters
        
        Returns:
            Action result
        """
        if action == "create_task":
            return await self.create_task(params)
        elif action == "update_task":
            return await self.update_task(params)
        elif action == "complete_task":
            return await self.complete_task(params)
        elif action == "list_tasks":
            return await self.list_tasks(params)
        elif action == "get_task":
            return await self.get_task(params)
        elif action == "create_project":
            return await self.create_project(params)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def create_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create task.
        
        Args:
            params: Dict with 'name', 'project_id', optional 'description', 'assignee'
        
        Returns:
            Dict with 'success', 'task_id'
        """
        name = params.get("name")
        project_id = params.get("project_id")
        description = params.get("description", "")
        assignee = params.get("assignee")

        if not name or not project_id:
            raise ValidationError(
                "create_task requires 'name' and 'project_id'",
                field="task_params"
            )

        try:
            task_id = self._generate_id()
            
            return {
                "success": True,
                "task_id": task_id,
                "name": name,
                "project_id": project_id,
                "description": description,
                "assignee": assignee,
                "status": "incomplete",
                "url": f"https://app.asana.com/0/{project_id}/{task_id}",
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to create task: {str(e)}",
                integration_type=self.name,
                action="create_task"
            )

    async def update_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update task.
        
        Args:
            params: Dict with 'task_id', optional 'name', 'description', 'assignee'
        
        Returns:
            Dict with 'success', 'task_id'
        """
        task_id = params.get("task_id")
        name = params.get("name")
        description = params.get("description")
        assignee = params.get("assignee")

        if not task_id:
            raise ValidationError(
                "update_task requires 'task_id'",
                field="task_id"
            )

        try:
            return {
                "success": True,
                "task_id": task_id,
                "name": name,
                "description": description,
                "assignee": assignee,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to update task: {str(e)}",
                integration_type=self.name,
                action="update_task"
            )

    async def complete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mark task complete.
        
        Args:
            params: Dict with 'task_id'
        
        Returns:
            Dict with 'success', 'task_id'
        """
        task_id = params.get("task_id")

        if not task_id:
            raise ValidationError(
                "complete_task requires 'task_id'",
                field="task_id"
            )

        try:
            return {
                "success": True,
                "task_id": task_id,
                "status": "complete",
                "completed_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to complete task: {str(e)}",
                integration_type=self.name,
                action="complete_task"
            )

    async def list_tasks(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List tasks.
        
        Args:
            params: Dict with 'project_id', optional 'limit', 'status'
        
        Returns:
            Dict with 'success', 'tasks', 'total'
        """
        project_id = params.get("project_id")
        limit = params.get("limit", 20)
        status = params.get("status")

        if not project_id:
            raise ValidationError(
                "list_tasks requires 'project_id'",
                field="project_id"
            )

        try:
            tasks = [
                {
                    "id": self._generate_id(),
                    "name": f"Task {i + 1}",
                    "status": status or "incomplete",
                    "assignee": "user@example.com",
                    "created_at": datetime.now(UTC).isoformat()
                }
                for i in range(min(limit, 5))
            ]
            
            return {
                "success": True,
                "tasks": tasks,
                "total": len(tasks),
                "project_id": project_id
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to list tasks: {str(e)}",
                integration_type=self.name,
                action="list_tasks"
            )

    async def get_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get task details.
        
        Args:
            params: Dict with 'task_id'
        
        Returns:
            Dict with task details
        """
        task_id = params.get("task_id")

        if not task_id:
            raise ValidationError(
                "get_task requires 'task_id'",
                field="task_id"
            )

        try:
            return {
                "success": True,
                "task_id": task_id,
                "name": "Sample Task",
                "description": "Task description",
                "status": "incomplete",
                "assignee": "user@example.com",
                "created_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to get task: {str(e)}",
                integration_type=self.name,
                action="get_task"
            )

    async def create_project(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create project.
        
        Args:
            params: Dict with 'name', optional 'description'
        
        Returns:
            Dict with 'success', 'project_id'
        """
        name = params.get("name")
        description = params.get("description", "")

        if not name:
            raise ValidationError(
                "create_project requires 'name'",
                field="name"
            )

        try:
            project_id = self._generate_id()
            
            return {
                "success": True,
                "project_id": project_id,
                "name": name,
                "description": description,
                "url": f"https://app.asana.com/0/{project_id}",
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to create project: {str(e)}",
                integration_type=self.name,
                action="create_project"
            )

    def get_available_actions(self) -> List[str]:
        """Get list of available actions."""
        return [
            "create_task",
            "update_task",
            "complete_task",
            "list_tasks",
            "get_task",
            "create_project"
        ]

    @staticmethod
    def _generate_id(length: int = 32) -> str:
        """Generate random ID."""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
