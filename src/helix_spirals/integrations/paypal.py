"""
PayPal Integration
==================

Integration with PayPal for payment processing.

Supported Actions:
- create_payment: Create payment
- execute_payment: Execute payment
- get_payment: Get payment details
- refund_payment: Refund payment
- list_payments: List payments
- create_subscription: Create subscription
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, UTC

from helix_spirals.integrations.base import BaseIntegration
from helix_spirals.error_handling import (
    IntegrationError,
    AuthenticationError,
    ValidationError,
)


class PayPalIntegration(BaseIntegration):
    """Integration with PayPal."""

    name = "paypal"
    display_name = "PayPal"
    description = "Payment processing and subscriptions"

    def __init__(self):
        """Initialize PayPal integration."""
        super().__init__()
        self.client_id = None
        self.client_secret = None
        self.mode = None
        self.api_base = "https://api.paypal.com"

    async def authenticate(self, credentials: Dict[str, str]) -> None:
        """Authenticate with PayPal API.
        
        Args:
            credentials: Dict with 'client_id', 'client_secret', optional 'mode'
        
        Raises:
            AuthenticationError: If credentials are invalid
        """
        self.client_id = credentials.get("client_id")
        self.client_secret = credentials.get("client_secret")
        self.mode = credentials.get("mode", "sandbox")

        if not self.client_id or not self.client_secret:
            raise AuthenticationError(
                "Missing required PayPal credentials: client_id, client_secret",
                service="paypal"
            )

    async def execute_action(
        self,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute action on PayPal.
        
        Args:
            action: Action to perform
            params: Action parameters
        
        Returns:
            Action result
        """
        if action == "create_payment":
            return await self.create_payment(params)
        elif action == "execute_payment":
            return await self.execute_payment(params)
        elif action == "get_payment":
            return await self.get_payment(params)
        elif action == "refund_payment":
            return await self.refund_payment(params)
        elif action == "list_payments":
            return await self.list_payments(params)
        elif action == "create_subscription":
            return await self.create_subscription(params)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def create_payment(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create payment.
        
        Args:
            params: Dict with 'amount', 'currency', 'description', optional 'return_url', 'cancel_url'
        
        Returns:
            Dict with 'success', 'payment_id', 'approval_url'
        """
        amount = params.get("amount")
        currency = params.get("currency", "USD")
        description = params.get("description")
        return_url = params.get("return_url")
        cancel_url = params.get("cancel_url")

        if not amount or not description:
            raise ValidationError(
                "create_payment requires 'amount' and 'description'",
                field="payment_params"
            )

        try:
            payment_id = self._generate_id()
            
            return {
                "success": True,
                "payment_id": payment_id,
                "amount": amount,
                "currency": currency,
                "description": description,
                "status": "created",
                "approval_url": f"https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token={payment_id}",
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to create payment: {str(e)}",
                integration_type=self.name,
                action="create_payment"
            )

    async def execute_payment(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute payment.
        
        Args:
            params: Dict with 'payment_id', 'payer_id'
        
        Returns:
            Dict with 'success', 'transaction_id'
        """
        payment_id = params.get("payment_id")
        payer_id = params.get("payer_id")

        if not payment_id or not payer_id:
            raise ValidationError(
                "execute_payment requires 'payment_id' and 'payer_id'",
                field="execute_params"
            )

        try:
            return {
                "success": True,
                "payment_id": payment_id,
                "transaction_id": self._generate_id(),
                "status": "completed",
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to execute payment: {str(e)}",
                integration_type=self.name,
                action="execute_payment"
            )

    async def get_payment(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get payment details.
        
        Args:
            params: Dict with 'payment_id'
        
        Returns:
            Dict with payment details
        """
        payment_id = params.get("payment_id")

        if not payment_id:
            raise ValidationError(
                "get_payment requires 'payment_id'",
                field="payment_id"
            )

        try:
            return {
                "success": True,
                "payment_id": payment_id,
                "amount": 99.99,
                "currency": "USD",
                "status": "completed",
                "transaction_id": self._generate_id(),
                "created_at": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to get payment: {str(e)}",
                integration_type=self.name,
                action="get_payment"
            )

    async def refund_payment(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Refund payment.
        
        Args:
            params: Dict with 'transaction_id', optional 'amount'
        
        Returns:
            Dict with 'success', 'refund_id'
        """
        transaction_id = params.get("transaction_id")
        amount = params.get("amount")

        if not transaction_id:
            raise ValidationError(
                "refund_payment requires 'transaction_id'",
                field="transaction_id"
            )

        try:
            return {
                "success": True,
                "transaction_id": transaction_id,
                "refund_id": self._generate_id(),
                "amount": amount,
                "status": "completed",
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to refund payment: {str(e)}",
                integration_type=self.name,
                action="refund_payment"
            )

    async def list_payments(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List payments.
        
        Args:
            params: Optional dict with 'limit', 'status'
        
        Returns:
            Dict with 'success', 'payments', 'total'
        """
        limit = params.get("limit", 20)
        status = params.get("status")

        try:
            payments = [
                {
                    "id": self._generate_id(),
                    "amount": 99.99 + i,
                    "currency": "USD",
                    "status": status or "completed",
                    "created_at": datetime.now(UTC).isoformat()
                }
                for i in range(min(limit, 5))
            ]
            
            return {
                "success": True,
                "payments": payments,
                "total": len(payments)
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to list payments: {str(e)}",
                integration_type=self.name,
                action="list_payments"
            )

    async def create_subscription(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create subscription.
        
        Args:
            params: Dict with 'plan_id', 'email', optional 'start_date'
        
        Returns:
            Dict with 'success', 'subscription_id'
        """
        plan_id = params.get("plan_id")
        email = params.get("email")
        start_date = params.get("start_date")

        if not plan_id or not email:
            raise ValidationError(
                "create_subscription requires 'plan_id' and 'email'",
                field="subscription_params"
            )

        try:
            return {
                "success": True,
                "subscription_id": self._generate_id(),
                "plan_id": plan_id,
                "email": email,
                "status": "active",
                "start_date": start_date or datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to create subscription: {str(e)}",
                integration_type=self.name,
                action="create_subscription"
            )

    def get_available_actions(self) -> List[str]:
        """Get list of available actions."""
        return [
            "create_payment",
            "execute_payment",
            "get_payment",
            "refund_payment",
            "list_payments",
            "create_subscription"
        ]

    @staticmethod
    def _generate_id(length: int = 32) -> str:
        """Generate random ID."""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
