"""
Workflow Execution Tests
========================

Tests for workflow execution, node processing, and DAG traversal.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, UTC

from tests.test_utils import (
    WorkflowTestBuilder,
    ExecutionContextBuilder,
    TestDataGenerator,
    AssertionHelpers
)


@pytest.mark.unit
class TestWorkflowBuilder:
    """Tests for WorkflowTestBuilder."""

    def test_build_simple_workflow(self, workflow_builder):
        """Test building a simple workflow."""
        workflow = (
            workflow_builder
            .add_trigger("webhook", {"path": "/orders"})
            .add_action("validate_data")
            .connect(0, 1)
            .build()
        )
        
        assert len(workflow["nodes"]) == 2
        assert len(workflow["edges"]) == 1
        assert workflow["nodes"][0]["type"] == "trigger"
        assert workflow["nodes"][1]["type"] == "action"

    def test_build_complex_workflow(self, workflow_builder):
        """Test building a complex workflow."""
        workflow = (
            workflow_builder
            .add_trigger("webhook")
            .add_action("validate")
            .add_integration("stripe", "create_charge")
            .add_action("send_notification")
            .connect(0, 1)
            .connect(1, 2)
            .connect(2, 3)
            .build()
        )
        
        assert len(workflow["nodes"]) == 4
        assert len(workflow["edges"]) == 3

    def test_workflow_with_conditionals(self, workflow_builder):
        """Test workflow with conditional nodes."""
        workflow = (
            workflow_builder
            .add_trigger("webhook")
            .add_conditional("amount > 100")
            .add_action("high_value_process")
            .add_action("standard_process")
            .connect(0, 1)
            .connect(1, 2)
            .connect(1, 3)
            .build()
        )
        
        assert len(workflow["nodes"]) == 4
        assert workflow["nodes"][1]["type"] == "conditional"


@pytest.mark.unit
class TestExecutionContextBuilder:
    """Tests for ExecutionContextBuilder."""

    def test_build_execution_context(self, context_builder):
        """Test building execution context."""
        context = (
            context_builder
            .with_variable("order_id", "ORD-123")
            .with_variable("customer_id", "cus_456")
            .with_status("completed")
            .build()
        )
        
        assert context["variables"]["order_id"] == "ORD-123"
        assert context["variables"]["customer_id"] == "cus_456"
        assert context["status"] == "completed"

    def test_context_with_node_results(self, context_builder):
        """Test context with node results."""
        context = (
            context_builder
            .with_node_result("validate", {"valid": True})
            .with_node_result("charge", {"charge_id": "ch_123"})
            .build()
        )
        
        assert len(context["node_results"]) == 2
        assert context["node_results"]["validate"]["valid"] is True

    def test_context_with_errors(self, context_builder):
        """Test context with errors."""
        context = (
            context_builder
            .with_error("charge", "payment_error", "Card declined")
            .with_status("failed")
            .build()
        )
        
        assert len(context["errors"]) == 1
        assert context["errors"][0]["error_type"] == "payment_error"


@pytest.mark.unit
class TestDataGenerator:
    """Tests for TestDataGenerator."""

    def test_sample_order(self):
        """Test generating sample order."""
        order = TestDataGenerator.sample_order()
        
        assert "order_id" in order
        assert "customer_id" in order
        assert "items" in order
        assert "total_amount" in order
        assert len(order["items"]) > 0

    def test_sample_customer(self):
        """Test generating sample customer."""
        customer = TestDataGenerator.sample_customer()
        
        assert "customer_id" in customer
        assert "name" in customer
        assert "email" in customer
        assert "address" in customer

    def test_sample_payment(self):
        """Test generating sample payment."""
        payment = TestDataGenerator.sample_payment()
        
        assert "payment_id" in payment
        assert "amount" in payment
        assert "currency" in payment
        assert "status" in payment

    def test_sample_webhook_payload(self):
        """Test generating sample webhook."""
        payload = TestDataGenerator.sample_webhook_payload()
        
        assert "event" in payload
        assert "timestamp" in payload
        assert "data" in payload

    def test_sample_social_post(self):
        """Test generating sample social post."""
        post = TestDataGenerator.sample_social_post()
        
        assert "id" in post
        assert "title" in post
        assert "content" in post
        assert "platforms" in post


@pytest.mark.unit
class TestAssertionHelpers:
    """Tests for AssertionHelpers."""

    def test_assert_workflow_valid(self):
        """Test workflow validation assertion."""
        valid_workflow = {
            "nodes": [{"id": "1"}],
            "edges": []
        }
        
        # Should not raise
        AssertionHelpers.assert_workflow_valid(valid_workflow)

    def test_assert_workflow_invalid(self):
        """Test workflow validation fails."""
        invalid_workflow = {
            "edges": []
        }
        
        with pytest.raises(AssertionError):
            AssertionHelpers.assert_workflow_valid(invalid_workflow)

    def test_assert_execution_successful(self):
        """Test successful execution assertion."""
        context = {
            "status": "completed",
            "errors": []
        }
        
        # Should not raise
        AssertionHelpers.assert_execution_successful(context)

    def test_assert_execution_failed(self):
        """Test failed execution assertion."""
        context = {
            "status": "failed",
            "errors": [{"message": "Error"}]
        }
        
        # Should not raise
        AssertionHelpers.assert_execution_failed(context)

    def test_assert_node_executed(self):
        """Test node execution assertion."""
        context = {
            "node_results": {
                "node_1": {"output": "data"}
            }
        }
        
        # Should not raise
        AssertionHelpers.assert_node_executed(context, "node_1")

    def test_assert_variable_set(self):
        """Test variable set assertion."""
        context = {
            "variables": {
                "order_id": "ORD-123"
            }
        }
        
        # Should not raise
        AssertionHelpers.assert_variable_set(context, "order_id", "ORD-123")


@pytest.mark.unit
class TestWorkflowPatterns:
    """Tests for common workflow patterns."""

    def test_sequential_workflow(self, workflow_builder):
        """Test sequential workflow pattern."""
        workflow = (
            workflow_builder
            .add_trigger("webhook")
            .add_action("step_1")
            .add_action("step_2")
            .add_action("step_3")
            .connect(0, 1)
            .connect(1, 2)
            .connect(2, 3)
            .build()
        )
        
        assert len(workflow["nodes"]) == 4
        assert len(workflow["edges"]) == 3

    def test_parallel_workflow(self, workflow_builder):
        """Test parallel workflow pattern."""
        workflow = (
            workflow_builder
            .add_trigger("webhook")
            .add_action("notify_slack")
            .add_action("notify_email")
            .add_action("track_analytics")
            .connect(0, 1)
            .connect(0, 2)
            .connect(0, 3)
            .build()
        )
        
        # All three actions connected to trigger
        assert len(workflow["edges"]) == 3

    def test_branching_workflow(self, workflow_builder):
        """Test branching workflow pattern."""
        workflow = (
            workflow_builder
            .add_trigger("webhook")
            .add_conditional("amount > 100")
            .add_integration("stripe", "create_charge")
            .add_action("send_confirmation")
            .connect(0, 1)
            .connect(1, 2)
            .connect(2, 3)
            .build()
        )
        
        assert workflow["nodes"][1]["type"] == "conditional"


@pytest.mark.unit
class TestIntegrationScenarios:
    """Tests for real-world integration scenarios."""

    def test_order_processing_workflow(self, workflow_builder, test_data):
        """Test order processing workflow."""
        workflow = (
            workflow_builder
            .add_trigger("webhook", {"path": "/orders"})
            .add_action("validate_order")
            .add_integration("stripe", "create_charge")
            .add_integration("email", "send_email")
            .add_action("update_inventory")
            .connect(0, 1)
            .connect(1, 2)
            .connect(2, 3)
            .connect(3, 4)
            .build()
        )
        
        # Verify structure
        assert len(workflow["nodes"]) == 5
        assert workflow["nodes"][0]["trigger_type"] == "webhook"
        assert workflow["nodes"][2]["integration_type"] == "stripe"

    def test_social_media_workflow(self, workflow_builder):
        """Test social media automation workflow."""
        workflow = (
            workflow_builder
            .add_trigger("schedule", {"expression": "0 9 * * *"})
            .add_integration("notion", "query_database")
            .add_action("generate_captions")
            .add_integration("slack", "send_message")
            .add_integration("email", "send_email")
            .connect(0, 1)
            .connect(1, 2)
            .connect(2, 3)
            .connect(2, 4)
            .build()
        )
        
        assert workflow["nodes"][0]["trigger_type"] == "schedule"
        # Parallel execution to Slack and Email
        assert len(workflow["edges"]) == 5

    def test_approval_workflow(self, workflow_builder):
        """Test approval workflow."""
        workflow = (
            workflow_builder
            .add_trigger("webhook")
            .add_conditional("amount > 1000")
            .add_action("request_approval")
            .add_action("auto_approve")
            .add_integration("stripe", "create_charge")
            .connect(0, 1)
            .connect(1, 2)
            .connect(1, 3)
            .connect(2, 4)
            .connect(3, 4)
            .build()
        )
        
        # Conditional branching with convergence
        assert len(workflow["edges"]) == 5


@pytest.mark.unit
class TestErrorScenarios:
    """Tests for error handling scenarios."""

    def test_error_path_workflow(self, workflow_builder):
        """Test workflow with error paths."""
        workflow = (
            workflow_builder
            .add_trigger("webhook")
            .add_integration("stripe", "create_charge")
            .add_action("success_handler")
            .add_action("error_handler")
            .connect(0, 1)
            .connect(1, 2)
            .build()
        )
        
        # In real implementation, node 1 would have error path to node 3
        assert len(workflow["nodes"]) == 4

    def test_retry_workflow(self, workflow_builder):
        """Test workflow with retry logic."""
        workflow = (
            workflow_builder
            .add_trigger("webhook")
            .add_integration("stripe", "create_charge")
            .add_action("notify_success")
            .connect(0, 1)
            .connect(1, 2)
            .build()
        )
        
        # Stripe node would have retry policy configured
        stripe_node = workflow["nodes"][1]
        assert stripe_node["integration_type"] == "stripe"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
