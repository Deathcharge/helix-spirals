# Helix Spirals API Reference

Complete API documentation for Helix Spirals workflow automation engine.

## Table of Contents

1. [Core Classes](#core-classes)
2. [Workflow Execution](#workflow-execution)
3. [Integration Nodes](#integration-nodes)
4. [Event Bus](#event-bus)
5. [Storage](#storage)
6. [Error Handling](#error-handling)

---

## Core Classes

### WorkflowEngine

The main execution engine for workflows.

```python
from helix_spirals import WorkflowEngine

engine = WorkflowEngine(storage=storage, ws_manager=ws_manager)
```

**Methods:**

#### `execute(spiral_id, trigger_type, trigger_data, metadata=None)`

Execute a workflow.

```python
result = await engine.execute(
    spiral_id="workflow_123",
    trigger_type="webhook",
    trigger_data={"order_id": "ORD-123"},
    metadata={"source": "api"}
)
```

**Parameters:**
- `spiral_id` (str): Unique workflow identifier
- `trigger_type` (str): Type of trigger (webhook, schedule, manual, etc.)
- `trigger_data` (dict): Data passed to the workflow
- `metadata` (dict, optional): Additional metadata

**Returns:**
- `ExecutionContext`: Execution result with status and outputs

#### `validate_workflow(workflow)`

Validate workflow structure.

```python
is_valid = engine.validate_workflow(workflow_definition)
```

**Parameters:**
- `workflow` (dict): Workflow definition

**Returns:**
- `bool`: True if valid, raises exception otherwise

---

### ExecutionContext

Represents the state of a workflow execution.

```python
from helix_spirals import ExecutionContext, ExecutionStatus

context = ExecutionContext(
    workflow_id="wf_123",
    execution_id="exec_456",
    status=ExecutionStatus.RUNNING,
    variables={"key": "value"},
    node_results={},
    errors=[]
)
```

**Attributes:**
- `workflow_id` (str): ID of the workflow
- `execution_id` (str): Unique execution ID
- `status` (ExecutionStatus): Current status
- `variables` (dict): Execution variables
- `node_results` (dict): Results from executed nodes
- `errors` (list): List of errors encountered
- `started_at` (datetime): Execution start time
- `completed_at` (datetime): Execution completion time

**Status Values:**
- `PENDING`: Waiting to start
- `RUNNING`: Currently executing
- `COMPLETED`: Successfully completed
- `FAILED`: Execution failed
- `CANCELLED`: Execution cancelled

---

### WorkflowNode

Represents a node in the workflow DAG.

```python
from helix_spirals import WorkflowNode

node = WorkflowNode(
    name="validate_order",
    node_type="action",
    action="validate_data",
    config={"schema": {...}}
)
```

**Parameters:**
- `name` (str): Unique node name
- `node_type` (str): Type of node (trigger, action, integration, conditional, etc.)
- `action` (str, optional): Action to perform
- `config` (dict, optional): Node configuration

**Methods:**

#### `connect_to(target_node)`

Connect this node to another node.

```python
node1.connect_to(node2)
```

#### `on_error(error_handler)`

Specify error handler for this node.

```python
node.on_error(error_handler_node)
```

---

### IntegrationNode

Represents an integration with external service.

```python
from helix_spirals import IntegrationNode, RetryPolicy

retry_policy = RetryPolicy(max_attempts=3)

node = IntegrationNode(
    name="send_slack",
    integration_type="slack",
    action="send_message",
    config={
        "channel": "#alerts",
        "message": "Hello!"
    },
    retry_policy=retry_policy
)
```

**Parameters:**
- `name` (str): Node name
- `integration_type` (str): Type of integration (slack, stripe, notion, etc.)
- `action` (str): Action to perform on the integration
- `config` (dict): Integration configuration
- `retry_policy` (RetryPolicy, optional): Retry configuration

---

## Workflow Execution

### Trigger Types

#### Webhook Trigger

```python
trigger = WorkflowNode(
    name="webhook_trigger",
    node_type="trigger",
    trigger_type="webhook",
    config={
        "path": "/orders",
        "method": "POST"
    }
)
```

#### Schedule Trigger

```python
trigger = WorkflowNode(
    name="scheduled_trigger",
    node_type="trigger",
    trigger_type="schedule",
    config={
        "schedule": "cron",
        "expression": "0 9 * * *",  # Daily at 9 AM
        "timezone": "UTC"
    }
)
```

#### Manual Trigger

```python
trigger = WorkflowNode(
    name="manual_trigger",
    node_type="trigger",
    trigger_type="manual"
)
```

#### Event Trigger

```python
trigger = WorkflowNode(
    name="event_trigger",
    node_type="trigger",
    trigger_type="event",
    config={
        "event_type": "order.created",
        "filter": {"status": "pending"}
    }
)
```

---

### Conditional Nodes

```python
from helix_spirals import ConditionalNode

condition = ConditionalNode(
    name="check_amount",
    condition=lambda ctx: ctx.get("amount", 0) > 100
)

condition.connect_true(high_value_path)
condition.connect_false(standard_path)
```

---

### Loop Nodes

```python
loop = WorkflowNode(
    name="process_items",
    node_type="loop",
    action="for_each",
    config={
        "items": "${items}",
        "parallel": False
    }
)
```

---

## Integration Nodes

### Slack Integration

```python
slack_node = IntegrationNode(
    name="send_slack",
    integration_type="slack",
    action="send_message",
    config={
        "channel": "#alerts",
        "message": "Alert: ${alert_message}",
        "thread_ts": "${thread_id}"
    }
)
```

**Available Actions:**
- `send_message`: Send a message to a channel
- `send_dm`: Send direct message
- `update_message`: Update existing message
- `add_reaction`: Add emoji reaction

### Stripe Integration

```python
stripe_node = IntegrationNode(
    name="charge_customer",
    integration_type="stripe",
    action="create_charge",
    config={
        "customer_id": "${customer_id}",
        "amount": "${amount}",
        "currency": "usd",
        "description": "Order #${order_id}"
    }
)
```

**Available Actions:**
- `create_charge`: Create a charge
- `create_customer`: Create customer
- `list_charges`: List charges
- `refund_charge`: Refund a charge

### Notion Integration

```python
notion_node = IntegrationNode(
    name="update_database",
    integration_type="notion",
    action="update_page",
    config={
        "page_id": "${page_id}",
        "properties": {
            "Status": {"select": {"name": "Done"}},
            "Updated": {"date": {"start": "${now}"}}
        }
    }
)
```

**Available Actions:**
- `query_database`: Query a database
- `get_page`: Get page details
- `update_page`: Update page properties
- `create_page`: Create new page

### Email Integration

```python
email_node = IntegrationNode(
    name="send_email",
    integration_type="email",
    action="send_email",
    config={
        "to": "${recipient_email}",
        "subject": "Order Confirmation",
        "template": "order_confirmation",
        "data": {
            "order_id": "${order_id}",
            "total": "${total_amount}"
        }
    }
)
```

**Available Actions:**
- `send_email`: Send email
- `send_bulk_email`: Send to multiple recipients
- `schedule_email`: Schedule email for later

### HTTP Integration

```python
http_node = IntegrationNode(
    name="call_api",
    integration_type="http",
    action="request",
    config={
        "method": "POST",
        "url": "https://api.example.com/webhook",
        "headers": {"Authorization": "Bearer ${api_key}"},
        "body": {"data": "${payload}"}
    }
)
```

**Available Actions:**
- `request`: Make HTTP request
- `get`: GET request
- `post`: POST request
- `put`: PUT request
- `delete`: DELETE request

---

## Event Bus

### EventBus

```python
from helix_spirals import EventBus, WorkflowTrigger

event_bus = EventBus()

# Register workflow
trigger = WorkflowTrigger(
    name="on_order_created",
    event_type="order.created",
    filter={"status": "pending"}
)

event_bus.register_workflow(trigger, workflow)

# Emit event
event_bus.emit("order.created", {
    "order_id": "ORD-123",
    "status": "pending"
})
```

**Methods:**

#### `register_workflow(trigger, workflow)`

Register a workflow to be triggered by events.

#### `emit(event_type, data)`

Emit an event to trigger registered workflows.

#### `subscribe(event_type, handler)`

Subscribe to events.

---

## Storage

### SpiralStorage

```python
from helix_spirals import SpiralStorage

storage = SpiralStorage(database_url="mysql://...")

# Save workflow
await storage.save_workflow(workflow_definition)

# Get workflow
workflow = await storage.get_workflow("workflow_123")

# Save execution
await storage.save_execution(execution_context)

# Get execution history
history = await storage.get_execution_history("workflow_123")
```

**Methods:**

#### `save_workflow(workflow)`

Save workflow definition.

#### `get_workflow(workflow_id)`

Retrieve workflow definition.

#### `save_execution(execution)`

Save execution record.

#### `get_execution_history(workflow_id, limit=100)`

Get execution history for a workflow.

---

## Error Handling

### Exception Types

```python
from helix_spirals.error_handling import (
    SpiralException,
    WorkflowExecutionError,
    IntegrationError,
    ValidationError,
    RateLimitError,
    TimeoutError,
    AuthenticationError
)
```

### Retry Policy

```python
from helix_spirals.error_handling import RetryPolicy

policy = RetryPolicy(
    max_attempts=3,
    backoff_strategy="exponential",
    initial_delay=1.0,
    max_delay=300.0,
    jitter=True,
    timeout=30.0
)
```

### Retry Decorator

```python
from helix_spirals.error_handling import retry

@retry(policy=policy)
async def call_external_service():
    return await service.request()
```

### Error Tracking

```python
from helix_spirals.error_handling import error_tracker

# Track error
error_tracker.track_error(error, workflow_id="wf_123")

# Get metrics
metrics = error_tracker.get_metrics()
error_rate = error_tracker.get_error_rate(window_minutes=60)
```

---

## Examples

### Example 1: Simple Workflow

```python
from helix_spirals import WorkflowEngine, WorkflowNode, IntegrationNode

engine = WorkflowEngine(storage=storage)

# Create nodes
trigger = WorkflowNode(name="start", node_type="trigger", trigger_type="manual")
slack = IntegrationNode(
    name="notify",
    integration_type="slack",
    action="send_message",
    config={"channel": "#alerts", "message": "Hello!"}
)
end = WorkflowNode(name="end", node_type="end")

# Connect
trigger.connect_to(slack)
slack.connect_to(end)

# Execute
result = await engine.execute(trigger, trigger_type="manual", trigger_data={})
```

### Example 2: Workflow with Retry

```python
from helix_spirals.error_handling import RetryPolicy

retry_policy = RetryPolicy(max_attempts=3, backoff_strategy="exponential")

stripe_node = IntegrationNode(
    name="charge",
    integration_type="stripe",
    action="create_charge",
    config={"customer_id": "${cus_id}", "amount": 9999},
    retry_policy=retry_policy
)
```

### Example 3: Conditional Workflow

```python
from helix_spirals import ConditionalNode

check = ConditionalNode(
    name="check_amount",
    condition=lambda ctx: ctx.get("amount", 0) > 100
)

check.connect_true(high_value_node)
check.connect_false(standard_node)
```

---

## Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=mysql://user:pass@localhost/spirals

# Redis (optional)
REDIS_URL=redis://localhost:6379

# API Keys
SLACK_API_KEY=xoxb-...
STRIPE_API_KEY=sk_...
NOTION_API_KEY=...
```

---

## Rate Limiting

Helix Spirals includes built-in rate limiting:

```python
from helix_spirals.engine import RateLimiter

limiter = RateLimiter(
    spiral_id="workflow_123",
    max_executions=10,
    window_ms=60000  # 1 minute
)

if await limiter.allow():
    # Execute workflow
    pass
```

---

**Last Updated**: April 2, 2026  
**Version**: 1.0.0
