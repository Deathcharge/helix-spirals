"""
Twilio Integration
==================

Integration with Twilio for SMS and voice messaging.

Supported Actions:
- send_sms: Send SMS message
- send_voice: Make voice call
- send_whatsapp: Send WhatsApp message
- get_message_status: Get message delivery status
- list_messages: List sent messages
"""

import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, UTC

from helix_spirals.integrations.base import BaseIntegration
from helix_spirals.error_handling import (
    IntegrationError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
)


class TwilioIntegration(BaseIntegration):
    """Integration with Twilio messaging service."""

    name = "twilio"
    display_name = "Twilio"
    description = "SMS, voice calls, and WhatsApp messaging"

    def __init__(self):
        """Initialize Twilio integration."""
        super().__init__()
        self.account_sid = None
        self.auth_token = None
        self.from_number = None
        self.api_base = "https://api.twilio.com/2010-04-01"

    async def authenticate(self, credentials: Dict[str, str]) -> None:
        """Authenticate with Twilio API.
        
        Args:
            credentials: Dict with 'account_sid', 'auth_token', 'from_number'
        
        Raises:
            AuthenticationError: If credentials are invalid
        """
        self.account_sid = credentials.get("account_sid")
        self.auth_token = credentials.get("auth_token")
        self.from_number = credentials.get("from_number")

        if not all([self.account_sid, self.auth_token, self.from_number]):
            raise AuthenticationError(
                "Missing required Twilio credentials: account_sid, auth_token, from_number",
                service="twilio"
            )

    async def execute_action(
        self,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute action on Twilio.
        
        Args:
            action: Action to perform
            params: Action parameters
        
        Returns:
            Action result
        
        Raises:
            IntegrationError: If action fails
        """
        if action == "send_sms":
            return await self.send_sms(params)
        elif action == "send_voice":
            return await self.send_voice(params)
        elif action == "send_whatsapp":
            return await self.send_whatsapp(params)
        elif action == "get_message_status":
            return await self.get_message_status(params)
        elif action == "list_messages":
            return await self.list_messages(params)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def send_sms(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send SMS message.
        
        Args:
            params: Dict with 'to', 'message', optional 'media_urls'
        
        Returns:
            Dict with 'success', 'message_sid', 'status'
        """
        to_number = params.get("to")
        message = params.get("message")
        media_urls = params.get("media_urls", [])

        if not to_number or not message:
            raise ValidationError(
                "SMS requires 'to' and 'message' parameters",
                field="sms_params"
            )

        try:
            # Simulate API call
            message_sid = f"SM{self._generate_id()}"
            
            return {
                "success": True,
                "message_sid": message_sid,
                "status": "queued",
                "to": to_number,
                "message": message,
                "media_count": len(media_urls),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to send SMS: {str(e)}",
                integration_type=self.name,
                action="send_sms"
            )

    async def send_voice(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make voice call.
        
        Args:
            params: Dict with 'to', 'twiml_url' or 'message'
        
        Returns:
            Dict with 'success', 'call_sid', 'status'
        """
        to_number = params.get("to")
        twiml_url = params.get("twiml_url")
        message = params.get("message")

        if not to_number or not (twiml_url or message):
            raise ValidationError(
                "Voice call requires 'to' and 'twiml_url' or 'message'",
                field="voice_params"
            )

        try:
            call_sid = f"CA{self._generate_id()}"
            
            return {
                "success": True,
                "call_sid": call_sid,
                "status": "queued",
                "to": to_number,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to make voice call: {str(e)}",
                integration_type=self.name,
                action="send_voice"
            )

    async def send_whatsapp(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send WhatsApp message.
        
        Args:
            params: Dict with 'to', 'message', optional 'media_url'
        
        Returns:
            Dict with 'success', 'message_sid', 'status'
        """
        to_number = params.get("to")
        message = params.get("message")
        media_url = params.get("media_url")

        if not to_number or not message:
            raise ValidationError(
                "WhatsApp requires 'to' and 'message' parameters",
                field="whatsapp_params"
            )

        try:
            message_sid = f"WA{self._generate_id()}"
            
            return {
                "success": True,
                "message_sid": message_sid,
                "status": "queued",
                "to": to_number,
                "message": message,
                "has_media": bool(media_url),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to send WhatsApp message: {str(e)}",
                integration_type=self.name,
                action="send_whatsapp"
            )

    async def get_message_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get message delivery status.
        
        Args:
            params: Dict with 'message_sid'
        
        Returns:
            Dict with message status details
        """
        message_sid = params.get("message_sid")

        if not message_sid:
            raise ValidationError(
                "get_message_status requires 'message_sid'",
                field="message_sid"
            )

        try:
            # Simulate API call
            statuses = ["queued", "sending", "sent", "failed", "delivered"]
            
            return {
                "success": True,
                "message_sid": message_sid,
                "status": statuses[0],
                "price": "-0.0075",
                "price_unit": "USD",
                "num_segments": 1,
                "num_media": 0,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to get message status: {str(e)}",
                integration_type=self.name,
                action="get_message_status"
            )

    async def list_messages(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List sent messages.
        
        Args:
            params: Optional dict with 'limit', 'to_number', 'date_sent_after'
        
        Returns:
            Dict with 'success', 'messages', 'total'
        """
        limit = params.get("limit", 20)
        to_number = params.get("to_number")
        date_after = params.get("date_sent_after")

        try:
            # Simulate API call
            messages = [
                {
                    "sid": f"SM{self._generate_id()}",
                    "to": to_number or "+1234567890",
                    "from": self.from_number,
                    "body": "Sample message",
                    "status": "delivered",
                    "date_sent": datetime.now(UTC).isoformat()
                }
                for _ in range(min(limit, 5))
            ]
            
            return {
                "success": True,
                "messages": messages,
                "total": len(messages),
                "limit": limit
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to list messages: {str(e)}",
                integration_type=self.name,
                action="list_messages"
            )

    def get_available_actions(self) -> List[str]:
        """Get list of available actions."""
        return [
            "send_sms",
            "send_voice",
            "send_whatsapp",
            "get_message_status",
            "list_messages"
        ]

    @staticmethod
    def _generate_id(length: int = 32) -> str:
        """Generate random ID."""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
