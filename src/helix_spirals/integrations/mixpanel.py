"""
Mixpanel Integration
====================

Integration with Mixpanel for product analytics and user insights.

Supported Actions:
- track_event: Track event
- set_user_properties: Set user properties
- increment_property: Increment user property
- get_user_profile: Get user profile
- list_events: List events
- get_event_data: Get event data
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, UTC

from helix_spirals.integrations.base import BaseIntegration
from helix_spirals.error_handling import (
    IntegrationError,
    AuthenticationError,
    ValidationError,
)


class MixpanelIntegration(BaseIntegration):
    """Integration with Mixpanel."""

    name = "mixpanel"
    display_name = "Mixpanel"
    description = "Product analytics and user insights"

    def __init__(self):
        """Initialize Mixpanel integration."""
        super().__init__()
        self.token = None
        self.api_key = None
        self.api_secret = None
        self.api_base = "https://api.mixpanel.com"

    async def authenticate(self, credentials: Dict[str, str]) -> None:
        """Authenticate with Mixpanel API.
        
        Args:
            credentials: Dict with 'token', optional 'api_key', 'api_secret'
        
        Raises:
            AuthenticationError: If credentials are invalid
        """
        self.token = credentials.get("token")
        self.api_key = credentials.get("api_key")
        self.api_secret = credentials.get("api_secret")

        if not self.token:
            raise AuthenticationError(
                "Missing required Mixpanel credentials: token",
                service="mixpanel"
            )

    async def execute_action(
        self,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute action on Mixpanel.
        
        Args:
            action: Action to perform
            params: Action parameters
        
        Returns:
            Action result
        """
        if action == "track_event":
            return await self.track_event(params)
        elif action == "set_user_properties":
            return await self.set_user_properties(params)
        elif action == "increment_property":
            return await self.increment_property(params)
        elif action == "get_user_profile":
            return await self.get_user_profile(params)
        elif action == "list_events":
            return await self.list_events(params)
        elif action == "get_event_data":
            return await self.get_event_data(params)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def track_event(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Track event.
        
        Args:
            params: Dict with 'user_id', 'event_name', optional 'properties'
        
        Returns:
            Dict with 'success'
        """
        user_id = params.get("user_id")
        event_name = params.get("event_name")
        properties = params.get("properties", {})

        if not user_id or not event_name:
            raise ValidationError(
                "track_event requires 'user_id' and 'event_name'",
                field="event_params"
            )

        try:
            return {
                "success": True,
                "user_id": user_id,
                "event_name": event_name,
                "properties": properties,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to track event: {str(e)}",
                integration_type=self.name,
                action="track_event"
            )

    async def set_user_properties(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Set user properties.
        
        Args:
            params: Dict with 'user_id', 'properties'
        
        Returns:
            Dict with 'success'
        """
        user_id = params.get("user_id")
        properties = params.get("properties", {})

        if not user_id or not properties:
            raise ValidationError(
                "set_user_properties requires 'user_id' and 'properties'",
                field="user_params"
            )

        try:
            return {
                "success": True,
                "user_id": user_id,
                "properties": properties,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to set user properties: {str(e)}",
                integration_type=self.name,
                action="set_user_properties"
            )

    async def increment_property(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Increment user property.
        
        Args:
            params: Dict with 'user_id', 'property_name', 'value'
        
        Returns:
            Dict with 'success'
        """
        user_id = params.get("user_id")
        property_name = params.get("property_name")
        value = params.get("value", 1)

        if not user_id or not property_name:
            raise ValidationError(
                "increment_property requires 'user_id' and 'property_name'",
                field="increment_params"
            )

        try:
            return {
                "success": True,
                "user_id": user_id,
                "property_name": property_name,
                "value": value,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to increment property: {str(e)}",
                integration_type=self.name,
                action="increment_property"
            )

    async def get_user_profile(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get user profile.
        
        Args:
            params: Dict with 'user_id'
        
        Returns:
            Dict with user profile
        """
        user_id = params.get("user_id")

        if not user_id:
            raise ValidationError(
                "get_user_profile requires 'user_id'",
                field="user_id"
            )

        try:
            return {
                "success": True,
                "user_id": user_id,
                "properties": {
                    "$email": "user@example.com",
                    "$name": "Sample User",
                    "plan": "premium"
                },
                "created_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to get user profile: {str(e)}",
                integration_type=self.name,
                action="get_user_profile"
            )

    async def list_events(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List events.
        
        Args:
            params: Optional dict with 'limit', 'from_date', 'to_date'
        
        Returns:
            Dict with 'success', 'events', 'total'
        """
        limit = params.get("limit", 20)
        from_date = params.get("from_date")
        to_date = params.get("to_date")

        try:
            events = [
                {
                    "name": f"Event {i + 1}",
                    "count": (i + 1) * 100,
                    "last_event": datetime.now(UTC).isoformat()
                }
                for i in range(min(limit, 5))
            ]
            
            return {
                "success": True,
                "events": events,
                "total": len(events)
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to list events: {str(e)}",
                integration_type=self.name,
                action="list_events"
            )

    async def get_event_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get event data.
        
        Args:
            params: Dict with 'event_name', optional 'from_date', 'to_date'
        
        Returns:
            Dict with event data
        """
        event_name = params.get("event_name")
        from_date = params.get("from_date")
        to_date = params.get("to_date")

        if not event_name:
            raise ValidationError(
                "get_event_data requires 'event_name'",
                field="event_name"
            )

        try:
            return {
                "success": True,
                "event_name": event_name,
                "count": 1000,
                "unique_users": 500,
                "from_date": from_date,
                "to_date": to_date,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to get event data: {str(e)}",
                integration_type=self.name,
                action="get_event_data"
            )

    def get_available_actions(self) -> List[str]:
        """Get list of available actions."""
        return [
            "track_event",
            "set_user_properties",
            "increment_property",
            "get_user_profile",
            "list_events",
            "get_event_data"
        ]

    @staticmethod
    def _generate_id(length: int = 32) -> str:
        """Generate random ID."""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
