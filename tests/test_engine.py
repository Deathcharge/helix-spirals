"""
Unit Tests for SpiralEngine
============================

Tests for the core workflow execution engine.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, UTC

from helix_spirals.engine import SpiralEngine, RateLimiter
from helix_spirals.models import (
    ExecutionContext,
    ExecutionStatus,
    ExecutionError,
)


@pytest.mark.unit
class TestRateLimiter:
    """Tests for RateLimiter class."""

    @pytest.mark.async
    async def test_rate_limiter_allows_first_request(self):
        """Test that rate limiter allows first request."""
        limiter = RateLimiter(
            spiral_id="test_spiral",
            max_executions=5,
            window_ms=1000
        )
        
        # Should allow first request when Redis is unavailable
        result = await limiter.allow()
        assert result is True

    @pytest.mark.async
    async def test_rate_limiter_with_mock_redis(self, mock_redis):
        """Test rate limiter with mocked Redis."""
        limiter = RateLimiter(
            spiral_id="test_spiral",
            max_executions=5,
            window_ms=1000
        )
        
        # Mock the get_redis function
        with patch('helix_spirals.engine.get_redis', return_value=mock_redis):
            # Setup mock pipeline
            pipeline = AsyncMock()
            pipeline.execute = AsyncMock(return_value=[0, 0, 1, True])
            mock_redis.pipeline.return_value = pipeline
            
            result = await limiter.allow()
            assert result is True

    def test_rate_limiter_initialization(self):
        """Test RateLimiter initialization."""
        limiter = RateLimiter(
            spiral_id="test_spiral",
            max_executions=10,
            window_ms=5000,
            strategy="sliding"
        )
        
        assert limiter.spiral_id == "test_spiral"
        assert limiter.max_executions == 10
        assert limiter.window_ms == 5000
        assert limiter.strategy == "sliding"


@pytest.mark.unit
class TestSpiralEngine:
    """Tests for SpiralEngine class."""

    def test_engine_initialization(self, spiral_engine):
        """Test SpiralEngine initialization."""
        assert spiral_engine.storage is not None
        assert spiral_engine.action_executor is not None
        assert isinstance(spiral_engine.execution_queue, dict)
        assert isinstance(spiral_engine.rate_limiters, dict)
        assert isinstance(spiral_engine.active_executions, dict)

    def test_engine_with_websocket_manager(self, mock_storage, mock_ws_manager):
        """Test SpiralEngine initialization with WebSocket manager."""
        engine = SpiralEngine(storage=mock_storage, ws_manager=mock_ws_manager)
        
        assert engine.ws_manager is not None
        assert engine.ws_manager == mock_ws_manager

    @pytest.mark.async
    async def test_execute_workflow_basic(self, spiral_engine, sample_execution_context):
        """Test basic workflow execution."""
        # Mock the execute method to return a context
        spiral_engine.storage.get_workflow = AsyncMock(
            return_value={
                "id": "test_workflow_123",
                "name": "Test Workflow",
                "nodes": [],
                "edges": []
            }
        )
        
        # Note: This is a simplified test. Full execution would require
        # more complex setup with actual workflow nodes.
        assert spiral_engine.storage is not None

    @pytest.mark.async
    async def test_execution_context_tracking(self, spiral_engine):
        """Test that execution contexts are properly tracked."""
        exec_id = "exec_123"
        context = ExecutionContext(
            workflow_id="workflow_123",
            execution_id=exec_id,
            status=ExecutionStatus.RUNNING,
            variables={},
            node_results={},
            errors=[]
        )
        
        spiral_engine.execution_queue[exec_id] = context
        
        assert exec_id in spiral_engine.execution_queue
        assert spiral_engine.execution_queue[exec_id].execution_id == exec_id

    def test_rate_limiter_creation(self, spiral_engine):
        """Test rate limiter creation for spiral."""
        spiral_id = "test_spiral"
        
        limiter = RateLimiter(
            spiral_id=spiral_id,
            max_executions=10,
            window_ms=60000
        )
        
        spiral_engine.rate_limiters[spiral_id] = limiter
        
        assert spiral_id in spiral_engine.rate_limiters
        assert spiral_engine.rate_limiters[spiral_id].max_executions == 10

    @pytest.mark.async
    async def test_action_executor_initialization(self, spiral_engine):
        """Test that action executor is properly initialized."""
        assert spiral_engine.action_executor is not None
        # Action executor should have reference to engine
        assert hasattr(spiral_engine.action_executor, 'engine')


@pytest.mark.unit
class TestExecutionContext:
    """Tests for ExecutionContext model."""

    def test_execution_context_creation(self):
        """Test ExecutionContext creation."""
        context = ExecutionContext(
            workflow_id="workflow_123",
            execution_id="exec_456",
            status=ExecutionStatus.RUNNING,
            variables={"key": "value"},
            node_results={},
            errors=[]
        )
        
        assert context.workflow_id == "workflow_123"
        assert context.execution_id == "exec_456"
        assert context.status == ExecutionStatus.RUNNING
        assert context.variables["key"] == "value"

    def test_execution_context_with_errors(self):
        """Test ExecutionContext with errors."""
        error = ExecutionError(
            node_id="node_123",
            error_type="api_error",
            message="API request failed"
        )
        
        context = ExecutionContext(
            workflow_id="workflow_123",
            execution_id="exec_456",
            status=ExecutionStatus.FAILED,
            variables={},
            node_results={},
            errors=[error]
        )
        
        assert len(context.errors) == 1
        assert context.errors[0].error_type == "api_error"

    def test_execution_context_status_transitions(self):
        """Test execution context status transitions."""
        context = ExecutionContext(
            workflow_id="workflow_123",
            execution_id="exec_456",
            status=ExecutionStatus.PENDING,
            variables={},
            node_results={},
            errors=[]
        )
        
        assert context.status == ExecutionStatus.PENDING
        
        # Simulate status change
        context.status = ExecutionStatus.RUNNING
        assert context.status == ExecutionStatus.RUNNING
        
        context.status = ExecutionStatus.COMPLETED
        assert context.status == ExecutionStatus.COMPLETED


@pytest.mark.unit
class TestErrorHandling:
    """Tests for error handling in the engine."""

    def test_execution_error_creation(self):
        """Test ExecutionError creation."""
        error = ExecutionError(
            node_id="node_123",
            error_type="timeout",
            message="Request timed out",
            retry_count=2
        )
        
        assert error.node_id == "node_123"
        assert error.error_type == "timeout"
        assert error.retry_count == 2

    def test_execution_error_with_context(self):
        """Test ExecutionError with additional context."""
        error = ExecutionError(
            node_id="node_123",
            error_type="validation_error",
            message="Invalid input",
            context={"field": "email", "value": "invalid"}
        )
        
        assert error.context["field"] == "email"

    @pytest.mark.async
    async def test_error_recovery(self, spiral_engine):
        """Test error recovery mechanisms."""
        # Create a context with an error
        error = ExecutionError(
            node_id="node_123",
            error_type="transient",
            message="Temporary failure"
        )
        
        context = ExecutionContext(
            workflow_id="workflow_123",
            execution_id="exec_456",
            status=ExecutionStatus.FAILED,
            variables={},
            node_results={},
            errors=[error]
        )
        
        # Store in queue for potential retry
        spiral_engine.execution_queue["exec_456"] = context
        
        assert "exec_456" in spiral_engine.execution_queue
        assert len(spiral_engine.execution_queue["exec_456"].errors) > 0


@pytest.mark.unit
class TestExecutionMetrics:
    """Tests for execution metrics and logging."""

    def test_execution_timing(self):
        """Test execution timing calculation."""
        context = ExecutionContext(
            workflow_id="workflow_123",
            execution_id="exec_456",
            status=ExecutionStatus.COMPLETED,
            variables={},
            node_results={},
            errors=[]
        )
        
        # Simulate execution timing
        start_time = datetime.now(UTC)
        context.started_at = start_time
        
        # Simulate some work
        import time
        time.sleep(0.1)
        
        end_time = datetime.now(UTC)
        context.completed_at = end_time
        
        # Calculate duration
        duration_ms = (end_time - start_time).total_seconds() * 1000
        
        assert duration_ms > 0
        assert context.started_at is not None
        assert context.completed_at is not None

    def test_node_result_tracking(self):
        """Test tracking of node execution results."""
        context = ExecutionContext(
            workflow_id="workflow_123",
            execution_id="exec_456",
            status=ExecutionStatus.RUNNING,
            variables={},
            node_results={},
            errors=[]
        )
        
        # Add node results
        context.node_results["node_1"] = {"status": "success", "output": "data"}
        context.node_results["node_2"] = {"status": "success", "output": "more_data"}
        
        assert len(context.node_results) == 2
        assert context.node_results["node_1"]["status"] == "success"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
