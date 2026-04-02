"""
Tests for Error Handling and Logging
=====================================

Tests for exception hierarchy, retry policies, recovery strategies,
and structured logging.
"""

import pytest
import asyncio
from datetime import datetime, UTC
from unittest.mock import AsyncMock, MagicMock, patch

from helix_spirals.error_handling import (
    SpiralException,
    WorkflowExecutionError,
    IntegrationError,
    ValidationError,
    RateLimitError,
    TimeoutError,
    AuthenticationError,
    RetryPolicy,
    BackoffStrategy,
    retry,
    retry_sync,
    RetryRecoveryStrategy,
    FallbackRecoveryStrategy,
    CircuitBreakerRecoveryStrategy,
    StructuredLogger,
    ErrorTracker,
    error_tracker,
)


@pytest.mark.unit
class TestExceptionHierarchy:
    """Tests for custom exception hierarchy."""

    def test_spiral_exception_creation(self):
        """Test SpiralException creation."""
        exc = SpiralException(
            message="Test error",
            error_code="TEST_ERROR",
            context={"key": "value"},
            recoverable=True
        )
        
        assert exc.message == "Test error"
        assert exc.error_code == "TEST_ERROR"
        assert exc.context["key"] == "value"
        assert exc.recoverable is True

    def test_spiral_exception_to_dict(self):
        """Test SpiralException conversion to dict."""
        exc = SpiralException(
            message="Test error",
            error_code="TEST_ERROR",
            context={"key": "value"}
        )
        
        exc_dict = exc.to_dict()
        assert exc_dict["error_code"] == "TEST_ERROR"
        assert exc_dict["message"] == "Test error"
        assert exc_dict["context"]["key"] == "value"

    def test_workflow_execution_error(self):
        """Test WorkflowExecutionError."""
        exc = WorkflowExecutionError(
            message="Workflow failed",
            workflow_id="wf_123",
            node_id="node_456"
        )
        
        assert exc.error_code == "WORKFLOW_EXECUTION_ERROR"
        assert exc.context["workflow_id"] == "wf_123"
        assert exc.context["node_id"] == "node_456"

    def test_integration_error(self):
        """Test IntegrationError."""
        exc = IntegrationError(
            message="API call failed",
            integration_type="stripe",
            action="create_charge",
            status_code=429
        )
        
        assert exc.error_code == "INTEGRATION_ERROR"
        assert exc.context["integration_type"] == "stripe"
        assert exc.context["status_code"] == 429

    def test_validation_error(self):
        """Test ValidationError."""
        exc = ValidationError(
            message="Invalid email",
            field="email",
            value="invalid"
        )
        
        assert exc.error_code == "VALIDATION_ERROR"
        assert exc.context["field"] == "email"

    def test_rate_limit_error(self):
        """Test RateLimitError."""
        exc = RateLimitError(
            message="Rate limited",
            service="slack",
            retry_after=60
        )
        
        assert exc.error_code == "RATE_LIMIT_ERROR"
        assert exc.recoverable is True
        assert exc.context["retry_after"] == 60

    def test_timeout_error(self):
        """Test TimeoutError."""
        exc = TimeoutError(
            message="Request timed out",
            operation="api_call",
            timeout_seconds=30
        )
        
        assert exc.error_code == "TIMEOUT_ERROR"
        assert exc.recoverable is True

    def test_authentication_error(self):
        """Test AuthenticationError."""
        exc = AuthenticationError(
            message="Invalid credentials",
            service="stripe"
        )
        
        assert exc.error_code == "AUTHENTICATION_ERROR"
        assert exc.recoverable is False


@pytest.mark.unit
class TestRetryPolicy:
    """Tests for RetryPolicy."""

    def test_retry_policy_creation(self):
        """Test RetryPolicy creation."""
        policy = RetryPolicy(
            max_attempts=3,
            backoff_strategy=BackoffStrategy.EXPONENTIAL,
            initial_delay=1.0
        )
        
        assert policy.max_attempts == 3
        assert policy.backoff_strategy == BackoffStrategy.EXPONENTIAL

    def test_linear_backoff(self):
        """Test linear backoff calculation."""
        policy = RetryPolicy(
            backoff_strategy=BackoffStrategy.LINEAR,
            initial_delay=1.0,
            jitter=False
        )
        
        assert policy.get_delay(0) == 1.0
        assert policy.get_delay(1) == 2.0
        assert policy.get_delay(2) == 3.0

    def test_exponential_backoff(self):
        """Test exponential backoff calculation."""
        policy = RetryPolicy(
            backoff_strategy=BackoffStrategy.EXPONENTIAL,
            initial_delay=1.0,
            backoff_base=2.0,
            jitter=False
        )
        
        assert policy.get_delay(0) == 1.0
        assert policy.get_delay(1) == 2.0
        assert policy.get_delay(2) == 4.0

    def test_fibonacci_backoff(self):
        """Test Fibonacci backoff calculation."""
        policy = RetryPolicy(
            backoff_strategy=BackoffStrategy.FIBONACCI,
            initial_delay=1.0,
            jitter=False
        )
        
        # Fibonacci: 1, 1, 2, 3, 5, 8, ...
        assert policy.get_delay(0) == 1.0
        assert policy.get_delay(1) == 1.0
        assert policy.get_delay(2) == 2.0

    def test_backoff_max_delay(self):
        """Test that backoff respects max_delay."""
        policy = RetryPolicy(
            backoff_strategy=BackoffStrategy.EXPONENTIAL,
            initial_delay=1.0,
            backoff_base=10.0,
            max_delay=100.0,
            jitter=False
        )
        
        # Without max_delay, this would be 10^5 = 100000
        delay = policy.get_delay(5)
        assert delay <= policy.max_delay


@pytest.mark.unit
@pytest.mark.async
class TestRetryDecorator:
    """Tests for retry decorator."""

    @pytest.mark.asyncio
    async def test_retry_success_first_attempt(self):
        """Test retry succeeds on first attempt."""
        call_count = 0
        
        @retry(policy=RetryPolicy(max_attempts=3))
        async def successful_function():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = await successful_function()
        assert result == "success"
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_retry_succeeds_after_failures(self):
        """Test retry succeeds after transient failures."""
        call_count = 0
        
        @retry(policy=RetryPolicy(max_attempts=3, initial_delay=0.01))
        async def eventually_succeeds():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise TimeoutError("Temporary failure")
            return "success"
        
        result = await eventually_succeeds()
        assert result == "success"
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_retry_exhausts_attempts(self):
        """Test retry exhausts all attempts."""
        call_count = 0
        
        @retry(policy=RetryPolicy(max_attempts=3, initial_delay=0.01))
        async def always_fails():
            nonlocal call_count
            call_count += 1
            raise TimeoutError("Persistent failure")
        
        with pytest.raises(TimeoutError):
            await always_fails()
        
        assert call_count == 3

    def test_retry_sync_decorator(self):
        """Test synchronous retry decorator."""
        call_count = 0
        
        @retry_sync(policy=RetryPolicy(max_attempts=3, initial_delay=0.01))
        def eventually_succeeds():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise TimeoutError("Temporary failure")
            return "success"
        
        result = eventually_succeeds()
        assert result == "success"
        assert call_count == 2


@pytest.mark.unit
class TestRecoveryStrategies:
    """Tests for error recovery strategies."""

    @pytest.mark.async
    async def test_retry_recovery_strategy(self):
        """Test RetryRecoveryStrategy."""
        strategy = RetryRecoveryStrategy()
        
        error = TimeoutError("Request timed out", "api_call")
        can_recover = await strategy.can_recover(error)
        
        assert can_recover is True

    @pytest.mark.async
    async def test_fallback_recovery_strategy(self):
        """Test FallbackRecoveryStrategy."""
        strategy = FallbackRecoveryStrategy(fallback_value="default")
        
        error = Exception("Some error")
        can_recover = await strategy.can_recover(error)
        assert can_recover is True
        
        result = await strategy.recover(error, {})
        assert result == "default"

    @pytest.mark.async
    async def test_circuit_breaker_strategy(self):
        """Test CircuitBreakerRecoveryStrategy."""
        strategy = CircuitBreakerRecoveryStrategy(
            failure_threshold=3,
            timeout=60
        )
        
        # First few failures should be recoverable
        error = Exception("Error")
        for i in range(3):
            can_recover = await strategy.can_recover(error)
            assert can_recover is True
        
        # After threshold, should raise
        with pytest.raises(SpiralException):
            await strategy.recover(error, {})
        
        # Circuit should be open
        can_recover = await strategy.can_recover(error)
        assert can_recover is False


@pytest.mark.unit
class TestStructuredLogger:
    """Tests for StructuredLogger."""

    def test_logger_creation(self):
        """Test StructuredLogger creation."""
        logger = StructuredLogger("test_logger")
        
        assert logger.logger is not None
        assert isinstance(logger.context_stack, list)

    def test_context_stack(self):
        """Test context stack operations."""
        logger = StructuredLogger("test_logger")
        
        logger.push_context(workflow_id="wf_123")
        context = logger.get_context()
        assert context["workflow_id"] == "wf_123"
        
        logger.push_context(execution_id="exec_456")
        context = logger.get_context()
        assert context["workflow_id"] == "wf_123"
        assert context["execution_id"] == "exec_456"
        
        logger.pop_context()
        context = logger.get_context()
        assert "execution_id" not in context
        assert context["workflow_id"] == "wf_123"

    def test_logger_methods(self, caplog):
        """Test logger methods."""
        logger = StructuredLogger("test_logger")
        
        # These should not raise
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")


@pytest.mark.unit
class TestErrorTracker:
    """Tests for ErrorTracker."""

    def test_error_tracker_creation(self):
        """Test ErrorTracker creation."""
        tracker = ErrorTracker()
        
        assert tracker.metrics is not None
        assert isinstance(tracker.error_history, list)

    def test_track_error(self):
        """Test tracking an error."""
        tracker = ErrorTracker()
        
        error = ValidationError(
            message="Invalid input",
            field="email"
        )
        
        tracker.track_error(error, workflow_id="wf_123")
        
        assert tracker.metrics.total_errors == 1
        assert len(tracker.error_history) == 1

    def test_get_metrics(self):
        """Test getting metrics."""
        tracker = ErrorTracker()
        
        error1 = ValidationError("Error 1", field="email")
        error2 = RateLimitError("Rate limited", service="slack")
        
        tracker.track_error(error1)
        tracker.track_error(error2)
        
        metrics = tracker.get_metrics()
        assert metrics["total_errors"] == 2
        assert metrics["recoverable_errors"] == 1
        assert metrics["unrecoverable_errors"] == 1

    def test_errors_by_type(self):
        """Test getting errors by type."""
        tracker = ErrorTracker()
        
        error1 = ValidationError("Error 1", field="email")
        error2 = ValidationError("Error 2", field="phone")
        error3 = RateLimitError("Rate limited", service="slack")
        
        tracker.track_error(error1)
        tracker.track_error(error2)
        tracker.track_error(error3)
        
        errors_by_type = tracker.get_errors_by_type()
        assert errors_by_type["VALIDATION_ERROR"] == 2
        assert errors_by_type["RATE_LIMIT_ERROR"] == 1

    def test_error_history_limit(self):
        """Test that error history is bounded."""
        tracker = ErrorTracker()
        tracker.max_history_size = 10
        
        for i in range(20):
            error = ValidationError(f"Error {i}", field="test")
            tracker.track_error(error)
        
        assert len(tracker.error_history) == 10

    def test_get_error_history(self):
        """Test getting error history."""
        tracker = ErrorTracker()
        
        for i in range(5):
            error = ValidationError(f"Error {i}", field="test")
            tracker.track_error(error)
        
        history = tracker.get_error_history(limit=3)
        assert len(history) == 3


@pytest.mark.unit
class TestErrorIntegration:
    """Integration tests for error handling."""

    @pytest.mark.async
    async def test_retry_with_fallback(self):
        """Test combining retry with fallback."""
        call_count = 0
        
        @retry(policy=RetryPolicy(max_attempts=2, initial_delay=0.01))
        async def flaky_function():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise TimeoutError("Temporary")
            return "success"
        
        try:
            result = await flaky_function()
            assert result == "success"
        except TimeoutError:
            result = "fallback"
        
        assert result == "success"

    def test_error_tracking_workflow(self):
        """Test error tracking in workflow context."""
        tracker = ErrorTracker()
        
        # Simulate workflow errors
        errors = [
            ValidationError("Invalid order", field="items"),
            RateLimitError("Stripe rate limited", service="stripe"),
            TimeoutError("Payment timeout", operation="charge"),
        ]
        
        for error in errors:
            tracker.track_error(error, workflow_id="wf_123")
        
        # Check metrics
        metrics = tracker.get_metrics()
        assert metrics["total_errors"] == 3
        assert metrics["recoverable_errors"] == 2
        assert metrics["unrecoverable_errors"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
