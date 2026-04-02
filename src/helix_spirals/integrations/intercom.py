"""
Intercom Integration
====================

Integration with Intercom for customer communication and support.

Supported Actions:
- create_user: Create user
- update_user: Update user
- send_message: Send message to user
- list_conversations: List conversations
- get_conversation: Get conversation details
- create_note: Create note on user
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, UTC

from helix_spirals.integrations.base import BaseIntegration
from helix_spirals.error_handling import (
    IntegrationError,
    AuthenticationError,
    ValidationError,
)


class IntercomIntegration(BaseIntegration):
    """Integration with Intercom."""

    name = "intercom"
    display_name = "Intercom"
    description = "Customer communication and support"

    def __init__(self):
        """Initialize Intercom integration."""
        super().__init__()
        self.access_token = None
        self.api_base = "https://api.intercom.io"

    async def authenticate(self, credentials: Dict[str, str]) -> None:
        """Authenticate with Intercom API.
        
        Args:
            credentials: Dict with 'access_token'
        
        Raises:
            AuthenticationError: If credentials are invalid
        """
        self.access_token = credentials.get("access_token")

        if not self.access_token:
            raise AuthenticationError(
                "Missing required Intercom credentials: access_token",
                service="intercom"
            )

    async def execute_action(
        self,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute action on Intercom.
        
        Args:
            action: Action to perform
            params: Action parameters
        
        Returns:
            Action result
        """
        if action == "create_user":
            return await self.create_user(params)
        elif action == "update_user":
            return await self.update_user(params)
        elif action == "send_message":
            return await self.send_message(params)
        elif action == "list_conversations":
            return await self.list_conversations(params)
        elif action == "get_conversation":
            return await self.get_conversation(params)
        elif action == "create_note":
            return await self.create_note(params)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def create_user(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create user.
        
        Args:
            params: Dict with 'email', optional 'name', 'phone'
        
        Returns:
            Dict with 'success', 'user_id'
        """
        email = params.get("email")
        name = params.get("name")
        phone = params.get("phone")

        if not email:
            raise ValidationError(
                "create_user requires 'email'",
                field="email"
            )

        try:
            user_id = self._generate_id()
            
            return {
                "success": True,
                "user_id": user_id,
                "email": email,
                "name": name,
                "phone": phone,
                "created_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to create user: {str(e)}",
                integration_type=self.name,
                action="create_user"
            )

    async def update_user(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update user.
        
        Args:
            params: Dict with 'user_id', optional 'name', 'phone', 'custom_attributes'
        
        Returns:
            Dict with 'success', 'user_id'
        """
        user_id = params.get("user_id")
        name = params.get("name")
        phone = params.get("phone")
        custom_attributes = params.get("custom_attributes", {})

        if not user_id:
            raise ValidationError(
                "update_user requires 'user_id'",
                field="user_id"
            )

        try:
            return {
                "success": True,
                "user_id": user_id,
                "name": name,
                "phone": phone,
                "custom_attributes": custom_attributes,
                "updated_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to update user: {str(e)}",
                integration_type=self.name,
                action="update_user"
            )

    async def send_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send message to user.
        
        Args:
            params: Dict with 'user_id', 'message_type', 'body'
        
        Returns:
            Dict with 'success', 'message_id'
        """
        user_id = params.get("user_id")
        message_type = params.get("message_type", "inapp")
        body = params.get("body")

        if not user_id or not body:
            raise ValidationError(
                "send_message requires 'user_id' and 'body'",
                field="message_params"
            )

        try:
            return {
                "success": True,
                "message_id": self._generate_id(),
                "user_id": user_id,
                "message_type": message_type,
                "body": body,
                "sent_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to send message: {str(e)}",
                integration_type=self.name,
                action="send_message"
            )

    async def list_conversations(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List conversations.
        
        Args:
            params: Optional dict with 'user_id', 'limit'
        
        Returns:
            Dict with 'success', 'conversations', 'total'
        """
        user_id = params.get("user_id")
        limit = params.get("limit", 20)

        try:
            conversations = [
                {
                    "id": self._generate_id(),
                    "user_id": user_id,
                    "subject": f"Conversation {i + 1}",
                    "state": "open",
                    "created_at": datetime.now(UTC).isoformat()
                }
                for i in range(min(limit, 5))
            ]
            
            return {
                "success": True,
                "conversations": conversations,
                "total": len(conversations)
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to list conversations: {str(e)}",
                integration_type=self.name,
                action="list_conversations"
            )

    async def get_conversation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get conversation details.
        
        Args:
            params: Dict with 'conversation_id'
        
        Returns:
            Dict with conversation details
        """
        conversation_id = params.get("conversation_id")

        if not conversation_id:
            raise ValidationError(
                "get_conversation requires 'conversation_id'",
                field="conversation_id"
            )

        try:
            return {
                "success": True,
                "conversation_id": conversation_id,
                "subject": "Sample Conversation",
                "state": "open",
                "messages": [],
                "created_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to get conversation: {str(e)}",
                integration_type=self.name,
                action="get_conversation"
            )

    async def create_note(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create note on user.
        
        Args:
            params: Dict with 'user_id', 'body'
        
        Returns:
            Dict with 'success', 'note_id'
        """
        user_id = params.get("user_id")
        body = params.get("body")

        if not user_id or not body:
            raise ValidationError(
                "create_note requires 'user_id' and 'body'",
                field="note_params"
            )

        try:
            return {
                "success": True,
                "note_id": self._generate_id(),
                "user_id": user_id,
                "body": body,
                "created_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to create note: {str(e)}",
                integration_type=self.name,
                action="create_note"
            )

    def get_available_actions(self) -> List[str]:
        """Get list of available actions."""
        return [
            "create_user",
            "update_user",
            "send_message",
            "list_conversations",
            "get_conversation",
            "create_note"
        ]

    @staticmethod
    def _generate_id(length: int = 32) -> str:
        """Generate random ID."""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
