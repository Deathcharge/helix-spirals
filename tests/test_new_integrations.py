"""
New Integrations Tests
======================

Tests for newly added integrations (Twilio, SendGrid, Discord, GitHub, Jira, Linear, AWS, Google Drive, Airtable, Zapier).
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, UTC

from helix_spirals.integrations.twilio import TwilioIntegration
from helix_spirals.integrations.sendgrid import SendGridIntegration
from helix_spirals.integrations.discord import DiscordIntegration
from helix_spirals.integrations.github import GitHubIntegration
from helix_spirals.integrations.jira import JiraIntegration
from helix_spirals.integrations.linear import LinearIntegration
from helix_spirals.integrations.aws import AWSIntegration
from helix_spirals.integrations.google_drive import GoogleDriveIntegration
from helix_spirals.integrations.airtable import AirtableIntegration
from helix_spirals.integrations.zapier import ZapierIntegration
from helix_spirals.error_handling import (
    AuthenticationError,
    ValidationError,
    IntegrationError,
)


@pytest.mark.integration
class TestTwilioIntegration:
    """Tests for Twilio integration."""

    @pytest.fixture
    def twilio(self):
        """Create Twilio integration instance."""
        return TwilioIntegration()

    @pytest.mark.async
    async def test_authentication(self, twilio):
        """Test Twilio authentication."""
        await twilio.authenticate({
            "account_sid": "AC123",
            "auth_token": "token123",
            "from_number": "+1234567890"
        })
        assert twilio.account_sid == "AC123"

    @pytest.mark.async
    async def test_send_sms(self, twilio):
        """Test sending SMS."""
        await twilio.authenticate({
            "account_sid": "AC123",
            "auth_token": "token123",
            "from_number": "+1234567890"
        })
        
        result = await twilio.send_sms({
            "to": "+1987654321",
            "message": "Hello World"
        })
        
        assert result["success"] is True
        assert result["status"] == "queued"

    @pytest.mark.async
    async def test_send_sms_missing_params(self, twilio):
        """Test SMS with missing parameters."""
        await twilio.authenticate({
            "account_sid": "AC123",
            "auth_token": "token123",
            "from_number": "+1234567890"
        })
        
        with pytest.raises(ValidationError):
            await twilio.send_sms({"to": "+1987654321"})


@pytest.mark.integration
class TestSendGridIntegration:
    """Tests for SendGrid integration."""

    @pytest.fixture
    def sendgrid(self):
        """Create SendGrid integration instance."""
        return SendGridIntegration()

    @pytest.mark.async
    async def test_authentication(self, sendgrid):
        """Test SendGrid authentication."""
        await sendgrid.authenticate({
            "api_key": "SG.key123",
            "from_email": "sender@example.com"
        })
        assert sendgrid.api_key == "SG.key123"

    @pytest.mark.async
    async def test_send_email(self, sendgrid):
        """Test sending email."""
        await sendgrid.authenticate({
            "api_key": "SG.key123",
            "from_email": "sender@example.com"
        })
        
        result = await sendgrid.send_email({
            "to": "recipient@example.com",
            "subject": "Test Email",
            "html": "<p>Hello</p>"
        })
        
        assert result["success"] is True
        assert result["to"] == "recipient@example.com"

    @pytest.mark.async
    async def test_send_bulk_email(self, sendgrid):
        """Test sending bulk email."""
        await sendgrid.authenticate({
            "api_key": "SG.key123",
            "from_email": "sender@example.com"
        })
        
        result = await sendgrid.send_bulk_email({
            "recipients": ["user1@example.com", "user2@example.com"],
            "subject": "Bulk Email",
            "text": "Hello"
        })
        
        assert result["success"] is True
        assert result["count"] == 2


@pytest.mark.integration
class TestDiscordIntegration:
    """Tests for Discord integration."""

    @pytest.fixture
    def discord(self):
        """Create Discord integration instance."""
        return DiscordIntegration()

    @pytest.mark.async
    async def test_authentication(self, discord):
        """Test Discord authentication."""
        await discord.authenticate({
            "webhook_url": "https://discord.com/api/webhooks/123/abc"
        })
        assert discord.webhook_url == "https://discord.com/api/webhooks/123/abc"

    @pytest.mark.async
    async def test_send_message(self, discord):
        """Test sending Discord message."""
        await discord.authenticate({
            "webhook_url": "https://discord.com/api/webhooks/123/abc"
        })
        
        result = await discord.send_message({
            "channel_id": "123456",
            "message": "Hello Discord"
        })
        
        assert result["success"] is True
        assert result["message"] == "Hello Discord"

    @pytest.mark.async
    async def test_send_embed(self, discord):
        """Test sending Discord embed."""
        await discord.authenticate({
            "webhook_url": "https://discord.com/api/webhooks/123/abc"
        })
        
        result = await discord.send_embed({
            "channel_id": "123456",
            "embed": {
                "title": "Test Embed",
                "description": "Test description",
                "color": 3447003
            }
        })
        
        assert result["success"] is True
        assert result["embed"]["title"] == "Test Embed"


@pytest.mark.integration
class TestGitHubIntegration:
    """Tests for GitHub integration."""

    @pytest.fixture
    def github(self):
        """Create GitHub integration instance."""
        return GitHubIntegration()

    @pytest.mark.async
    async def test_authentication(self, github):
        """Test GitHub authentication."""
        await github.authenticate({
            "access_token": "ghp_token123",
            "owner": "myuser",
            "repo": "myrepo"
        })
        assert github.owner == "myuser"

    @pytest.mark.async
    async def test_create_issue(self, github):
        """Test creating GitHub issue."""
        await github.authenticate({
            "access_token": "ghp_token123",
            "owner": "myuser",
            "repo": "myrepo"
        })
        
        result = await github.create_issue({
            "title": "Bug Report",
            "body": "Found a bug"
        })
        
        assert result["success"] is True
        assert result["title"] == "Bug Report"

    @pytest.mark.async
    async def test_create_pull_request(self, github):
        """Test creating pull request."""
        await github.authenticate({
            "access_token": "ghp_token123",
            "owner": "myuser",
            "repo": "myrepo"
        })
        
        result = await github.create_pull_request({
            "title": "Add feature",
            "head": "feature-branch",
            "base": "main"
        })
        
        assert result["success"] is True
        assert result["state"] == "open"


@pytest.mark.integration
class TestJiraIntegration:
    """Tests for Jira integration."""

    @pytest.fixture
    def jira(self):
        """Create Jira integration instance."""
        return JiraIntegration()

    @pytest.mark.async
    async def test_authentication(self, jira):
        """Test Jira authentication."""
        await jira.authenticate({
            "domain": "mycompany",
            "email": "user@example.com",
            "api_token": "token123"
        })
        assert jira.domain == "mycompany"

    @pytest.mark.async
    async def test_create_issue(self, jira):
        """Test creating Jira issue."""
        await jira.authenticate({
            "domain": "mycompany",
            "email": "user@example.com",
            "api_token": "token123"
        })
        
        result = await jira.create_issue({
            "project_key": "PROJ",
            "issue_type": "Bug",
            "summary": "Test issue"
        })
        
        assert result["success"] is True
        assert "PROJ-" in result["issue_key"]

    @pytest.mark.async
    async def test_transition_issue(self, jira):
        """Test transitioning issue."""
        await jira.authenticate({
            "domain": "mycompany",
            "email": "user@example.com",
            "api_token": "token123"
        })
        
        result = await jira.transition_issue({
            "issue_key": "PROJ-1",
            "transition_name": "In Progress"
        })
        
        assert result["success"] is True
        assert result["new_status"] == "In Progress"


@pytest.mark.integration
class TestLinearIntegration:
    """Tests for Linear integration."""

    @pytest.fixture
    def linear(self):
        """Create Linear integration instance."""
        return LinearIntegration()

    @pytest.mark.async
    async def test_authentication(self, linear):
        """Test Linear authentication."""
        await linear.authenticate({
            "api_key": "lin_key123",
            "team_key": "ENG"
        })
        assert linear.team_key == "ENG"

    @pytest.mark.async
    async def test_create_issue(self, linear):
        """Test creating Linear issue."""
        await linear.authenticate({
            "api_key": "lin_key123",
            "team_key": "ENG"
        })
        
        result = await linear.create_issue({
            "title": "New feature"
        })
        
        assert result["success"] is True
        assert "ENG-" in result["issue_key"]

    @pytest.mark.async
    async def test_change_status(self, linear):
        """Test changing issue status."""
        await linear.authenticate({
            "api_key": "lin_key123",
            "team_key": "ENG"
        })
        
        result = await linear.change_status({
            "issue_id": "123",
            "status": "In Progress"
        })
        
        assert result["success"] is True
        assert result["new_status"] == "In Progress"


@pytest.mark.integration
class TestAWSIntegration:
    """Tests for AWS integration."""

    @pytest.fixture
    def aws(self):
        """Create AWS integration instance."""
        return AWSIntegration()

    @pytest.mark.async
    async def test_authentication(self, aws):
        """Test AWS authentication."""
        await aws.authenticate({
            "access_key_id": "AKIA123",
            "secret_access_key": "secret123",
            "region": "us-east-1"
        })
        assert aws.region == "us-east-1"

    @pytest.mark.async
    async def test_s3_upload(self, aws):
        """Test S3 upload."""
        await aws.authenticate({
            "access_key_id": "AKIA123",
            "secret_access_key": "secret123"
        })
        
        result = await aws.s3_upload({
            "bucket": "mybucket",
            "key": "file.txt",
            "file_content": b"content"
        })
        
        assert result["success"] is True
        assert "mybucket" in result["url"]

    @pytest.mark.async
    async def test_lambda_invoke(self, aws):
        """Test Lambda invocation."""
        await aws.authenticate({
            "access_key_id": "AKIA123",
            "secret_access_key": "secret123"
        })
        
        result = await aws.lambda_invoke({
            "function_name": "my-function",
            "payload": {"key": "value"}
        })
        
        assert result["success"] is True
        assert result["status_code"] == 200


@pytest.mark.integration
class TestGoogleDriveIntegration:
    """Tests for Google Drive integration."""

    @pytest.fixture
    def google_drive(self):
        """Create Google Drive integration instance."""
        return GoogleDriveIntegration()

    @pytest.mark.async
    async def test_authentication(self, google_drive):
        """Test Google Drive authentication."""
        await google_drive.authenticate({
            "access_token": "ya29.token123"
        })
        assert google_drive.access_token == "ya29.token123"

    @pytest.mark.async
    async def test_upload_file(self, google_drive):
        """Test uploading file to Drive."""
        await google_drive.authenticate({
            "access_token": "ya29.token123"
        })
        
        result = await google_drive.upload_file({
            "file_name": "document.pdf",
            "file_content": b"content"
        })
        
        assert result["success"] is True
        assert result["file_name"] == "document.pdf"

    @pytest.mark.async
    async def test_create_folder(self, google_drive):
        """Test creating folder."""
        await google_drive.authenticate({
            "access_token": "ya29.token123"
        })
        
        result = await google_drive.create_folder({
            "folder_name": "My Folder"
        })
        
        assert result["success"] is True
        assert result["folder_name"] == "My Folder"


@pytest.mark.integration
class TestAirtableIntegration:
    """Tests for Airtable integration."""

    @pytest.fixture
    def airtable(self):
        """Create Airtable integration instance."""
        return AirtableIntegration()

    @pytest.mark.async
    async def test_authentication(self, airtable):
        """Test Airtable authentication."""
        await airtable.authenticate({
            "api_key": "key123",
            "base_id": "appABC123"
        })
        assert airtable.base_id == "appABC123"

    @pytest.mark.async
    async def test_create_record(self, airtable):
        """Test creating record."""
        await airtable.authenticate({
            "api_key": "key123",
            "base_id": "appABC123"
        })
        
        result = await airtable.create_record({
            "table_name": "Contacts",
            "fields": {"Name": "John Doe", "Email": "john@example.com"}
        })
        
        assert result["success"] is True
        assert result["fields"]["Name"] == "John Doe"

    @pytest.mark.async
    async def test_search_records(self, airtable):
        """Test searching records."""
        await airtable.authenticate({
            "api_key": "key123",
            "base_id": "appABC123"
        })
        
        result = await airtable.search_records({
            "table_name": "Contacts",
            "field_name": "Email",
            "value": "john@example.com"
        })
        
        assert result["success"] is True
        assert len(result["records"]) > 0


@pytest.mark.integration
class TestZapierIntegration:
    """Tests for Zapier integration."""

    @pytest.fixture
    def zapier(self):
        """Create Zapier integration instance."""
        return ZapierIntegration()

    @pytest.mark.async
    async def test_authentication(self, zapier):
        """Test Zapier authentication."""
        await zapier.authenticate({
            "api_key": "zapier_key123"
        })
        assert zapier.api_key == "zapier_key123"

    @pytest.mark.async
    async def test_trigger_zap(self, zapier):
        """Test triggering Zap."""
        await zapier.authenticate({
            "api_key": "zapier_key123"
        })
        
        result = await zapier.trigger_zap({
            "zap_id": "123",
            "data": {"name": "John"}
        })
        
        assert result["success"] is True
        assert result["status"] == "triggered"

    @pytest.mark.async
    async def test_enable_zap(self, zapier):
        """Test enabling Zap."""
        await zapier.authenticate({
            "api_key": "zapier_key123"
        })
        
        result = await zapier.enable_zap({
            "zap_id": "123"
        })
        
        assert result["success"] is True
        assert result["status"] == "enabled"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
