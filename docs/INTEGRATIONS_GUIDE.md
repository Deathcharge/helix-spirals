# Integrations Guide

Complete guide to all 22+ integrations available in Helix Spirals.

## Table of Contents

1. [Communication Integrations](#communication-integrations)
2. [Project Management Integrations](#project-management-integrations)
3. [Cloud & Data Integrations](#cloud--data-integrations)
4. [Using Integrations](#using-integrations)
5. [Integration Examples](#integration-examples)

---

## Communication Integrations

### Slack

Send messages and notifications to Slack channels.

**Available Actions:**
- `send_message`: Send message to channel
- `send_thread_message`: Reply in thread
- `send_embed`: Send rich embed
- `add_reaction`: Add emoji reaction

**Configuration:**
```python
await slack.authenticate({
    "webhook_url": "https://hooks.slack.com/services/...",
    "bot_token": "xoxb-..."  # Alternative to webhook
})
```

**Example:**
```python
result = await slack.send_message({
    "channel": "#alerts",
    "message": "Order #123 has been processed"
})
```

### Twilio

Send SMS, voice calls, and WhatsApp messages.

**Available Actions:**
- `send_sms`: Send SMS message
- `send_voice`: Make voice call
- `send_whatsapp`: Send WhatsApp message
- `get_message_status`: Get delivery status
- `list_messages`: List sent messages

**Configuration:**
```python
await twilio.authenticate({
    "account_sid": "AC...",
    "auth_token": "...",
    "from_number": "+1234567890"
})
```

**Example:**
```python
result = await twilio.send_sms({
    "to": "+1987654321",
    "message": "Your verification code is 123456"
})
```

### SendGrid

Send emails and manage contacts.

**Available Actions:**
- `send_email`: Send single email
- `send_bulk_email`: Send to multiple recipients
- `send_template_email`: Send using template
- `get_email_stats`: Get delivery statistics
- `add_contact`: Add contact to list

**Configuration:**
```python
await sendgrid.authenticate({
    "api_key": "SG.key...",
    "from_email": "noreply@example.com",
    "from_name": "Company"
})
```

**Example:**
```python
result = await sendgrid.send_email({
    "to": "user@example.com",
    "subject": "Welcome!",
    "html": "<h1>Welcome to our service</h1>"
})
```

### Discord

Send messages to Discord channels and servers.

**Available Actions:**
- `send_message`: Send message to channel
- `send_embed`: Send rich embed
- `send_thread_message`: Send in thread
- `create_thread`: Create new thread
- `add_reaction`: Add emoji reaction

**Configuration:**
```python
await discord.authenticate({
    "webhook_url": "https://discord.com/api/webhooks/...",
    "bot_token": "..."  # Alternative to webhook
})
```

**Example:**
```python
result = await discord.send_embed({
    "channel_id": "123456",
    "embed": {
        "title": "New Order",
        "description": "Order #123 received",
        "color": 3447003
    }
})
```

---

## Project Management Integrations

### GitHub

Manage repositories, issues, and pull requests.

**Available Actions:**
- `create_issue`: Create new issue
- `update_issue`: Update issue
- `create_pull_request`: Create PR
- `list_issues`: List issues
- `add_comment`: Add comment
- `create_release`: Create release

**Configuration:**
```python
await github.authenticate({
    "access_token": "ghp_...",
    "owner": "myuser",
    "repo": "myrepo"
})
```

**Example:**
```python
result = await github.create_issue({
    "title": "Bug: Login not working",
    "body": "Users cannot log in on mobile",
    "labels": ["bug", "critical"]
})
```

### Jira

Track issues and manage projects.

**Available Actions:**
- `create_issue`: Create issue
- `update_issue`: Update issue
- `transition_issue`: Change status
- `add_comment`: Add comment
- `search_issues`: Search with JQL
- `get_issue`: Get issue details

**Configuration:**
```python
await jira.authenticate({
    "domain": "mycompany",
    "email": "user@example.com",
    "api_token": "..."
})
```

**Example:**
```python
result = await jira.create_issue({
    "project_key": "PROJ",
    "issue_type": "Task",
    "summary": "Implement new feature",
    "priority": "High"
})
```

### Linear

Modern issue tracking and planning.

**Available Actions:**
- `create_issue`: Create issue
- `update_issue`: Update issue
- `add_comment`: Add comment
- `change_status`: Change status
- `list_issues`: List issues
- `get_issue`: Get issue details

**Configuration:**
```python
await linear.authenticate({
    "api_key": "lin_...",
    "team_key": "ENG"
})
```

**Example:**
```python
result = await linear.create_issue({
    "title": "Refactor authentication",
    "priority": 2,  # 0=No priority, 1=Urgent, 2=High, 3=Medium, 4=Low
    "assignee": "user@example.com"
})
```

---

## Cloud & Data Integrations

### AWS

Amazon Web Services integration for cloud operations.

**Available Actions:**
- `s3_upload`: Upload file to S3
- `s3_download`: Download from S3
- `lambda_invoke`: Invoke Lambda function
- `sns_publish`: Publish to SNS topic
- `sqs_send`: Send SQS message
- `dynamodb_put`: Put item in DynamoDB

**Configuration:**
```python
await aws.authenticate({
    "access_key_id": "AKIA...",
    "secret_access_key": "...",
    "region": "us-east-1"
})
```

**Example:**
```python
result = await aws.s3_upload({
    "bucket": "mybucket",
    "key": "uploads/document.pdf",
    "file_content": file_bytes
})
```

### Google Drive

File storage and collaboration.

**Available Actions:**
- `upload_file`: Upload file
- `download_file`: Download file
- `list_files`: List files
- `create_folder`: Create folder
- `share_file`: Share file
- `delete_file`: Delete file

**Configuration:**
```python
await google_drive.authenticate({
    "access_token": "ya29...."
})
```

**Example:**
```python
result = await google_drive.upload_file({
    "file_name": "report.pdf",
    "file_content": pdf_bytes,
    "folder_id": "folder_123"
})
```

### Airtable

Database and spreadsheet automation.

**Available Actions:**
- `create_record`: Create record
- `update_record`: Update record
- `delete_record`: Delete record
- `list_records`: List records
- `search_records`: Search records
- `get_record`: Get record details

**Configuration:**
```python
await airtable.authenticate({
    "api_key": "key...",
    "base_id": "app..."
})
```

**Example:**
```python
result = await airtable.create_record({
    "table_name": "Contacts",
    "fields": {
        "Name": "John Doe",
        "Email": "john@example.com",
        "Status": "Active"
    }
})
```

### Zapier

Connect to 5,000+ apps via Zapier.

**Available Actions:**
- `trigger_zap`: Trigger a Zap
- `get_zap_status`: Get execution status
- `list_zaps`: List Zaps
- `enable_zap`: Enable Zap
- `disable_zap`: Disable Zap

**Configuration:**
```python
await zapier.authenticate({
    "api_key": "zapier_..."
})
```

**Example:**
```python
result = await zapier.trigger_zap({
    "zap_id": "123",
    "data": {
        "name": "John Doe",
        "email": "john@example.com"
    }
})
```

---

## Using Integrations

### Basic Usage

```python
from helix_spirals.integrations.slack import SlackIntegration

# Create integration instance
slack = SlackIntegration()

# Authenticate
await slack.authenticate({
    "webhook_url": "https://hooks.slack.com/services/..."
})

# Execute action
result = await slack.send_message({
    "channel": "#alerts",
    "message": "Hello from Helix Spirals!"
})

print(result)  # {'success': True, 'message_id': '...', ...}
```

### In Workflows

```python
from helix_spirals import SpiralEngine, IntegrationNode

# Create integration node
slack_node = IntegrationNode(
    name="notify_slack",
    integration_type="slack",
    action="send_message",
    config={
        "channel": "#alerts",
        "message": "Order processed: ${order_id}"
    }
)

# Use in workflow
engine = SpiralEngine(storage=storage)
result = await engine.execute(slack_node, trigger_data={"order_id": "ORD-123"})
```

### Error Handling

```python
from helix_spirals.error_handling import IntegrationError

try:
    result = await slack.send_message({
        "channel": "#alerts",
        "message": "Test"
    })
except IntegrationError as e:
    print(f"Integration failed: {e.message}")
    # Handle error
```

---

## Integration Examples

### Example 1: Order Processing Workflow

```python
# Trigger: Webhook receives order
# Step 1: Validate order
# Step 2: Charge with Stripe
# Step 3: Send confirmation email (SendGrid)
# Step 4: Notify team (Slack)
# Step 5: Create issue in Jira
# Step 6: Upload receipt to S3 (AWS)

workflow = {
    "nodes": [
        {"type": "trigger", "trigger_type": "webhook"},
        {"type": "action", "action": "validate_order"},
        {"type": "integration", "integration": "stripe", "action": "charge"},
        {"type": "integration", "integration": "sendgrid", "action": "send_email"},
        {"type": "integration", "integration": "slack", "action": "send_message"},
        {"type": "integration", "integration": "jira", "action": "create_issue"},
        {"type": "integration", "integration": "aws", "action": "s3_upload"}
    ]
}
```

### Example 2: Lead Management

```python
# Trigger: New lead from form
# Step 1: Add to Airtable
# Step 2: Send welcome email (SendGrid)
# Step 3: Create Linear issue
# Step 4: Notify sales team (Discord)
# Step 5: Trigger Zapier workflow

workflow = {
    "nodes": [
        {"type": "trigger", "trigger_type": "webhook"},
        {"type": "integration", "integration": "airtable", "action": "create_record"},
        {"type": "integration", "integration": "sendgrid", "action": "send_email"},
        {"type": "integration", "integration": "linear", "action": "create_issue"},
        {"type": "integration", "integration": "discord", "action": "send_message"},
        {"type": "integration", "integration": "zapier", "action": "trigger_zap"}
    ]
}
```

### Example 3: Content Distribution

```python
# Trigger: Schedule (daily at 9 AM)
# Step 1: Fetch content from Notion
# Step 2: Generate captions with AI
# Step 3: Post to Twitter (via Zapier)
# Step 4: Post to LinkedIn (via Zapier)
# Step 5: Send summary email (SendGrid)

workflow = {
    "nodes": [
        {"type": "trigger", "trigger_type": "schedule", "cron": "0 9 * * *"},
        {"type": "integration", "integration": "notion", "action": "query_database"},
        {"type": "action", "action": "generate_captions"},
        {"type": "integration", "integration": "zapier", "action": "trigger_zap"},
        {"type": "integration", "integration": "zapier", "action": "trigger_zap"},
        {"type": "integration", "integration": "sendgrid", "action": "send_email"}
    ]
}
```

---

## Integration Status

| Integration | Status | Actions | Tested |
|-------------|--------|---------|--------|
| Slack | ✅ Production | 5 | ✅ Yes |
| Twilio | ✅ Production | 5 | ✅ Yes |
| SendGrid | ✅ Production | 5 | ✅ Yes |
| Discord | ✅ Production | 5 | ✅ Yes |
| GitHub | ✅ Production | 6 | ✅ Yes |
| Jira | ✅ Production | 6 | ✅ Yes |
| Linear | ✅ Production | 6 | ✅ Yes |
| AWS | ✅ Production | 6 | ✅ Yes |
| Google Drive | ✅ Production | 6 | ✅ Yes |
| Airtable | ✅ Production | 6 | ✅ Yes |
| Zapier | ✅ Production | 5 | ✅ Yes |
| Stripe | ✅ Production | 4 | ✅ Yes |
| Notion | ✅ Production | 4 | ✅ Yes |
| Email | ✅ Production | 3 | ✅ Yes |
| HTTP | ✅ Production | 2 | ✅ Yes |

---

## Adding Custom Integrations

To add a custom integration:

1. Create a new file in `src/helix_spirals/integrations/`
2. Extend `BaseIntegration` class
3. Implement required methods:
   - `authenticate(credentials)`
   - `execute_action(action, params)`
   - `get_available_actions()`
4. Add tests in `tests/test_integrations.py`
5. Document in this guide

**Template:**
```python
from helix_spirals.integrations.base import BaseIntegration

class MyServiceIntegration(BaseIntegration):
    name = "my_service"
    display_name = "My Service"
    description = "Integration with My Service"
    
    async def authenticate(self, credentials):
        # Implement authentication
        pass
    
    async def execute_action(self, action, params):
        # Implement action execution
        pass
    
    def get_available_actions(self):
        return ["action1", "action2"]
```

---

**Last Updated**: April 2, 2026  
**Version**: 2.0.0  
**Total Integrations**: 22+
