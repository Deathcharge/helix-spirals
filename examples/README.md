# Helix Spirals Examples

This directory contains comprehensive, production-ready examples demonstrating various use cases and patterns for Helix Spirals workflow automation engine.

## Quick Navigation

| Example | File | Use Case | Complexity |
|---------|------|----------|-----------|
| Basic Workflow | `01_basic_workflow.py` | Simple notifications, context variables, parallel execution | Beginner |
| Order Processing | `02_order_processing.py` | E-commerce order fulfillment with payment, inventory, notifications | Intermediate |
| Social Media Automation | `03_social_media_automation.py` | Multi-platform content distribution with AI captions | Intermediate |

## Running the Examples

### Prerequisites

```bash
# Install helix-spirals
pip install helix-spirals

# Or install from source with dev dependencies
pip install -e ".[dev,integrations]"
```

### Running Individual Examples

```bash
# Basic workflow example
python examples/01_basic_workflow.py

# Order processing example
python examples/02_order_processing.py

# Social media automation example
python examples/03_social_media_automation.py
```

## Example 1: Basic Workflow

**File:** `01_basic_workflow.py`

Learn the fundamentals of Helix Spirals:

- **Basic Notification Workflow**: Send a message to Slack when triggered
- **Context Variables**: Pass data through workflow execution
- **Parallel Execution**: Execute independent nodes simultaneously

**Key Concepts:**
- Workflow nodes and connections
- Trigger types (manual, webhook)
- Integration nodes
- Execution context

**Use Cases:**
- Simple notifications
- Alert systems
- Basic automation

## Example 2: Order Processing

**File:** `02_order_processing.py`

A real-world e-commerce workflow demonstrating:

- **Webhook Triggers**: Receive orders via HTTP
- **Data Validation**: Validate order structure and content
- **Conditional Branching**: Different paths based on inventory
- **Error Handling**: Retry logic for payment processing
- **Multiple Integrations**: Stripe, Shopify, Email, Analytics
- **State Management**: Pass data through workflow steps

**Workflow Steps:**
1. Receive order via webhook
2. Validate order data
3. Check inventory (Shopify)
4. Process payment (Stripe) with retries
5. Update inventory
6. Send confirmation email
7. Log to analytics
8. Handle errors gracefully

**Key Concepts:**
- Conditional nodes
- Retry policies
- Error paths
- Integration configuration
- Context variable interpolation

**Use Cases:**
- E-commerce order processing
- Payment workflows
- Inventory management
- Customer notifications

## Example 3: Social Media Automation

**File:** `03_social_media_automation.py`

Automate content distribution across multiple platforms:

- **Scheduled Triggers**: Execute on a schedule (cron expressions)
- **Content Management**: Fetch drafts from Notion
- **AI Integration**: Generate platform-specific captions
- **Multi-Platform Distribution**: Post to Twitter, LinkedIn, Instagram
- **Parallel Execution**: Post to all platforms simultaneously
- **Status Tracking**: Update content management system
- **Analytics**: Track engagement metrics

**Workflow Steps:**
1. Scheduled trigger (daily at 9 AM)
2. Fetch draft posts from Notion
3. Loop through each post
4. Generate AI captions for each platform
5. Post to Twitter, LinkedIn, Instagram (parallel)
6. Update post status in Notion
7. Track metrics in analytics
8. Send summary email

**Key Concepts:**
- Scheduled triggers
- Loop nodes
- Parallel execution
- AI/LLM integration
- Multi-integration workflows
- Batch processing

**Use Cases:**
- Social media management
- Content distribution
- Marketing automation
- Engagement tracking

## Common Patterns

### 1. Error Handling with Retries

```python
from helix_spirals import RetryPolicy, IntegrationNode

retry_policy = RetryPolicy(
    max_attempts=3,
    backoff_strategy="exponential",
    backoff_base=2,
    jitter=True
)

node = IntegrationNode(
    name="call_api",
    integration_type="stripe",
    action="create_charge",
    retry_policy=retry_policy
)
```

### 2. Conditional Branching

```python
from helix_spirals import ConditionalNode

check = ConditionalNode(
    name="check_amount",
    condition=lambda ctx: ctx.get("amount", 0) > 100
)

check.connect_true(high_value_path)
check.connect_false(standard_path)
```

### 3. Parallel Execution

```python
# All three nodes execute in parallel
trigger.connect_to(slack_notify)
trigger.connect_to(email_notify)
trigger.connect_to(webhook_notify)

# All converge at end node
slack_notify.connect_to(end)
email_notify.connect_to(end)
webhook_notify.connect_to(end)
```

### 4. Loop Processing

```python
process_loop = WorkflowNode(
    name="process_items",
    node_type="loop",
    action="for_each",
    config={
        "items": "${items}",
        "parallel": False  # Sequential processing
    }
)
```

### 5. Context Variable Interpolation

```python
# Use ${variable_name} to reference context data
email_node = IntegrationNode(
    name="send_email",
    integration_type="email",
    action="send_email",
    config={
        "to": "${customer_email}",
        "subject": "Order #${order_id}",
        "body": "Total: ${total_amount}"
    }
)
```

## Integration Examples

### Slack

```python
slack_node = IntegrationNode(
    name="notify",
    integration_type="slack",
    action="send_message",
    config={
        "channel": "#alerts",
        "message": "Alert: ${alert_message}",
        "thread_ts": "${thread_id}"
    }
)
```

### Stripe

```python
stripe_node = IntegrationNode(
    name="charge",
    integration_type="stripe",
    action="create_charge",
    config={
        "customer_id": "${customer_id}",
        "amount": "${amount}",
        "currency": "usd"
    }
)
```

### Notion

```python
notion_node = IntegrationNode(
    name="update_database",
    integration_type="notion",
    action="update_page",
    config={
        "page_id": "${page_id}",
        "properties": {
            "Status": {"select": {"name": "Done"}},
            "Completed": {"date": {"start": "${now}"}}
        }
    }
)
```

### Email

```python
email_node = IntegrationNode(
    name="send_email",
    integration_type="email",
    action="send_email",
    config={
        "to": "${recipient_email}",
        "subject": "Notification",
        "template": "template_name",
        "data": {
            "name": "${user_name}",
            "content": "${message}"
        }
    }
)
```

## Best Practices

### 1. Validate Input Data

Always validate incoming data before processing:

```python
validate = WorkflowNode(
    name="validate",
    node_type="action",
    action="validate_data",
    config={
        "schema": {
            "email": "string",
            "amount": "number"
        },
        "required_fields": ["email", "amount"]
    }
)
```

### 2. Use Retry Policies for External APIs

Protect against transient failures:

```python
retry_policy = RetryPolicy(
    max_attempts=3,
    backoff_strategy="exponential",
    timeout=30
)
```

### 3. Implement Error Paths

Always handle failure scenarios:

```python
payment_node.on_error(handle_payment_failure)
handle_payment_failure.connect_to(error_end)
```

### 4. Log Important Events

Track workflow execution for debugging:

```python
track_event = IntegrationNode(
    name="track",
    integration_type="mixpanel",
    action="track_event",
    config={
        "event": "order_completed",
        "properties": {"order_id": "${order_id}"}
    }
)
```

### 5. Use Meaningful Node Names

Make workflows easy to understand and debug:

```python
# Good
validate_order = WorkflowNode(name="validate_order", ...)

# Avoid
node1 = WorkflowNode(name="step1", ...)
```

## Troubleshooting

### Workflow Not Triggering

- Check trigger configuration (webhook path, schedule expression)
- Verify trigger data matches expected schema
- Check logs for validation errors

### Integration Failures

- Verify API credentials are configured
- Check rate limits on external services
- Review error messages in execution logs

### Performance Issues

- Use parallel execution for independent nodes
- Implement caching for repeated API calls
- Consider batch processing for large datasets

## Next Steps

1. **Explore the Examples**: Run each example and modify them for your use case
2. **Read the Documentation**: Check `../docs/` for detailed API documentation
3. **Build Your Workflow**: Create your first workflow using these patterns
4. **Join the Community**: Share your workflows and examples

## Contributing

Have a great example? We'd love to include it!

1. Create a new example file: `0X_your_example.py`
2. Follow the format of existing examples
3. Include docstrings and comments
4. Add a section to this README
5. Submit a pull request

## Resources

- **Main Repository**: https://github.com/Deathcharge/helix-spirals
- **Documentation**: https://helix-spirals.dev
- **Issues & Discussions**: https://github.com/Deathcharge/helix-spirals/issues
- **Architecture Guide**: `../ARCHITECTURE.md`

---

**Last Updated**: April 2, 2026  
**Version**: 1.0.0
