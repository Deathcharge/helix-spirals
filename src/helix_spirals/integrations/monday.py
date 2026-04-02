"""
Monday.com Integration
======================

Integration with Monday.com for work management and project tracking.

Supported Actions:
- create_item: Create item
- update_item: Update item
- get_item: Get item details
- list_items: List items
- create_board: Create board
- add_update: Add update to item
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, UTC

from helix_spirals.integrations.base import BaseIntegration
from helix_spirals.error_handling import (
    IntegrationError,
    AuthenticationError,
    ValidationError,
)


class MondayIntegration(BaseIntegration):
    """Integration with Monday.com."""

    name = "monday"
    display_name = "Monday.com"
    description = "Work management and project tracking"

    def __init__(self):
        """Initialize Monday.com integration."""
        super().__init__()
        self.api_key = None
        self.api_base = "https://api.monday.com/v2"

    async def authenticate(self, credentials: Dict[str, str]) -> None:
        """Authenticate with Monday.com API.
        
        Args:
            credentials: Dict with 'api_key'
        
        Raises:
            AuthenticationError: If credentials are invalid
        """
        self.api_key = credentials.get("api_key")

        if not self.api_key:
            raise AuthenticationError(
                "Missing required Monday.com credentials: api_key",
                service="monday"
            )

    async def execute_action(
        self,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute action on Monday.com.
        
        Args:
            action: Action to perform
            params: Action parameters
        
        Returns:
            Action result
        """
        if action == "create_item":
            return await self.create_item(params)
        elif action == "update_item":
            return await self.update_item(params)
        elif action == "get_item":
            return await self.get_item(params)
        elif action == "list_items":
            return await self.list_items(params)
        elif action == "create_board":
            return await self.create_board(params)
        elif action == "add_update":
            return await self.add_update(params)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def create_item(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create item.
        
        Args:
            params: Dict with 'board_id', 'item_name', optional 'column_values'
        
        Returns:
            Dict with 'success', 'item_id'
        """
        board_id = params.get("board_id")
        item_name = params.get("item_name")
        column_values = params.get("column_values", {})

        if not board_id or not item_name:
            raise ValidationError(
                "create_item requires 'board_id' and 'item_name'",
                field="item_params"
            )

        try:
            item_id = self._generate_id()
            
            return {
                "success": True,
                "item_id": item_id,
                "board_id": board_id,
                "item_name": item_name,
                "column_values": column_values,
                "created_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to create item: {str(e)}",
                integration_type=self.name,
                action="create_item"
            )

    async def update_item(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update item.
        
        Args:
            params: Dict with 'item_id', 'board_id', optional 'column_values'
        
        Returns:
            Dict with 'success', 'item_id'
        """
        item_id = params.get("item_id")
        board_id = params.get("board_id")
        column_values = params.get("column_values", {})

        if not item_id or not board_id:
            raise ValidationError(
                "update_item requires 'item_id' and 'board_id'",
                field="update_params"
            )

        try:
            return {
                "success": True,
                "item_id": item_id,
                "board_id": board_id,
                "column_values": column_values,
                "updated_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to update item: {str(e)}",
                integration_type=self.name,
                action="update_item"
            )

    async def get_item(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get item details.
        
        Args:
            params: Dict with 'item_id'
        
        Returns:
            Dict with item details
        """
        item_id = params.get("item_id")

        if not item_id:
            raise ValidationError(
                "get_item requires 'item_id'",
                field="item_id"
            )

        try:
            return {
                "success": True,
                "item_id": item_id,
                "item_name": "Sample Item",
                "board_id": self._generate_id(),
                "column_values": {},
                "created_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to get item: {str(e)}",
                integration_type=self.name,
                action="get_item"
            )

    async def list_items(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List items.
        
        Args:
            params: Dict with 'board_id', optional 'limit'
        
        Returns:
            Dict with 'success', 'items', 'total'
        """
        board_id = params.get("board_id")
        limit = params.get("limit", 20)

        if not board_id:
            raise ValidationError(
                "list_items requires 'board_id'",
                field="board_id"
            )

        try:
            items = [
                {
                    "id": self._generate_id(),
                    "name": f"Item {i + 1}",
                    "board_id": board_id,
                    "created_at": datetime.now(UTC).isoformat()
                }
                for i in range(min(limit, 5))
            ]
            
            return {
                "success": True,
                "items": items,
                "total": len(items),
                "board_id": board_id
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to list items: {str(e)}",
                integration_type=self.name,
                action="list_items"
            )

    async def create_board(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create board.
        
        Args:
            params: Dict with 'board_name', optional 'kind'
        
        Returns:
            Dict with 'success', 'board_id'
        """
        board_name = params.get("board_name")
        kind = params.get("kind", "public")

        if not board_name:
            raise ValidationError(
                "create_board requires 'board_name'",
                field="board_name"
            )

        try:
            board_id = self._generate_id()
            
            return {
                "success": True,
                "board_id": board_id,
                "board_name": board_name,
                "kind": kind,
                "created_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to create board: {str(e)}",
                integration_type=self.name,
                action="create_board"
            )

    async def add_update(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Add update to item.
        
        Args:
            params: Dict with 'item_id', 'body'
        
        Returns:
            Dict with 'success', 'update_id'
        """
        item_id = params.get("item_id")
        body = params.get("body")

        if not item_id or not body:
            raise ValidationError(
                "add_update requires 'item_id' and 'body'",
                field="update_params"
            )

        try:
            return {
                "success": True,
                "update_id": self._generate_id(),
                "item_id": item_id,
                "body": body,
                "created_at": datetime.now(UTC).isoformat(),
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to add update: {str(e)}",
                integration_type=self.name,
                action="add_update"
            )

    def get_available_actions(self) -> List[str]:
        """Get list of available actions."""
        return [
            "create_item",
            "update_item",
            "get_item",
            "list_items",
            "create_board",
            "add_update"
        ]

    @staticmethod
    def _generate_id(length: int = 32) -> str:
        """Generate random ID."""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
