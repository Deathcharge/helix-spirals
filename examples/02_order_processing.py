"""
Order Processing Workflow Example
==================================

This example demonstrates a real-world use case: processing customer orders
with payment, inventory management, and notifications.

Workflow:
1. Receive order via webhook
2. Validate order data
3. Check inventory availability
4. Process payment via Stripe
5. Update inventory
6. Send confirmation email
7. Log to analytics
8. Handle errors with retries

This showcases:
- Conditional branching (inventory check)
- Error handling and retries
- Multiple integrations (Stripe, Email, Analytics)
- State management across steps
"""

from helix_spirals import (
    WorkflowEngine,
    WorkflowNode,
    IntegrationNode,
    ConditionalNode,
    RetryPolicy,
)


def create_order_processing_workflow():
    """Create a production-ready order processing workflow."""
    
    engine = WorkflowEngine()
    
    # ============================================================
    # 1. TRIGGER: Receive order via webhook
    # ============================================================
    trigger = WorkflowNode(
        name="receive_order",
        node_type="trigger",
        trigger_type="webhook",
        config={
            "path": "/orders",
            "method": "POST",
            "description": "Webhook endpoint for incoming orders"
        }
    )
    
    # ============================================================
    # 2. VALIDATION: Validate order data
    # ============================================================
    validate_order = WorkflowNode(
        name="validate_order",
        node_type="action",
        action="validate_order_data",
        config={
            "schema": {
                "customer_id": "string",
                "customer_email": "string",
                "items": "array",
                "total_amount": "number"
            },
            "required_fields": ["customer_id", "items", "total_amount"]
        }
    )
    
    # ============================================================
    # 3. INVENTORY CHECK: Check product availability
    # ============================================================
    check_inventory = IntegrationNode(
        name="check_inventory",
        integration_type="shopify",
        action="check_inventory",
        config={
            "product_ids": "${items[*].product_id}",
            "quantities": "${items[*].quantity}"
        }
    )
    
    # ============================================================
    # 4. CONDITIONAL: Branch based on inventory
    # ============================================================
    inventory_check = ConditionalNode(
        name="inventory_available",
        condition=lambda ctx: ctx.get("inventory_status") == "in_stock"
    )
    
    # ============================================================
    # 5. PAYMENT: Process payment with Stripe
    # ============================================================
    # Define retry policy for payment processing
    payment_retry_policy = RetryPolicy(
        max_attempts=3,
        backoff_strategy="exponential",
        backoff_base=2,
        jitter=True,
        timeout=30
    )
    
    process_payment = IntegrationNode(
        name="process_payment",
        integration_type="stripe",
        action="create_charge",
        config={
            "customer_id": "${customer_id}",
            "amount": "${total_amount}",
            "currency": "usd",
            "description": "Order #${order_id}"
        },
        retry_policy=payment_retry_policy
    )
    
    # ============================================================
    # 6. INVENTORY UPDATE: Update inventory after payment
    # ============================================================
    update_inventory = IntegrationNode(
        name="update_inventory",
        integration_type="shopify",
        action="update_inventory",
        config={
            "product_ids": "${items[*].product_id}",
            "quantities": "${items[*].quantity}",
            "operation": "decrement"
        }
    )
    
    # ============================================================
    # 7. CONFIRMATION: Send confirmation email
    # ============================================================
    send_confirmation = IntegrationNode(
        name="send_confirmation",
        integration_type="email",
        action="send_email",
        config={
            "to": "${customer_email}",
            "subject": "Order Confirmation - Order #${order_id}",
            "template": "order_confirmation",
            "data": {
                "order_id": "${order_id}",
                "total_amount": "${total_amount}",
                "items": "${items}",
                "estimated_delivery": "${estimated_delivery}"
            }
        }
    )
    
    # ============================================================
    # 8. ANALYTICS: Log order to analytics service
    # ============================================================
    log_analytics = IntegrationNode(
        name="log_analytics",
        integration_type="mixpanel",
        action="track_event",
        config={
            "event": "order_completed",
            "properties": {
                "order_id": "${order_id}",
                "customer_id": "${customer_id}",
                "amount": "${total_amount}",
                "item_count": "${items.length}"
            }
        }
    )
    
    # ============================================================
    # ERROR PATHS: Handle failures
    # ============================================================
    
    # Insufficient inventory
    insufficient_inventory = IntegrationNode(
        name="notify_insufficient_inventory",
        integration_type="email",
        action="send_email",
        config={
            "to": "${customer_email}",
            "subject": "Order Cannot Be Fulfilled - Order #${order_id}",
            "body": "Unfortunately, some items in your order are out of stock. Please update your order."
        }
    )
    
    # Payment failed
    payment_failed = IntegrationNode(
        name="notify_payment_failed",
        integration_type="email",
        action="send_email",
        config={
            "to": "${customer_email}",
            "subject": "Payment Failed - Order #${order_id}",
            "body": "Your payment could not be processed. Please try again or contact support."
        }
    )
    
    # ============================================================
    # END NODES
    # ============================================================
    success_end = WorkflowNode(
        name="order_complete",
        node_type="end"
    )
    
    failure_end = WorkflowNode(
        name="order_failed",
        node_type="end"
    )
    
    # ============================================================
    # CONNECTIONS: Wire up the workflow
    # ============================================================
    
    # Main flow
    trigger.connect_to(validate_order)
    validate_order.connect_to(check_inventory)
    check_inventory.connect_to(inventory_check)
    
    # Inventory check branches
    inventory_check.connect_true(process_payment)
    inventory_check.connect_false(insufficient_inventory)
    
    # Payment success path
    process_payment.connect_to(update_inventory)
    update_inventory.connect_to(send_confirmation)
    send_confirmation.connect_to(log_analytics)
    log_analytics.connect_to(success_end)
    
    # Failure paths
    insufficient_inventory.connect_to(failure_end)
    process_payment.on_error(payment_failed)
    payment_failed.connect_to(failure_end)
    
    return engine, trigger


def print_workflow_structure():
    """Print the workflow structure for visualization."""
    
    structure = """
    Order Processing Workflow Structure
    ====================================
    
    receive_order (webhook)
           ↓
    validate_order (action)
           ↓
    check_inventory (Shopify)
           ↓
    inventory_available (conditional)
           ├─ TRUE → process_payment (Stripe, retry: 3x)
           │              ↓
           │         update_inventory (Shopify)
           │              ↓
           │         send_confirmation (Email)
           │              ↓
           │         log_analytics (Mixpanel)
           │              ↓
           │         order_complete ✅
           │
           └─ FALSE → notify_insufficient_inventory (Email)
                           ↓
                      order_failed ❌
    
    Error Paths:
    - Payment failure → notify_payment_failed → order_failed
    """
    
    print(structure)


def example_workflow_execution():
    """Example of how to execute the workflow."""
    
    engine, trigger = create_order_processing_workflow()
    
    # Example order data
    order_data = {
        "order_id": "ORD-2024-001",
        "customer_id": "cus_123456",
        "customer_email": "customer@example.com",
        "items": [
            {"product_id": "prod_1", "quantity": 2, "price": 29.99},
            {"product_id": "prod_2", "quantity": 1, "price": 49.99}
        ],
        "total_amount": 109.97,
        "estimated_delivery": "2024-04-10"
    }
    
    try:
        # Execute the workflow with order data
        result = engine.execute(
            trigger,
            trigger_data=order_data,
            metadata={"source": "api", "user_agent": "mobile"}
        )
        
        print("✅ Order processing workflow completed successfully")
        print(f"   Order ID: {order_data['order_id']}")
        print(f"   Status: {result.status}")
        print(f"   Execution Time: {result.execution_time}ms")
        
        return result
        
    except Exception as e:
        print(f"❌ Order processing failed: {e}")
        raise


if __name__ == "__main__":
    print("=" * 70)
    print("Helix Spirals - Order Processing Workflow Example")
    print("=" * 70)
    print()
    
    print("Workflow Structure:")
    print("-" * 70)
    print_workflow_structure()
    print()
    
    print("Creating and executing workflow...")
    print("-" * 70)
    example_workflow_execution()
    print()
    
    print("=" * 70)
    print("Example completed!")
    print("=" * 70)
