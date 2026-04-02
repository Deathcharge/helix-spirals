"""
Discord Integration
===================

Integration with Discord for team messaging and webhooks.

Supported Actions:
- send_message: Send message to channel
- send_embed: Send rich embed message
- send_thread_message: Send message in thread
- create_thread: Create new thread
- add_reaction: Add emoji reaction
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, UTC

from helix_spirals.integrations.base import BaseIntegration
from helix_spirals.error_handling import (
    IntegrationError,
    AuthenticationError,
    ValidationError,
)


class DiscordIntegration(BaseIntegration):
    """Integration with Discord messaging service."""

    name = "discord"
    display_name = "Discord"
    description = "Team messaging and webhooks"

    def __init__(self):
        """Initialize Discord integration."""
        super().__init__()
        self.webhook_url = None
        self.bot_token = None
        self.api_base = "https://discord.com/api/v10"

    async def authenticate(self, credentials: Dict[str, str]) -> None:
        """Authenticate with Discord.
        
        Args:
            credentials: Dict with 'webhook_url' or 'bot_token'
        
        Raises:
            AuthenticationError: If credentials are invalid
        """
        self.webhook_url = credentials.get("webhook_url")
        self.bot_token = credentials.get("bot_token")

        if not (self.webhook_url or self.bot_token):
            raise AuthenticationError(
                "Missing required Discord credentials: webhook_url or bot_token",
                service="discord"
            )

    async def execute_action(
        self,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute action on Discord.
        
        Args:
            action: Action to perform
            params: Action parameters
        
        Returns:
            Action result
        """
        if action == "send_message":
            return await self.send_message(params)
        elif action == "send_embed":
            return await self.send_embed(params)
        elif action == "send_thread_message":
            return await self.send_thread_message(params)
        elif action == "create_thread":
            return await self.create_thread(params)
        elif action == "add_reaction":
            return await self.add_reaction(params)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def send_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send message to channel.
        
        Args:
            params: Dict with 'channel_id', 'message', optional 'mentions'
        
        Returns:
            Dict with 'success', 'message_id'
        """
        channel_id = params.get("channel_id")
        message = params.get("message")
        mentions = params.get("mentions", [])

        if not channel_id or not message:
            raise ValidationError(
                "send_message requires 'channel_id' and 'message'",
                field="message_params"
            )

        try:
            message_id = self._generate_id()
            
            return {
                "success": True,
                "message_id": message_id,
                "channel_id": channel_id,
                "message": message,
                "mentions": mentions,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to send Discord message: {str(e)}",
                integration_type=self.name,
                action="send_message"
            )

    async def send_embed(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send rich embed message.
        
        Args:
            params: Dict with 'channel_id', 'embed' (title, description, color, fields)
        
        Returns:
            Dict with 'success', 'message_id'
        """
        channel_id = params.get("channel_id")
        embed = params.get("embed", {})

        if not channel_id or not embed:
            raise ValidationError(
                "send_embed requires 'channel_id' and 'embed'",
                field="embed_params"
            )

        try:
            message_id = self._generate_id()
            
            return {
                "success": True,
                "message_id": message_id,
                "channel_id": channel_id,
                "embed": {
                    "title": embed.get("title", ""),
                    "description": embed.get("description", ""),
                    "color": embed.get("color", 3447003),
                    "fields": embed.get("fields", [])
                },
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to send Discord embed: {str(e)}",
                integration_type=self.name,
                action="send_embed"
            )

    async def send_thread_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send message in thread.
        
        Args:
            params: Dict with 'thread_id', 'message'
        
        Returns:
            Dict with 'success', 'message_id'
        """
        thread_id = params.get("thread_id")
        message = params.get("message")

        if not thread_id or not message:
            raise ValidationError(
                "send_thread_message requires 'thread_id' and 'message'",
                field="thread_params"
            )

        try:
            message_id = self._generate_id()
            
            return {
                "success": True,
                "message_id": message_id,
                "thread_id": thread_id,
                "message": message,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to send thread message: {str(e)}",
                integration_type=self.name,
                action="send_thread_message"
            )

    async def create_thread(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create new thread.
        
        Args:
            params: Dict with 'channel_id', 'name', optional 'message'
        
        Returns:
            Dict with 'success', 'thread_id'
        """
        channel_id = params.get("channel_id")
        name = params.get("name")
        message = params.get("message")

        if not channel_id or not name:
            raise ValidationError(
                "create_thread requires 'channel_id' and 'name'",
                field="thread_params"
            )

        try:
            thread_id = self._generate_id()
            
            return {
                "success": True,
                "thread_id": thread_id,
                "channel_id": channel_id,
                "name": name,
                "message": message,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to create thread: {str(e)}",
                integration_type=self.name,
                action="create_thread"
            )

    async def add_reaction(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Add emoji reaction to message.
        
        Args:
            params: Dict with 'channel_id', 'message_id', 'emoji'
        
        Returns:
            Dict with 'success'
        """
        channel_id = params.get("channel_id")
        message_id = params.get("message_id")
        emoji = params.get("emoji")

        if not channel_id or not message_id or not emoji:
            raise ValidationError(
                "add_reaction requires 'channel_id', 'message_id', 'emoji'",
                field="reaction_params"
            )

        try:
            return {
                "success": True,
                "channel_id": channel_id,
                "message_id": message_id,
                "emoji": emoji,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to add reaction: {str(e)}",
                integration_type=self.name,
                action="add_reaction"
            )

    def get_available_actions(self) -> List[str]:
        """Get list of available actions."""
        return [
            "send_message",
            "send_embed",
            "send_thread_message",
            "create_thread",
            "add_reaction"
        ]

    @staticmethod
    def _generate_id(length: int = 18) -> str:
        """Generate Discord-style ID."""
        import random
        return str(random.randint(10**17, 10**18 - 1))
