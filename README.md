# Helix Spirals

**Open-source workflow automation engine for AI-driven integration orchestration.** Build, deploy, and scale complex multi-step workflows with 130+ pre-built integrations. Think of it as an open-source Zapier alternative designed specifically for AI agents, multi-agent systems, and intelligent automation.

![Status](https://img.shields.io/badge/status-production-green) ![License](https://img.shields.io/badge/license-Apache%202.0-blue) ![Python](https://img.shields.io/badge/python-3.9%2B-blue)

---

## What is Helix Spirals?

Helix Spirals is a **workflow automation engine** that enables developers to:

- **Define complex workflows** as directed acyclic graphs (DAGs) with conditional branching, loops, and error handling
- **Connect 130+ integrations** including Slack, Discord, Notion, Stripe, Mailchimp, Twilio, AWS, Google Cloud, and more
- **Orchestrate AI agents** to execute workflows with intelligent decision-making and meta-learning
- **Build marketplace templates** for reusable workflow patterns
- **Enable real-time event-driven automation** with webhooks and event buses
- **Optimize workflow performance** with built-in meta-learning and adaptive execution strategies

Perfect for:
- **Multi-agent AI systems** that need to coordinate across external services
- **Indie hackers** building automation tools without infrastructure overhead
- **Enterprise teams** requiring workflow orchestration with audit trails and compliance
- **AI researchers** studying workflow optimization and agent coordination

---

## Quick Start

### Installation

```bash
pip install helix-spirals
```

### Basic Usage

```python
from helix_spirals import WorkflowEngine, WorkflowNode, IntegrationNode

# Create a workflow engine
engine = WorkflowEngine()

# Define nodes
start = WorkflowNode(name="start", node_type="trigger", trigger_type="manual")
slack_notify = IntegrationNode(
    name="notify_slack",
    integration_type="slack",
    action="send_message",
    config={"channel": "#alerts", "message": "Workflow started"}
)
end = WorkflowNode(name="end", node_type="end")

# Connect nodes
start.connect_to(slack_notify)
slack_notify.connect_to(end)

# Execute workflow
result = engine.execute(start)
print(result)
```

### Workflow Templates

Use pre-built templates for common patterns:

```python
from helix_spirals.marketplace import WorkflowTemplates

# Social media automation
template = WorkflowTemplates.get("social_media_scheduler")
workflow = template.instantiate({
    "platforms": ["twitter", "linkedin"],
    "schedule": "daily",
    "content_source": "notion"
})

# E-commerce order processing
template = WorkflowTemplates.get("ecommerce_fulfillment")
workflow = template.instantiate({
    "payment_processor": "stripe",
    "fulfillment_service": "shopify",
    "notification_channel": "email"
})
```

---

## Core Features

### 1. Workflow Engine

- **DAG-based workflow definition** with Python or JSON
- **Conditional branching** (if/else, switch statements)
- **Loop support** (for-each, while loops)
- **Error handling** (try-catch, retry logic)
- **Parallel execution** for independent nodes
- **State management** across workflow steps

### 2. 130+ Pre-built Integrations

#### Communication
- Slack, Discord, Telegram, Twilio, SendGrid, Mailchimp

#### Productivity
- Notion, Airtable, Google Sheets, Calendly

#### E-commerce & Payment
- Stripe, Shopify, PayPal, Square

#### Cloud Platforms
- AWS, Google Cloud, Azure

#### Data & Analytics
- Mixpanel, Segment, Amplitude

#### Development
- GitHub, GitLab, Bitbucket

#### Custom Integrations
- Generic HTTP connector for any REST API

### 3. Integration Nodes

```python
# Slack integration
slack_node = IntegrationNode(
    name="send_slack_message",
    integration_type="slack",
    action="send_message",
    config={
        "channel": "#general",
        "message": "Hello from Spirals!",
        "thread_ts": "optional_thread_id"
    }
)

# Stripe integration
stripe_node = IntegrationNode(
    name="charge_customer",
    integration_type="stripe",
    action="create_charge",
    config={
        "customer_id": "cus_123",
        "amount": 9999,
        "currency": "usd"
    }
)

# Generic HTTP connector
http_node = IntegrationNode(
    name="call_custom_api",
    integration_type="http",
    action="request",
    config={
        "method": "POST",
        "url": "https://api.example.com/webhook",
        "headers": {"Authorization": "Bearer token"},
        "body": {"key": "value"}
    }
)
```

### 4. Event-Driven Architecture

```python
from helix_spirals import EventBus, WorkflowTrigger

# Create event bus
event_bus = EventBus()

# Define trigger
trigger = WorkflowTrigger(
    name="on_slack_message",
    event_type="slack.message_received",
    filter={"channel": "#orders"}
)

# Register workflow
event_bus.register_workflow(trigger, workflow)

# Events automatically trigger workflows
event_bus.emit("slack.message_received", {
    "channel": "#orders",
    "user": "customer",
    "text": "I want to order 5 units"
})
```

### 5. Meta-Learning & Optimization

```python
from helix_spirals import MetaLearningEngine

# Enable adaptive optimization
engine = WorkflowEngine(enable_meta_learning=True)

# Spirals learns from execution patterns
result = engine.execute(workflow)

# Get optimization recommendations
recommendations = engine.get_optimization_suggestions()
# Returns: parallelization opportunities, caching strategies, error patterns
```

### 6. Marketplace & Templates

```python
from helix_spirals.marketplace import WorkflowMarketplace

marketplace = WorkflowMarketplace()

# Browse templates
templates = marketplace.list_templates(category="social_media")

# Use community workflows
workflow = marketplace.get_template("twitter_to_notion_logger")

# Publish your own
marketplace.publish_template(my_workflow, {
    "name": "custom_workflow",
    "description": "My awesome workflow",
    "category": "custom",
    "version": "1.0.0"
})
```

### 7. Zapier Import

Migrate workflows from Zapier:

```python
from helix_spirals import ZapierImporter

importer = ZapierImporter(api_key="your_zapier_api_key")

# Import all your Zaps
workflows = importer.import_all_zaps()

# Convert to Spirals format
spirals_workflows = [importer.convert_zap(zap) for zap in workflows]
```

---

## Architecture

### Core Components

```
helix_spirals/
├── engine.py              # Workflow execution engine
├── models.py              # Data models (Workflow, Node, Connection)
├── actions.py             # Action definitions and handlers
├── integration_nodes.py    # Integration node implementations
├── event_bus.py           # Event-driven orchestration
├── meta_learning_engine.py # Optimization and learning
├── scheduler.py           # Workflow scheduling
├── storage.py             # Workflow persistence
├── integrations/          # 130+ integration connectors
│   ├── base.py           # Base integration class
│   ├── slack_connector.py
│   ├── stripe_connector.py
│   ├── notion_connector.py
│   └── ... (130+ more)
├── marketplace/           # Template marketplace
├── oauth/                 # OAuth credential management
├── versioning/            # Workflow versioning
└── routes.py             # FastAPI routes for REST API
```

### Execution Flow

```
Trigger Event
    ↓
Event Bus (matches trigger conditions)
    ↓
Workflow Engine (loads workflow DAG)
    ↓
Node Executor (processes each node)
    ├─ Action Nodes (execute logic)
    ├─ Integration Nodes (call external services)
    └─ Control Nodes (branching, loops)
    ↓
State Manager (tracks execution state)
    ↓
Meta-Learning Engine (learns from execution)
    ↓
Result Storage (persists outcomes)
```

---

## Advanced Usage

### Custom Integration

```python
from helix_spirals.integrations import BaseIntegration

class CustomIntegration(BaseIntegration):
    name = "my_service"
    
    def authenticate(self, credentials):
        self.api_key = credentials.get("api_key")
    
    def execute_action(self, action, params):
        if action == "create_item":
            return self._create_item(params)
        elif action == "list_items":
            return self._list_items(params)
    
    def _create_item(self, params):
        # Your custom logic
        pass
    
    def _list_items(self, params):
        # Your custom logic
        pass
```

### Conditional Workflows

```python
from helix_spirals import ConditionalNode

workflow = WorkflowEngine()

# Check order amount
check_amount = ConditionalNode(
    name="check_amount",
    condition=lambda ctx: ctx.get("order_amount", 0) > 100
)

# High-value order path
high_value_path = IntegrationNode(
    name="send_vip_notification",
    integration_type="slack",
    action="send_message"
)

# Standard path
standard_path = IntegrationNode(
    name="send_standard_notification",
    integration_type="email"
)

check_amount.connect_true(high_value_path)
check_amount.connect_false(standard_path)
```

### Error Handling & Retries

```python
from helix_spirals import RetryPolicy

# Define retry strategy
retry_policy = RetryPolicy(
    max_attempts=3,
    backoff_strategy="exponential",
    backoff_base=2,
    jitter=True
)

# Apply to integration node
stripe_charge = IntegrationNode(
    name="charge_customer",
    integration_type="stripe",
    retry_policy=retry_policy
)
```

---

## REST API

Helix Spirals ships with a FastAPI server for REST-based workflow management:

```bash
python -m helix_spirals.main
# Server runs on http://localhost:8000
```

### Endpoints

```
POST   /workflows              # Create workflow
GET    /workflows              # List workflows
GET    /workflows/{id}         # Get workflow
PUT    /workflows/{id}         # Update workflow
DELETE /workflows/{id}         # Delete workflow

POST   /workflows/{id}/execute # Execute workflow
GET    /workflows/{id}/runs    # Get execution history
GET    /workflows/{id}/runs/{run_id} # Get execution details

POST   /integrations/connect   # Connect integration
GET    /integrations           # List connected integrations
DELETE /integrations/{id}      # Disconnect integration

GET    /marketplace/templates  # Browse templates
POST   /marketplace/publish    # Publish template
```

---

## Performance & Optimization

### Built-in Optimizations

- **Parallel execution** for independent workflow branches
- **Caching** for repeated integration calls
- **Connection pooling** for external services
- **Batch processing** for bulk operations
- **Meta-learning** to identify optimization opportunities

### Benchmarks

- **Simple workflow** (3 nodes): ~200ms
- **Complex workflow** (20 nodes, 5 parallel branches): ~1.2s
- **Integration call** (Slack message): ~150ms
- **Marketplace lookup**: ~50ms

---

## Security & Compliance

- **Encrypted credential storage** with AES-256
- **OAuth 2.0 support** for secure integrations
- **Audit logging** for all workflow executions
- **RBAC** (Role-Based Access Control) for team management
- **SOC 2 compliance** ready

---

## Dual Licensing

Helix Spirals is available under two licenses:

1. **Apache 2.0** - For open-source projects and community use
2. **Proprietary License** - For commercial use with additional features

See [LICENSE](./LICENSE) and [LICENSE.PROPRIETARY](./LICENSE.PROPRIETARY) for details.

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
git clone https://github.com/Deathcharge/helix-spirals.git
cd helix-spirals
pip install -e ".[dev]"
pytest
```

---

## Roadmap

- [ ] **v2.0** - Visual workflow builder (web UI)
- [ ] **v2.1** - Mobile app for workflow monitoring
- [ ] **v2.2** - Advanced analytics and performance insights
- [ ] **v2.3** - AI-powered workflow suggestions
- [ ] **v3.0** - Distributed execution across multiple machines

---

## Community & Support

- **GitHub Issues**: [Report bugs](https://github.com/Deathcharge/helix-spirals/issues)
- **Discussions**: [Ask questions](https://github.com/Deathcharge/helix-spirals/discussions)
- **Documentation**: [Full docs](https://helix-spirals.dev)
- **Discord**: [Join community](https://discord.gg/helix-spirals)

---

## Acknowledgments

Helix Spirals is built on the foundation of the Helix ecosystem, which includes:

- **helix-orchestration** - Multi-agent coordination framework
- **helix-ethics** - Ethical AI governance framework
- **helix-creative-studio** - AI-powered story generation

---

## License

Licensed under the Apache License 2.0. See [LICENSE](./LICENSE) for details.

**Made with ❤️ by the Helix team**
