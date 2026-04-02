"""
Test Utilities and Helpers
===========================

Utility functions and helpers for testing Helix Spirals.
"""

import pytest
from typing import Dict, Any, List
from unittest.mock import MagicMock, AsyncMock


class WorkflowTestBuilder:
    """Builder class for constructing test workflows."""

    def __init__(self):
        self.nodes = []
        self.edges = []
        self.config = {}

    def add_trigger(self, trigger_type: str, config: Dict[str, Any] = None):
        """Add a trigger node."""
        node = {
            "id": f"trigger_{len(self.nodes)}",
            "type": "trigger",
            "trigger_type": trigger_type,
            "config": config or {}
        }
        self.nodes.append(node)
        return self

    def add_action(self, action: str, config: Dict[str, Any] = None):
        """Add an action node."""
        node = {
            "id": f"action_{len(self.nodes)}",
            "type": "action",
            "action": action,
            "config": config or {}
        }
        self.nodes.append(node)
        return self

    def add_integration(
        self,
        integration_type: str,
        action: str,
        config: Dict[str, Any] = None
    ):
        """Add an integration node."""
        node = {
            "id": f"integration_{len(self.nodes)}",
            "type": "integration",
            "integration_type": integration_type,
            "action": action,
            "config": config or {}
        }
        self.nodes.append(node)
        return self

    def add_conditional(self, condition: str):
        """Add a conditional node."""
        node = {
            "id": f"conditional_{len(self.nodes)}",
            "type": "conditional",
            "condition": condition
        }
        self.nodes.append(node)
        return self

    def connect(self, from_index: int, to_index: int):
        """Connect two nodes."""
        if from_index < len(self.nodes) and to_index < len(self.nodes):
            self.edges.append({
                "from": self.nodes[from_index]["id"],
                "to": self.nodes[to_index]["id"]
            })
        return self

    def build(self) -> Dict[str, Any]:
        """Build the workflow."""
        return {
            "nodes": self.nodes,
            "edges": self.edges,
            "config": self.config
        }


class ExecutionContextBuilder:
    """Builder class for constructing test execution contexts."""

    def __init__(self, workflow_id: str = "test_workflow"):
        self.workflow_id = workflow_id
        self.execution_id = "test_execution"
        self.status = "running"
        self.variables = {}
        self.node_results = {}
        self.errors = []

    def with_variable(self, key: str, value: Any):
        """Add a variable to the context."""
        self.variables[key] = value
        return self

    def with_variables(self, variables: Dict[str, Any]):
        """Add multiple variables."""
        self.variables.update(variables)
        return self

    def with_node_result(self, node_id: str, result: Dict[str, Any]):
        """Add a node result."""
        self.node_results[node_id] = result
        return self

    def with_error(self, node_id: str, error_type: str, message: str):
        """Add an error."""
        self.errors.append({
            "node_id": node_id,
            "error_type": error_type,
            "message": message
        })
        return self

    def with_status(self, status: str):
        """Set the execution status."""
        self.status = status
        return self

    def build(self) -> Dict[str, Any]:
        """Build the execution context."""
        return {
            "workflow_id": self.workflow_id,
            "execution_id": self.execution_id,
            "status": self.status,
            "variables": self.variables,
            "node_results": self.node_results,
            "errors": self.errors
        }


class MockIntegrationBuilder:
    """Builder class for constructing mock integrations."""

    def __init__(self, name: str):
        self.name = name
        self.mock = MagicMock()
        self.mock.name = name
        self.actions = {}

    def add_action(
        self,
        action_name: str,
        response: Dict[str, Any],
        is_async: bool = True
    ):
        """Add a mock action."""
        if is_async:
            self.mock.execute_action = AsyncMock(return_value=response)
        else:
            self.mock.execute_action = MagicMock(return_value=response)
        self.actions[action_name] = response
        return self

    def add_action_error(
        self,
        action_name: str,
        error: Exception,
        is_async: bool = True
    ):
        """Add a mock action that raises an error."""
        if is_async:
            self.mock.execute_action = AsyncMock(side_effect=error)
        else:
            self.mock.execute_action = MagicMock(side_effect=error)
        return self

    def build(self):
        """Build the mock integration."""
        return self.mock


class TestDataGenerator:
    """Generate test data for various scenarios."""

    @staticmethod
    def sample_order() -> Dict[str, Any]:
        """Generate sample order data."""
        return {
            "order_id": "ORD-2024-001",
            "customer_id": "cus_123456",
            "customer_email": "customer@example.com",
            "items": [
                {"product_id": "prod_1", "quantity": 2, "price": 29.99},
                {"product_id": "prod_2", "quantity": 1, "price": 49.99}
            ],
            "total_amount": 109.97,
            "status": "pending"
        }

    @staticmethod
    def sample_customer() -> Dict[str, Any]:
        """Generate sample customer data."""
        return {
            "customer_id": "cus_123456",
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "address": {
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip": "10001"
            }
        }

    @staticmethod
    def sample_payment() -> Dict[str, Any]:
        """Generate sample payment data."""
        return {
            "payment_id": "pay_123456",
            "amount": 99.99,
            "currency": "usd",
            "status": "succeeded",
            "method": "card",
            "card": {
                "brand": "visa",
                "last4": "4242"
            }
        }

    @staticmethod
    def sample_webhook_payload() -> Dict[str, Any]:
        """Generate sample webhook payload."""
        return {
            "event": "order.created",
            "timestamp": "2024-04-02T10:00:00Z",
            "data": TestDataGenerator.sample_order()
        }

    @staticmethod
    def sample_social_post() -> Dict[str, Any]:
        """Generate sample social media post."""
        return {
            "id": "post_123",
            "title": "New Feature Release",
            "content": "We're excited to announce a new feature...",
            "media_urls": ["https://example.com/image.jpg"],
            "hashtags": "#announcement #feature",
            "platforms": ["twitter", "linkedin", "instagram"]
        }


class AssertionHelpers:
    """Helper methods for common assertions."""

    @staticmethod
    def assert_workflow_valid(workflow: Dict[str, Any]):
        """Assert that a workflow is valid."""
        assert "nodes" in workflow
        assert "edges" in workflow
        assert isinstance(workflow["nodes"], list)
        assert isinstance(workflow["edges"], list)
        assert len(workflow["nodes"]) > 0

    @staticmethod
    def assert_execution_successful(context: Dict[str, Any]):
        """Assert that an execution was successful."""
        assert context["status"] in ["completed", "success"]
        assert len(context.get("errors", [])) == 0

    @staticmethod
    def assert_execution_failed(context: Dict[str, Any]):
        """Assert that an execution failed."""
        assert context["status"] in ["failed", "error"]
        assert len(context.get("errors", [])) > 0

    @staticmethod
    def assert_node_executed(context: Dict[str, Any], node_id: str):
        """Assert that a node was executed."""
        assert node_id in context.get("node_results", {})

    @staticmethod
    def assert_variable_set(context: Dict[str, Any], var_name: str, value: Any = None):
        """Assert that a variable was set."""
        assert var_name in context.get("variables", {})
        if value is not None:
            assert context["variables"][var_name] == value


# Pytest fixtures using the builders

@pytest.fixture
def workflow_builder() -> WorkflowTestBuilder:
    """Provide a workflow builder."""
    return WorkflowTestBuilder()


@pytest.fixture
def context_builder() -> ExecutionContextBuilder:
    """Provide an execution context builder."""
    return ExecutionContextBuilder()


@pytest.fixture
def integration_builder():
    """Provide an integration builder factory."""
    def _builder(name: str):
        return MockIntegrationBuilder(name)
    return _builder


@pytest.fixture
def test_data() -> TestDataGenerator:
    """Provide test data generator."""
    return TestDataGenerator()


@pytest.fixture
def assertions() -> AssertionHelpers:
    """Provide assertion helpers."""
    return AssertionHelpers()


if __name__ == "__main__":
    # Example usage
    builder = WorkflowTestBuilder()
    workflow = (
        builder
        .add_trigger("webhook", {"path": "/orders"})
        .add_action("validate_data")
        .add_integration("stripe", "create_charge")
        .connect(0, 1)
        .connect(1, 2)
        .build()
    )
    
    print("Generated workflow:")
    print(workflow)
