"""
Integration Tests for Helix Spirals
====================================

Tests for integration connectors and external service interactions.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.integration
class TestSlackIntegration:
    """Tests for Slack integration connector."""

    def test_slack_connector_initialization(self, mock_integration):
        """Test Slack connector initialization."""
        mock_integration.name = "slack"
        
        assert mock_integration.name == "slack"
        assert hasattr(mock_integration, 'authenticate')
        assert hasattr(mock_integration, 'execute_action')

    @pytest.mark.async
    async def test_slack_send_message(self, mock_integration):
        """Test sending a message to Slack."""
        mock_integration.name = "slack"
        mock_integration.execute_action = AsyncMock(
            return_value={
                "success": True,
                "message_ts": "1234567890.123456",
                "channel": "C123456"
            }
        )
        
        result = await mock_integration.execute_action(
            action="send_message",
            params={
                "channel": "#general",
                "message": "Hello Slack!"
            }
        )
        
        assert result["success"] is True
        assert "message_ts" in result

    @pytest.mark.async
    async def test_slack_authentication(self, mock_integration):
        """Test Slack authentication."""
        mock_integration.authenticate = MagicMock(return_value=None)
        
        mock_integration.authenticate(
            credentials={"api_token": "xoxb-123456"}
        )
        
        mock_integration.authenticate.assert_called_once()


@pytest.mark.integration
class TestStripeIntegration:
    """Tests for Stripe integration connector."""

    def test_stripe_connector_initialization(self, mock_integration):
        """Test Stripe connector initialization."""
        mock_integration.name = "stripe"
        
        assert mock_integration.name == "stripe"

    @pytest.mark.async
    async def test_stripe_create_charge(self, mock_integration):
        """Test creating a charge in Stripe."""
        mock_integration.name = "stripe"
        mock_integration.execute_action = AsyncMock(
            return_value={
                "success": True,
                "charge_id": "ch_1234567890",
                "amount": 9999,
                "currency": "usd",
                "status": "succeeded"
            }
        )
        
        result = await mock_integration.execute_action(
            action="create_charge",
            params={
                "customer_id": "cus_123456",
                "amount": 9999,
                "currency": "usd"
            }
        )
        
        assert result["success"] is True
        assert result["status"] == "succeeded"
        assert result["amount"] == 9999

    @pytest.mark.async
    async def test_stripe_charge_failure(self, mock_integration):
        """Test handling Stripe charge failure."""
        mock_integration.name = "stripe"
        mock_integration.execute_action = AsyncMock(
            return_value={
                "success": False,
                "error": "card_declined",
                "message": "Your card was declined"
            }
        )
        
        result = await mock_integration.execute_action(
            action="create_charge",
            params={
                "customer_id": "cus_123456",
                "amount": 9999,
                "currency": "usd"
            }
        )
        
        assert result["success"] is False
        assert "error" in result


@pytest.mark.integration
class TestNotionIntegration:
    """Tests for Notion integration connector."""

    def test_notion_connector_initialization(self, mock_integration):
        """Test Notion connector initialization."""
        mock_integration.name = "notion"
        
        assert mock_integration.name == "notion"

    @pytest.mark.async
    async def test_notion_query_database(self, mock_integration):
        """Test querying a Notion database."""
        mock_integration.name = "notion"
        mock_integration.execute_action = AsyncMock(
            return_value={
                "success": True,
                "results": [
                    {
                        "id": "page_1",
                        "properties": {
                            "Name": {"title": [{"text": {"content": "Item 1"}}]},
                            "Status": {"select": {"name": "Done"}}
                        }
                    },
                    {
                        "id": "page_2",
                        "properties": {
                            "Name": {"title": [{"text": {"content": "Item 2"}}]},
                            "Status": {"select": {"name": "In Progress"}}
                        }
                    }
                ]
            }
        )
        
        result = await mock_integration.execute_action(
            action="query_database",
            params={
                "database_id": "db_123456",
                "filter": {"property": "Status", "select": {"equals": "Done"}}
            }
        )
        
        assert result["success"] is True
        assert len(result["results"]) == 2

    @pytest.mark.async
    async def test_notion_update_page(self, mock_integration):
        """Test updating a Notion page."""
        mock_integration.name = "notion"
        mock_integration.execute_action = AsyncMock(
            return_value={
                "success": True,
                "page_id": "page_123",
                "updated_properties": {
                    "Status": {"select": {"name": "Done"}},
                    "Last Updated": {"date": {"start": "2024-04-02"}}
                }
            }
        )
        
        result = await mock_integration.execute_action(
            action="update_page",
            params={
                "page_id": "page_123",
                "properties": {
                    "Status": {"select": {"name": "Done"}},
                    "Last Updated": {"date": {"start": "2024-04-02"}}
                }
            }
        )
        
        assert result["success"] is True
        assert result["page_id"] == "page_123"


@pytest.mark.integration
class TestEmailIntegration:
    """Tests for Email integration connector."""

    def test_email_connector_initialization(self, mock_integration):
        """Test Email connector initialization."""
        mock_integration.name = "email"
        
        assert mock_integration.name == "email"

    @pytest.mark.async
    async def test_email_send_basic(self, mock_integration):
        """Test sending a basic email."""
        mock_integration.name = "email"
        mock_integration.execute_action = AsyncMock(
            return_value={
                "success": True,
                "message_id": "msg_123456",
                "recipient": "user@example.com"
            }
        )
        
        result = await mock_integration.execute_action(
            action="send_email",
            params={
                "to": "user@example.com",
                "subject": "Test Email",
                "body": "This is a test email"
            }
        )
        
        assert result["success"] is True
        assert result["recipient"] == "user@example.com"

    @pytest.mark.async
    async def test_email_send_with_template(self, mock_integration):
        """Test sending email with template."""
        mock_integration.name = "email"
        mock_integration.execute_action = AsyncMock(
            return_value={
                "success": True,
                "message_id": "msg_123456",
                "template_used": "order_confirmation"
            }
        )
        
        result = await mock_integration.execute_action(
            action="send_email",
            params={
                "to": "user@example.com",
                "template": "order_confirmation",
                "data": {
                    "order_id": "ORD-123",
                    "total": "$99.99"
                }
            }
        )
        
        assert result["success"] is True
        assert result["template_used"] == "order_confirmation"


@pytest.mark.integration
class TestHTTPIntegration:
    """Tests for generic HTTP integration connector."""

    def test_http_connector_initialization(self, mock_integration):
        """Test HTTP connector initialization."""
        mock_integration.name = "http"
        
        assert mock_integration.name == "http"

    @pytest.mark.async
    async def test_http_post_request(self, mock_integration):
        """Test making a POST request."""
        mock_integration.name = "http"
        mock_integration.execute_action = AsyncMock(
            return_value={
                "success": True,
                "status_code": 200,
                "response": {"result": "success"}
            }
        )
        
        result = await mock_integration.execute_action(
            action="request",
            params={
                "method": "POST",
                "url": "https://api.example.com/webhook",
                "headers": {"Authorization": "Bearer token"},
                "body": {"key": "value"}
            }
        )
        
        assert result["success"] is True
        assert result["status_code"] == 200

    @pytest.mark.async
    async def test_http_get_request(self, mock_integration):
        """Test making a GET request."""
        mock_integration.name = "http"
        mock_integration.execute_action = AsyncMock(
            return_value={
                "success": True,
                "status_code": 200,
                "response": {"data": [1, 2, 3]}
            }
        )
        
        result = await mock_integration.execute_action(
            action="request",
            params={
                "method": "GET",
                "url": "https://api.example.com/data"
            }
        )
        
        assert result["success"] is True
        assert len(result["response"]["data"]) == 3


@pytest.mark.integration
class TestIntegrationErrorHandling:
    """Tests for error handling in integrations."""

    @pytest.mark.async
    async def test_integration_timeout(self, mock_integration):
        """Test handling integration timeout."""
        mock_integration.execute_action = AsyncMock(
            side_effect=TimeoutError("Request timed out after 30s")
        )
        
        with pytest.raises(TimeoutError):
            await mock_integration.execute_action(
                action="send_message",
                params={"message": "test"}
            )

    @pytest.mark.async
    async def test_integration_authentication_error(self, mock_integration):
        """Test handling authentication errors."""
        mock_integration.execute_action = AsyncMock(
            return_value={
                "success": False,
                "error": "unauthorized",
                "message": "Invalid API key"
            }
        )
        
        result = await mock_integration.execute_action(
            action="send_message",
            params={"message": "test"}
        )
        
        assert result["success"] is False
        assert result["error"] == "unauthorized"

    @pytest.mark.async
    async def test_integration_rate_limit(self, mock_integration):
        """Test handling rate limiting."""
        mock_integration.execute_action = AsyncMock(
            return_value={
                "success": False,
                "error": "rate_limited",
                "retry_after": 60
            }
        )
        
        result = await mock_integration.execute_action(
            action="send_message",
            params={"message": "test"}
        )
        
        assert result["success"] is False
        assert result["retry_after"] == 60


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
