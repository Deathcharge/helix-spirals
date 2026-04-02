"""
Enhanced Error Handling and Logging
====================================

Comprehensive error handling, recovery strategies, and structured logging
for Helix Spirals workflows.

Features:
- Custom exception hierarchy
- Retry policies with exponential backoff
- Error recovery strategies
- Structured logging with context
- Error tracking and analytics
- Graceful degradation patterns
"""

import logging
import asyncio
import json
from datetime import datetime, UTC, timedelta
from typing import Any, Callable, Optional, Dict, List, TypeVar
from enum import Enum
from dataclasses import dataclass, asdict
from functools import wraps
import traceback

logger = logging.getLogger(__name__)


# ============================================================================
# EXCEPTION HIERARCHY
# ============================================================================

class SpiralException(Exception):
    """Base exception for all Helix Spirals errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "SPIRAL_ERROR",
        context: Dict[str, Any] = None,
        recoverable: bool = False
    ):
        self.message = message
        self.error_code = error_code
        self.context = context or {}
        self.recoverable = recoverable
        self.timestamp = datetime.now(UTC)
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for logging."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "context": self.context,
            "recoverable": self.recoverable,
            "timestamp": self.timestamp.isoformat()
        }


class WorkflowExecutionError(SpiralException):
    """Raised when workflow execution fails."""

    def __init__(self, message: str, workflow_id: str, node_id: str = None, **kwargs):
        super().__init__(
            message,
            error_code="WORKFLOW_EXECUTION_ERROR",
            context={"workflow_id": workflow_id, "node_id": node_id},
            **kwargs
        )


class IntegrationError(SpiralException):
    """Raised when an integration fails."""

    def __init__(
        self,
        message: str,
        integration_type: str,
        action: str = None,
        status_code: int = None,
        **kwargs
    ):
        super().__init__(
            message,
            error_code="INTEGRATION_ERROR",
            context={
                "integration_type": integration_type,
                "action": action,
                "status_code": status_code
            },
            **kwargs
        )


class ValidationError(SpiralException):
    """Raised when validation fails."""

    def __init__(self, message: str, field: str = None, value: Any = None, **kwargs):
        super().__init__(
            message,
            error_code="VALIDATION_ERROR",
            context={"field": field, "value": str(value)},
            **kwargs
        )


class RateLimitError(SpiralException):
    """Raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str,
        service: str,
        retry_after: int = None,
        **kwargs
    ):
        super().__init__(
            message,
            error_code="RATE_LIMIT_ERROR",
            context={"service": service, "retry_after": retry_after},
            recoverable=True,
            **kwargs
        )


class TimeoutError(SpiralException):
    """Raised when operation times out."""

    def __init__(
        self,
        message: str,
        operation: str,
        timeout_seconds: int = None,
        **kwargs
    ):
        super().__init__(
            message,
            error_code="TIMEOUT_ERROR",
            context={"operation": operation, "timeout_seconds": timeout_seconds},
            recoverable=True,
            **kwargs
        )


class AuthenticationError(SpiralException):
    """Raised when authentication fails."""

    def __init__(self, message: str, service: str = None, **kwargs):
        super().__init__(
            message,
            error_code="AUTHENTICATION_ERROR",
            context={"service": service},
            **kwargs
        )


# ============================================================================
# RETRY POLICIES AND STRATEGIES
# ============================================================================

class BackoffStrategy(Enum):
    """Backoff strategies for retries."""
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    FIBONACCI = "fibonacci"
    RANDOM = "random"


@dataclass
class RetryPolicy:
    """Configuration for retry behavior."""

    max_attempts: int = 3
    backoff_strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL
    backoff_base: float = 2.0
    initial_delay: float = 1.0
    max_delay: float = 300.0
    jitter: bool = True
    timeout: float = 30.0
    retryable_exceptions: tuple = (
        RateLimitError,
        TimeoutError,
        ConnectionError,
        asyncio.TimeoutError
    )

    def get_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt number."""
        import random

        if self.backoff_strategy == BackoffStrategy.LINEAR:
            delay = self.initial_delay * attempt
        elif self.backoff_strategy == BackoffStrategy.EXPONENTIAL:
            delay = self.initial_delay * (self.backoff_base ** attempt)
        elif self.backoff_strategy == BackoffStrategy.FIBONACCI:
            fib = self._fibonacci(attempt)
            delay = self.initial_delay * fib
        else:  # RANDOM
            delay = random.uniform(self.initial_delay, self.max_delay)

        # Apply jitter
        if self.jitter:
            jitter_amount = delay * 0.1 * random.random()
            delay += jitter_amount

        # Cap at max delay
        return min(delay, self.max_delay)

    @staticmethod
    def _fibonacci(n: int) -> int:
        """Calculate nth Fibonacci number."""
        if n <= 1:
            return 1
        a, b = 1, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return b


# ============================================================================
# RETRY DECORATORS
# ============================================================================

T = TypeVar('T')


def retry(policy: RetryPolicy = None):
    """Decorator for retrying async functions with backoff."""
    if policy is None:
        policy = RetryPolicy()

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_exception = None

            for attempt in range(policy.max_attempts):
                try:
                    return await func(*args, **kwargs)
                except policy.retryable_exceptions as e:
                    last_exception = e
                    
                    if attempt < policy.max_attempts - 1:
                        delay = policy.get_delay(attempt)
                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                            f"Retrying in {delay:.2f}s..."
                        )
                        await asyncio.sleep(delay)
                    else:
                        logger.error(
                            f"All {policy.max_attempts} attempts failed for {func.__name__}"
                        )

            raise last_exception

        return wrapper

    return decorator


def retry_sync(policy: RetryPolicy = None):
    """Decorator for retrying synchronous functions with backoff."""
    if policy is None:
        policy = RetryPolicy()

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            import time
            last_exception = None

            for attempt in range(policy.max_attempts):
                try:
                    return func(*args, **kwargs)
                except policy.retryable_exceptions as e:
                    last_exception = e
                    
                    if attempt < policy.max_attempts - 1:
                        delay = policy.get_delay(attempt)
                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                            f"Retrying in {delay:.2f}s..."
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"All {policy.max_attempts} attempts failed for {func.__name__}"
                        )

            raise last_exception

        return wrapper

    return decorator


# ============================================================================
# ERROR RECOVERY STRATEGIES
# ============================================================================

class ErrorRecoveryStrategy:
    """Base class for error recovery strategies."""

    async def can_recover(self, error: Exception) -> bool:
        """Check if this strategy can recover from the error."""
        raise NotImplementedError

    async def recover(self, error: Exception, context: Dict[str, Any]) -> Any:
        """Attempt to recover from the error."""
        raise NotImplementedError


class RetryRecoveryStrategy(ErrorRecoveryStrategy):
    """Recovery strategy that retries the operation."""

    def __init__(self, policy: RetryPolicy = None):
        self.policy = policy or RetryPolicy()

    async def can_recover(self, error: Exception) -> bool:
        """Can recover if error is retryable."""
        return isinstance(error, self.policy.retryable_exceptions)

    async def recover(self, error: Exception, context: Dict[str, Any]) -> Any:
        """Retry the operation."""
        logger.info(f"Attempting retry recovery for: {error}")
        # Implementation depends on context


class FallbackRecoveryStrategy(ErrorRecoveryStrategy):
    """Recovery strategy that uses a fallback value."""

    def __init__(self, fallback_value: Any):
        self.fallback_value = fallback_value

    async def can_recover(self, error: Exception) -> bool:
        """Can always recover with fallback."""
        return True

    async def recover(self, error: Exception, context: Dict[str, Any]) -> Any:
        """Return fallback value."""
        logger.info(f"Using fallback value for error: {error}")
        return self.fallback_value


class CircuitBreakerRecoveryStrategy(ErrorRecoveryStrategy):
    """Recovery strategy using circuit breaker pattern."""

    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    async def can_recover(self, error: Exception) -> bool:
        """Check if circuit breaker allows recovery."""
        if self.is_open:
            # Check if timeout has passed
            if self.last_failure_time:
                elapsed = (datetime.now(UTC) - self.last_failure_time).total_seconds()
                if elapsed > self.timeout:
                    self.is_open = False
                    self.failure_count = 0
                    logger.info("Circuit breaker reset")
                    return True
            return False
        return True

    async def recover(self, error: Exception, context: Dict[str, Any]) -> Any:
        """Track failures and open circuit if threshold exceeded."""
        self.failure_count += 1
        self.last_failure_time = datetime.now(UTC)

        if self.failure_count >= self.failure_threshold:
            self.is_open = True
            logger.error(
                f"Circuit breaker opened after {self.failure_count} failures"
            )
            raise SpiralException(
                "Circuit breaker is open",
                error_code="CIRCUIT_BREAKER_OPEN"
            )


# ============================================================================
# STRUCTURED LOGGING
# ============================================================================

class StructuredLogger:
    """Structured logging with context and tracing."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.context_stack: List[Dict[str, Any]] = []

    def push_context(self, **kwargs):
        """Push context onto stack."""
        self.context_stack.append(kwargs)

    def pop_context(self):
        """Pop context from stack."""
        if self.context_stack:
            self.context_stack.pop()

    def get_context(self) -> Dict[str, Any]:
        """Get merged context from stack."""
        merged = {}
        for ctx in self.context_stack:
            merged.update(ctx)
        return merged

    def _log(self, level: int, message: str, **kwargs):
        """Internal logging method with context."""
        context = self.get_context()
        context.update(kwargs)
        
        # Format as structured log
        log_entry = {
            "message": message,
            "timestamp": datetime.now(UTC).isoformat(),
            "context": context
        }
        
        self.logger.log(level, json.dumps(log_entry))

    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self._log(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs):
        """Log info message."""
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: str, exception: Exception = None, **kwargs):
        """Log error message."""
        if exception:
            kwargs["exception"] = {
                "type": type(exception).__name__,
                "message": str(exception),
                "traceback": traceback.format_exc()
            }
        self._log(logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self._log(logging.CRITICAL, message, **kwargs)


# ============================================================================
# ERROR TRACKING AND ANALYTICS
# ============================================================================

@dataclass
class ErrorMetrics:
    """Metrics for error tracking and analytics."""

    total_errors: int = 0
    errors_by_type: Dict[str, int] = None
    errors_by_service: Dict[str, int] = None
    recoverable_errors: int = 0
    unrecoverable_errors: int = 0
    error_rate: float = 0.0
    last_error_time: Optional[datetime] = None

    def __post_init__(self):
        if self.errors_by_type is None:
            self.errors_by_type = {}
        if self.errors_by_service is None:
            self.errors_by_service = {}

    def record_error(self, error: SpiralException):
        """Record an error."""
        self.total_errors += 1
        self.errors_by_type[error.error_code] = \
            self.errors_by_type.get(error.error_code, 0) + 1
        
        if error.recoverable:
            self.recoverable_errors += 1
        else:
            self.unrecoverable_errors += 1
        
        self.last_error_time = datetime.now(UTC)

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return asdict(self)


class ErrorTracker:
    """Track and analyze errors across workflows."""

    def __init__(self):
        self.metrics = ErrorMetrics()
        self.error_history: List[Dict[str, Any]] = []
        self.max_history_size = 1000

    def track_error(self, error: SpiralException, workflow_id: str = None):
        """Track an error."""
        self.metrics.record_error(error)
        
        error_entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "error_code": error.error_code,
            "message": error.message,
            "workflow_id": workflow_id,
            "context": error.context,
            "recoverable": error.recoverable
        }
        
        self.error_history.append(error_entry)
        
        # Keep history size bounded
        if len(self.error_history) > self.max_history_size:
            self.error_history = self.error_history[-self.max_history_size:]

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        return self.metrics.to_dict()

    def get_error_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent error history."""
        return self.error_history[-limit:]

    def get_errors_by_type(self) -> Dict[str, int]:
        """Get error count by type."""
        return self.metrics.errors_by_type.copy()

    def get_error_rate(self, window_minutes: int = 60) -> float:
        """Calculate error rate in given time window."""
        if not self.error_history:
            return 0.0
        
        cutoff_time = datetime.now(UTC) - timedelta(minutes=window_minutes)
        recent_errors = [
            e for e in self.error_history
            if datetime.fromisoformat(e["timestamp"]) > cutoff_time
        ]
        
        return len(recent_errors) / max(1, window_minutes)


# ============================================================================
# GLOBAL INSTANCES
# ============================================================================

structured_logger = StructuredLogger("helix_spirals")
error_tracker = ErrorTracker()
