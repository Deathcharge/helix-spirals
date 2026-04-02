"""
Basic Workflow Example
======================

This example demonstrates the fundamental concepts of Helix Spirals:
- Creating a simple workflow
- Defining nodes and connections
- Executing the workflow
- Handling results

Use case: A basic notification workflow that sends a message to Slack
when triggered manually.
"""

from helix_spirals import WorkflowEngine, WorkflowNode, IntegrationNode


def example_basic_notification_workflow():
    """Create and execute a basic notification workflow."""
    
    # Initialize the workflow engine
    engine = WorkflowEngine()
    
    # Define the trigger node (manual trigger)
    trigger = WorkflowNode(
        name="start",
        node_type="trigger",
        trigger_type="manual",
        description="Manual trigger to start the workflow"
    )
    
    # Define an integration node to send a Slack message
    slack_notify = IntegrationNode(
        name="notify_slack",
        integration_type="slack",
        action="send_message",
        config={
            "channel": "#notifications",
            "message": "Workflow executed successfully!",
            "thread_ts": None  # Optional: reply in thread
        },
        description="Send notification to Slack channel"
    )
    
    # Define the end node
    end = WorkflowNode(
        name="end",
        node_type="end",
        description="Workflow completion"
    )
    
    # Connect nodes to form the workflow DAG
    trigger.connect_to(slack_notify)
    slack_notify.connect_to(end)
    
    # Execute the workflow
    try:
        result = engine.execute(trigger)
        print(f"✅ Workflow executed successfully")
        print(f"   Result: {result}")
        return result
    except Exception as e:
        print(f"❌ Workflow execution failed: {e}")
        raise


def example_workflow_with_context():
    """Demonstrate passing data through workflow execution context."""
    
    engine = WorkflowEngine()
    
    # Trigger with input data
    trigger = WorkflowNode(
        name="trigger",
        node_type="trigger",
        trigger_type="webhook",
        config={
            "path": "/notify",
            "method": "POST"
        }
    )
    
    # Extract and validate input
    validate = WorkflowNode(
        name="validate_input",
        node_type="action",
        action="validate_data",
        config={
            "schema": {
                "user_email": "string",
                "message": "string"
            }
        }
    )
    
    # Send email with validated data
    send_email = IntegrationNode(
        name="send_email",
        integration_type="email",
        action="send_email",
        config={
            "to": "${user_email}",  # Reference from context
            "subject": "Notification from Helix Spirals",
            "body": "${message}",   # Reference from context
            "html": False
        }
    )
    
    # Connect workflow
    trigger.connect_to(validate)
    validate.connect_to(send_email)
    
    print("✅ Workflow with context created")
    print("   Trigger: webhook at /notify")
    print("   Action: validate input data")
    print("   Integration: send email with context variables")


def example_parallel_workflow():
    """Demonstrate parallel execution of independent nodes."""
    
    engine = WorkflowEngine()
    
    # Trigger
    trigger = WorkflowNode(
        name="trigger",
        node_type="trigger",
        trigger_type="manual"
    )
    
    # Multiple notification channels (can execute in parallel)
    slack_notify = IntegrationNode(
        name="notify_slack",
        integration_type="slack",
        action="send_message",
        config={"channel": "#alerts", "message": "Alert!"}
    )
    
    discord_notify = IntegrationNode(
        name="notify_discord",
        integration_type="discord",
        action="send_message",
        config={"channel": "alerts", "message": "Alert!"}
    )
    
    email_notify = IntegrationNode(
        name="notify_email",
        integration_type="email",
        action="send_email",
        config={
            "to": "admin@example.com",
            "subject": "Alert",
            "body": "Alert triggered!"
        }
    )
    
    # Merge point
    end = WorkflowNode(
        name="end",
        node_type="end"
    )
    
    # Connect: trigger branches to all three notifications (parallel)
    # then all converge at end
    trigger.connect_to(slack_notify)
    trigger.connect_to(discord_notify)
    trigger.connect_to(email_notify)
    
    slack_notify.connect_to(end)
    discord_notify.connect_to(end)
    email_notify.connect_to(end)
    
    print("✅ Parallel workflow created")
    print("   Trigger → [Slack, Discord, Email] → End")
    print("   All notifications execute in parallel for efficiency")


if __name__ == "__main__":
    print("=" * 60)
    print("Helix Spirals - Basic Workflow Examples")
    print("=" * 60)
    print()
    
    print("Example 1: Basic Notification Workflow")
    print("-" * 60)
    example_basic_notification_workflow()
    print()
    
    print("Example 2: Workflow with Context Variables")
    print("-" * 60)
    example_workflow_with_context()
    print()
    
    print("Example 3: Parallel Execution")
    print("-" * 60)
    example_parallel_workflow()
    print()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)
