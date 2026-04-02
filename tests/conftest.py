"""
Pytest Configuration and Fixtures
==================================

This module provides shared fixtures and configuration for all tests.
"""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock
from typing import Generator

# Import from helix_spirals
try:
    from helix_spirals.engine import SpiralEngine
    from helix_spirals.models import (
        Spiral,
        ExecutionContext,
        ExecutionStatus,
        WorkflowNode,
        IntegrationNode,
    )
    from helix_spirals.storage import SpiralStorage
except ImportError:
    # Fallback for when modules aren't available
    pass


@pytest.fixture
def event_loop() -> Generator:
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_storage() -> MagicMock:
    """Create a mock storage instance."""
    storage = AsyncMock(spec=SpiralStorage)
    storage.save_workflow = AsyncMock(return_value=None)
    storage.get_workflow = AsyncMock(return_value=None)
    storage.save_execution = AsyncMock(return_value=None)
    storage.get_execution_history = AsyncMock(return_value=[])
    return storage


@pytest.fixture
def spiral_engine(mock_storage) -> SpiralEngine:
    """Create a SpiralEngine instance for testing."""
    return SpiralEngine(storage=mock_storage)


@pytest.fixture
def sample_execution_context() -> ExecutionContext:
    """Create a sample execution context."""
    return ExecutionContext(
        workflow_id="test_workflow_123",
        execution_id="exec_456",
        status=ExecutionStatus.RUNNING,
        variables={
            "user_id": "user_123",
            "order_id": "order_456",
            "amount": 99.99,
        },
        node_results={},
        errors=[],
    )


@pytest.fixture
def mock_redis():
    """Create a mock Redis client."""
    redis = AsyncMock()
    redis.pipeline = MagicMock(return_value=AsyncMock())
    redis.zremrangebyscore = AsyncMock(return_value=0)
    redis.zcard = AsyncMock(return_value=0)
    redis.zadd = AsyncMock(return_value=1)
    redis.pexpire = AsyncMock(return_value=True)
    redis.zrem = AsyncMock(return_value=1)
    return redis


@pytest.fixture
def mock_integration():
    """Create a mock integration connector."""
    integration = MagicMock()
    integration.name = "mock_service"
    integration.authenticate = MagicMock(return_value=None)
    integration.execute_action = AsyncMock(
        return_value={"success": True, "data": {}}
    )
    integration.get_available_actions = MagicMock(
        return_value=["action1", "action2"]
    )
    return integration


class MockWebSocketManager:
    """Mock WebSocket manager for testing."""

    def __init__(self):
        self.messages = []

    async def broadcast(self, message: dict):
        """Mock broadcast method."""
        self.messages.append(message)

    async def send_to_user(self, user_id: str, message: dict):
        """Mock send_to_user method."""
        self.messages.append({"user_id": user_id, **message})


@pytest.fixture
def mock_ws_manager() -> MockWebSocketManager:
    """Create a mock WebSocket manager."""
    return MockWebSocketManager()


# Markers for test categorization
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "async: mark test as an async test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "requires_redis: mark test as requiring Redis"
    )


# Pytest hooks for better output
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add async marker to async tests
        if asyncio.iscoroutinefunction(item.function):
            item.add_marker(pytest.mark.async)

        # Add integration marker to integration tests
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        else:
            item.add_marker(pytest.mark.unit)
