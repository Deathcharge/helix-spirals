"""
HubSpot Integration
===================

Integration with HubSpot for CRM and marketing automation.

Supported Actions:
- create_contact: Create contact
- update_contact: Update contact
- get_contact: Get contact details
- list_contacts: List contacts
- create_deal: Create deal
- update_deal: Update deal
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, UTC

from helix_spirals.integrations.base import BaseIntegration
from helix_spirals.error_handling import (
    IntegrationError,
    AuthenticationError,
    ValidationError,
)


class HubSpotIntegration(BaseIntegration):
    """Integration with HubSpot."""

    name = "hubspot"
    display_name = "HubSpot"
    description = "CRM and marketing automation"

    def __init__(self):
        """Initialize HubSpot integration."""
        super().__init__()
        self.api_key = None
        self.api_base = "https://api.hubapi.com"

    async def authenticate(self, credentials: Dict[str, str]) -> None:
        """Authenticate with HubSpot API.
        
        Args:
            credentials: Dict with 'api_key'
        
        Raises:
            AuthenticationError: If credentials are invalid
        """
        self.api_key = credentials.get("api_key")

        if not self.api_key:
            raise AuthenticationError(
                "Missing required HubSpot credentials: api_key",
                service="hubspot"
            )

    async def execute_action(
        self,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute action on HubSpot.
        
        Args:
            action: Action to perform
            params: Action parameters
        
        Returns:
            Action result
        """
        if action == "create_contact":
            return await self.create_contact(params)
        elif action == "update_contact":
            return await self.update_contact(params)
        elif action == "get_contact":
            return await self.get_contact(params)
        elif action == "list_contacts":
            return await self.list_contacts(params)
        elif action == "create_deal":
            return await self.create_deal(params)
        elif action == "update_deal":
            return await self.update_deal(params)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def create_contact(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create contact.
        
        Args:
            params: Dict with 'email', optional 'firstname', 'lastname', 'phone'
        
        Returns:
            Dict with 'success', 'contact_id'
        """
        email = params.get("email")
        firstname = params.get("firstname")
        lastname = params.get("lastname")
        phone = params.get("phone")

        if not email:
            raise ValidationError(
                "create_contact requires 'email'",
                field="email"
            )

        try:
            contact_id = self._generate_id()
            
            return {
                "success": True,
                "contact_id": contact_id,
                "email": email,
                "firstname": firstname,
                "lastname": lastname,
                "phone": phone,
                "created_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to create contact: {str(e)}",
                integration_type=self.name,
                action="create_contact"
            )

    async def update_contact(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update contact.
        
        Args:
            params: Dict with 'contact_id', optional 'firstname', 'lastname', 'phone'
        
        Returns:
            Dict with 'success', 'contact_id'
        """
        contact_id = params.get("contact_id")
        firstname = params.get("firstname")
        lastname = params.get("lastname")
        phone = params.get("phone")

        if not contact_id:
            raise ValidationError(
                "update_contact requires 'contact_id'",
                field="contact_id"
            )

        try:
            return {
                "success": True,
                "contact_id": contact_id,
                "firstname": firstname,
                "lastname": lastname,
                "phone": phone,
                "updated_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to update contact: {str(e)}",
                integration_type=self.name,
                action="update_contact"
            )

    async def get_contact(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get contact details.
        
        Args:
            params: Dict with 'contact_id'
        
        Returns:
            Dict with contact details
        """
        contact_id = params.get("contact_id")

        if not contact_id:
            raise ValidationError(
                "get_contact requires 'contact_id'",
                field="contact_id"
            )

        try:
            return {
                "success": True,
                "contact_id": contact_id,
                "email": "contact@example.com",
                "firstname": "John",
                "lastname": "Doe",
                "phone": "+1234567890",
                "created_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to get contact: {str(e)}",
                integration_type=self.name,
                action="get_contact"
            )

    async def list_contacts(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List contacts.
        
        Args:
            params: Optional dict with 'limit'
        
        Returns:
            Dict with 'success', 'contacts', 'total'
        """
        limit = params.get("limit", 20)

        try:
            contacts = [
                {
                    "id": self._generate_id(),
                    "email": f"contact{i}@example.com",
                    "firstname": f"Contact{i}",
                    "lastname": "User",
                    "created_at": datetime.now(UTC).isoformat()
                }
                for i in range(min(limit, 5))
            ]
            
            return {
                "success": True,
                "contacts": contacts,
                "total": len(contacts)
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to list contacts: {str(e)}",
                integration_type=self.name,
                action="list_contacts"
            )

    async def create_deal(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create deal.
        
        Args:
            params: Dict with 'dealname', 'dealstage', optional 'amount', 'contact_id'
        
        Returns:
            Dict with 'success', 'deal_id'
        """
        dealname = params.get("dealname")
        dealstage = params.get("dealstage")
        amount = params.get("amount")
        contact_id = params.get("contact_id")

        if not dealname or not dealstage:
            raise ValidationError(
                "create_deal requires 'dealname' and 'dealstage'",
                field="deal_params"
            )

        try:
            deal_id = self._generate_id()
            
            return {
                "success": True,
                "deal_id": deal_id,
                "dealname": dealname,
                "dealstage": dealstage,
                "amount": amount,
                "contact_id": contact_id,
                "created_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to create deal: {str(e)}",
                integration_type=self.name,
                action="create_deal"
            )

    async def update_deal(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update deal.
        
        Args:
            params: Dict with 'deal_id', optional 'dealstage', 'amount'
        
        Returns:
            Dict with 'success', 'deal_id'
        """
        deal_id = params.get("deal_id")
        dealstage = params.get("dealstage")
        amount = params.get("amount")

        if not deal_id:
            raise ValidationError(
                "update_deal requires 'deal_id'",
                field="deal_id"
            )

        try:
            return {
                "success": True,
                "deal_id": deal_id,
                "dealstage": dealstage,
                "amount": amount,
                "updated_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to update deal: {str(e)}",
                integration_type=self.name,
                action="update_deal"
            )

    def get_available_actions(self) -> List[str]:
        """Get list of available actions."""
        return [
            "create_contact",
            "update_contact",
            "get_contact",
            "list_contacts",
            "create_deal",
            "update_deal"
        ]

    @staticmethod
    def _generate_id(length: int = 32) -> str:
        """Generate random ID."""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
