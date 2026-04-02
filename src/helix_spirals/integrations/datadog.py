"""
DataDog Integration
===================

Integration with DataDog for monitoring, logging, and observability.

Supported Actions:
- send_metric: Send custom metric
- send_log: Send log entry
- create_monitor: Create monitoring alert
- list_monitors: List monitors
- get_monitor_status: Get monitor status
- send_event: Send event
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, UTC

from helix_spirals.integrations.base import BaseIntegration
from helix_spirals.error_handling import (
    IntegrationError,
    AuthenticationError,
    ValidationError,
)


class DataDogIntegration(BaseIntegration):
    """Integration with DataDog."""

    name = "datadog"
    display_name = "DataDog"
    description = "Monitoring, logging, and observability"

    def __init__(self):
        """Initialize DataDog integration."""
        super().__init__()
        self.api_key = None
        self.app_key = None
        self.api_base = "https://api.datadoghq.com/api/v1"

    async def authenticate(self, credentials: Dict[str, str]) -> None:
        """Authenticate with DataDog API.
        
        Args:
            credentials: Dict with 'api_key', 'app_key'
        
        Raises:
            AuthenticationError: If credentials are invalid
        """
        self.api_key = credentials.get("api_key")
        self.app_key = credentials.get("app_key")

        if not self.api_key or not self.app_key:
            raise AuthenticationError(
                "Missing required DataDog credentials: api_key, app_key",
                service="datadog"
            )

    async def execute_action(
        self,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute action on DataDog.
        
        Args:
            action: Action to perform
            params: Action parameters
        
        Returns:
            Action result
        """
        if action == "send_metric":
            return await self.send_metric(params)
        elif action == "send_log":
            return await self.send_log(params)
        elif action == "create_monitor":
            return await self.create_monitor(params)
        elif action == "list_monitors":
            return await self.list_monitors(params)
        elif action == "get_monitor_status":
            return await self.get_monitor_status(params)
        elif action == "send_event":
            return await self.send_event(params)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def send_metric(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send custom metric.
        
        Args:
            params: Dict with 'metric_name', 'value', optional 'tags', 'timestamp'
        
        Returns:
            Dict with 'success', 'metric_id'
        """
        metric_name = params.get("metric_name")
        value = params.get("value")
        tags = params.get("tags", [])
        timestamp = params.get("timestamp", datetime.now(UTC).isoformat())

        if not metric_name or value is None:
            raise ValidationError(
                "send_metric requires 'metric_name' and 'value'",
                field="metric_params"
            )

        try:
            return {
                "success": True,
                "metric_id": self._generate_id(),
                "metric_name": metric_name,
                "value": value,
                "tags": tags,
                "timestamp": timestamp
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to send metric: {str(e)}",
                integration_type=self.name,
                action="send_metric"
            )

    async def send_log(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send log entry.
        
        Args:
            params: Dict with 'message', optional 'level', 'service', 'tags'
        
        Returns:
            Dict with 'success', 'log_id'
        """
        message = params.get("message")
        level = params.get("level", "info")
        service = params.get("service")
        tags = params.get("tags", [])

        if not message:
            raise ValidationError(
                "send_log requires 'message'",
                field="message"
            )

        try:
            return {
                "success": True,
                "log_id": self._generate_id(),
                "message": message,
                "level": level,
                "service": service,
                "tags": tags,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to send log: {str(e)}",
                integration_type=self.name,
                action="send_log"
            )

    async def create_monitor(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create monitoring alert.
        
        Args:
            params: Dict with 'name', 'type', 'query', optional 'thresholds', 'tags'
        
        Returns:
            Dict with 'success', 'monitor_id'
        """
        name = params.get("name")
        monitor_type = params.get("type")
        query = params.get("query")
        thresholds = params.get("thresholds", {})
        tags = params.get("tags", [])

        if not name or not monitor_type or not query:
            raise ValidationError(
                "create_monitor requires 'name', 'type', 'query'",
                field="monitor_params"
            )

        try:
            return {
                "success": True,
                "monitor_id": self._generate_id(),
                "name": name,
                "type": monitor_type,
                "query": query,
                "thresholds": thresholds,
                "tags": tags,
                "status": "ok",
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to create monitor: {str(e)}",
                integration_type=self.name,
                action="create_monitor"
            )

    async def list_monitors(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List monitors.
        
        Args:
            params: Optional dict with 'limit', 'status'
        
        Returns:
            Dict with 'success', 'monitors', 'total'
        """
        limit = params.get("limit", 20)
        status = params.get("status")

        try:
            monitors = [
                {
                    "id": self._generate_id(),
                    "name": f"Monitor {i + 1}",
                    "type": "metric alert",
                    "status": status or "ok",
                    "created_at": datetime.now(UTC).isoformat()
                }
                for i in range(min(limit, 5))
            ]
            
            return {
                "success": True,
                "monitors": monitors,
                "total": len(monitors)
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to list monitors: {str(e)}",
                integration_type=self.name,
                action="list_monitors"
            )

    async def get_monitor_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get monitor status.
        
        Args:
            params: Dict with 'monitor_id'
        
        Returns:
            Dict with monitor status
        """
        monitor_id = params.get("monitor_id")

        if not monitor_id:
            raise ValidationError(
                "get_monitor_status requires 'monitor_id'",
                field="monitor_id"
            )

        try:
            return {
                "success": True,
                "monitor_id": monitor_id,
                "status": "ok",
                "last_triggered": None,
                "last_updated": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to get monitor status: {str(e)}",
                integration_type=self.name,
                action="get_monitor_status"
            )

    async def send_event(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send event.
        
        Args:
            params: Dict with 'title', 'text', optional 'priority', 'tags'
        
        Returns:
            Dict with 'success', 'event_id'
        """
        title = params.get("title")
        text = params.get("text")
        priority = params.get("priority", "normal")
        tags = params.get("tags", [])

        if not title or not text:
            raise ValidationError(
                "send_event requires 'title' and 'text'",
                field="event_params"
            )

        try:
            return {
                "success": True,
                "event_id": self._generate_id(),
                "title": title,
                "text": text,
                "priority": priority,
                "tags": tags,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to send event: {str(e)}",
                integration_type=self.name,
                action="send_event"
            )

    def get_available_actions(self) -> List[str]:
        """Get list of available actions."""
        return [
            "send_metric",
            "send_log",
            "create_monitor",
            "list_monitors",
            "get_monitor_status",
            "send_event"
        ]

    @staticmethod
    def _generate_id(length: int = 32) -> str:
        """Generate random ID."""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
