# Error Handling Guide

## Overview

Helix Spirals provides comprehensive error handling, recovery strategies, and structured logging to ensure robust workflow execution. This guide covers best practices for handling errors in your workflows.

## Table of Contents

1. [Exception Hierarchy](#exception-hierarchy)
2. [Retry Policies](#retry-policies)
3. [Recovery Strategies](#recovery-strategies)
4. [Structured Logging](#structured-logging)
5. [Error Tracking](#error-tracking)
6. [Best Practices](#best-practices)

---

## Exception Hierarchy

Helix Spirals uses a custom exception hierarchy for different error scenarios:

### Base Exception

```python
from helix_spirals.error_handling import SpiralException

try:
    # Your code
    pass
except SpiralException as e:
    print(f"Error: {e.message}")
    print(f"Code: {e.error_code}")
    print(f"Recoverable: {e.recoverable}")
```

### Specific Exceptions

| Exception | Use Case | Recoverable |
|-----------|----------|------------|
| `WorkflowExecutionError` | Workflow execution fails | No |
| `IntegrationError` | Integration call fails | Depends |
| `ValidationError` | Input validation fails | No |
| `RateLimitError` | API rate limit exceeded | Yes |
| `TimeoutError` | Operation times out | Yes |
| `AuthenticationError` | Authentication fails | No |

### Example: Handling Different Exceptions

```python
from helix_spirals.error_handling import (
    IntegrationError,
    RateLimitError,
    TimeoutError,
    AuthenticationError
)

try:
    result = await integration.execute_action("send_message", params)
except RateLimitError as e:
    # Retry later
    print(f"Rate limited. Retry after {e.context['retry_after']}s")
except TimeoutError as e:
    # Timeout - may retry
    print(f"Timeout after {e.context['timeout_seconds']}s")
except AuthenticationError as e:
    # Authentication failed - don't retry
    print(f"Auth failed: {e.message}")
except IntegrationError as e:
    # Generic integration error
    print(f"Integration error: {e.message}")
```

---

## Retry Policies

### Basic Retry Policy

```python
from helix_spirals.error_handling import RetryPolicy

policy = RetryPolicy(
    max_attempts=3,
    backoff_strategy="exponential",
    initial_delay=1.0,
    max_delay=300.0,
    jitter=True
)
```

### Backoff Strategies

| Strategy | Formula | Use Case |
|----------|---------|----------|
| `LINEAR` | delay = initial_delay × attempt | Simple, predictable |
| `EXPONENTIAL` | delay = initial_delay × (base ^ attempt) | Recommended for most cases |
| `FIBONACCI` | delay = initial_delay × fib(attempt) | Smooth progression |
| `RANDOM` | delay = random(initial_delay, max_delay) | Avoid thundering herd |

### Using Retry Decorator

```python
from helix_spirals.error_handling import retry, RetryPolicy

policy = RetryPolicy(
    max_attempts=3,
    backoff_strategy="exponential",
    initial_delay=1.0
)

@retry(policy=policy)
async def call_external_api():
    # This will automatically retry on transient errors
    response = await api.request()
    return response
```

### Custom Retryable Exceptions

```python
policy = RetryPolicy(
    max_attempts=3,
    retryable_exceptions=(
        TimeoutError,
        ConnectionError,
        asyncio.TimeoutError,
        RateLimitError
    )
)
```

---

## Recovery Strategies

### Retry Recovery

```python
from helix_spirals.error_handling import RetryRecoveryStrategy

strategy = RetryRecoveryStrategy(policy=retry_policy)

try:
    result = await operation()
except Exception as e:
    if await strategy.can_recover(e):
        result = await strategy.recover(e, context)
```

### Fallback Recovery

```python
from helix_spirals.error_handling import FallbackRecoveryStrategy

strategy = FallbackRecoveryStrategy(fallback_value="default_value")

try:
    result = await operation()
except Exception as e:
    if await strategy.can_recover(e):
        result = await strategy.recover(e, context)
```

### Circuit Breaker Pattern

```python
from helix_spirals.error_handling import CircuitBreakerRecoveryStrategy

strategy = CircuitBreakerRecoveryStrategy(
    failure_threshold=5,
    timeout=60  # seconds
)

try:
    result = await operation()
except Exception as e:
    if await strategy.can_recover(e):
        result = await strategy.recover(e, context)
```

---

## Structured Logging

### Basic Logging

```python
from helix_spirals.error_handling import structured_logger

# Simple log
structured_logger.info("Workflow started")

# Log with context
structured_logger.info(
    "Processing order",
    order_id="ORD-123",
    customer_id="cus_456"
)

# Log error with exception
try:
    result = await operation()
except Exception as e:
    structured_logger.error(
        "Operation failed",
        exception=e,
        operation="api_call"
    )
```

### Context Stack

```python
# Push context
structured_logger.push_context(
    workflow_id="wf_123",
    execution_id="exec_456"
)

# All subsequent logs include this context
structured_logger.info("Processing node")  # Includes workflow_id, execution_id

# Pop context
structured_logger.pop_context()
```

### Log Levels

```python
structured_logger.debug("Debug information")
structured_logger.info("Informational message")
structured_logger.warning("Warning message")
structured_logger.error("Error message", exception=e)
structured_logger.critical("Critical error")
```

---

## Error Tracking

### Track Errors

```python
from helix_spirals.error_handling import error_tracker, SpiralException

try:
    result = await operation()
except SpiralException as e:
    error_tracker.track_error(e, workflow_id="wf_123")
```

### Get Metrics

```python
# Get all metrics
metrics = error_tracker.get_metrics()
print(f"Total errors: {metrics['total_errors']}")
print(f"Recoverable: {metrics['recoverable_errors']}")
print(f"Unrecoverable: {metrics['unrecoverable_errors']}")

# Get errors by type
errors_by_type = error_tracker.get_errors_by_type()
# {'RATE_LIMIT_ERROR': 5, 'TIMEOUT_ERROR': 2, ...}

# Get error rate (errors per minute)
rate = error_tracker.get_error_rate(window_minutes=60)
print(f"Error rate: {rate} errors/minute")

# Get error history
history = error_tracker.get_error_history(limit=10)
```

---

## Best Practices

### 1. Use Appropriate Exception Types

```python
# Good: Specific exception with context
raise IntegrationError(
    "Stripe API returned 429",
    integration_type="stripe",
    status_code=429,
    recoverable=True
)

# Avoid: Generic exception
raise Exception("API error")
```

### 2. Implement Retry Logic for Transient Errors

```python
# Good: Retry on transient errors
policy = RetryPolicy(
    max_attempts=3,
    retryable_exceptions=(RateLimitError, TimeoutError)
)

@retry(policy=policy)
async def call_api():
    return await api.request()

# Avoid: No retry logic
result = await api.request()  # Will fail on transient errors
```

### 3. Use Circuit Breaker for Failing Services

```python
# Good: Protect against cascading failures
circuit_breaker = CircuitBreakerRecoveryStrategy(
    failure_threshold=5,
    timeout=60
)

try:
    result = await service.call()
except Exception as e:
    if await circuit_breaker.can_recover(e):
        result = await circuit_breaker.recover(e, context)
```

### 4. Log with Context

```python
# Good: Structured logging with context
structured_logger.push_context(
    workflow_id=workflow_id,
    execution_id=execution_id
)

structured_logger.info("Processing order", order_id=order_id)

# Avoid: Unstructured logging
print(f"Processing order {order_id}")
```

### 5. Track Errors for Analytics

```python
# Good: Track errors for monitoring
try:
    result = await operation()
except SpiralException as e:
    error_tracker.track_error(e, workflow_id=workflow_id)
    raise

# Monitor error metrics
metrics = error_tracker.get_metrics()
if metrics['error_rate'] > threshold:
    alert_ops_team()
```

### 6. Provide Fallbacks

```python
# Good: Fallback for non-critical operations
try:
    analytics_result = await analytics.track(event)
except Exception as e:
    structured_logger.warning("Analytics failed", exception=e)
    # Continue without analytics

# Avoid: Let non-critical errors fail the workflow
analytics_result = await analytics.track(event)  # Fails entire workflow
```

### 7. Handle Errors at Appropriate Levels

```python
# Good: Handle at node level
async def process_order(order):
    try:
        payment = await charge_card(order)
    except RateLimitError:
        # Retry payment
        payment = await charge_card(order)
    except PaymentError as e:
        # Log and notify
        structured_logger.error("Payment failed", exception=e)
        await notify_customer(order, "Payment failed")
        return None
    
    return payment

# Avoid: Let all errors bubble up
payment = await charge_card(order)  # No error handling
```

---

## Examples

### Example 1: Retry with Exponential Backoff

```python
from helix_spirals.error_handling import retry, RetryPolicy

policy = RetryPolicy(
    max_attempts=3,
    backoff_strategy="exponential",
    initial_delay=1.0,
    backoff_base=2.0
)

@retry(policy=policy)
async def send_slack_message(message):
    return await slack_client.send(message)

# Usage
try:
    result = await send_slack_message("Hello!")
except Exception as e:
    print(f"Failed after retries: {e}")
```

### Example 2: Graceful Degradation

```python
from helix_spirals.error_handling import FallbackRecoveryStrategy

# Try primary service, fallback to secondary
try:
    result = await primary_service.call()
except Exception as e:
    structured_logger.warning("Primary failed", exception=e)
    result = await secondary_service.call()
```

### Example 3: Error Tracking Dashboard

```python
from helix_spirals.error_handling import error_tracker

# Get metrics for dashboard
metrics = error_tracker.get_metrics()
errors_by_type = error_tracker.get_errors_by_type()
error_rate = error_tracker.get_error_rate(window_minutes=60)

dashboard_data = {
    "total_errors": metrics["total_errors"],
    "recoverable": metrics["recoverable_errors"],
    "unrecoverable": metrics["unrecoverable_errors"],
    "by_type": errors_by_type,
    "error_rate": error_rate,
    "recent_errors": error_tracker.get_error_history(limit=10)
}

return dashboard_data
```

---

## Troubleshooting

### Retries Not Working

**Problem**: Errors are not being retried.

**Solution**: Check that the exception type is in `retryable_exceptions`:

```python
policy = RetryPolicy(
    retryable_exceptions=(
        RateLimitError,
        TimeoutError,
        ConnectionError
    )
)
```

### Circuit Breaker Always Open

**Problem**: Circuit breaker won't reset.

**Solution**: Check the timeout setting:

```python
strategy = CircuitBreakerRecoveryStrategy(
    failure_threshold=5,
    timeout=60  # Increase if needed
)
```

### Missing Context in Logs

**Problem**: Context not appearing in logs.

**Solution**: Push context before logging:

```python
structured_logger.push_context(workflow_id=workflow_id)
structured_logger.info("Message")  # Now includes workflow_id
```

---

## References

- [Exception Hierarchy](../src/helix_spirals/error_handling.py)
- [Retry Patterns](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)
- [Structured Logging](https://www.kartar.net/2015/12/structured-logging/)

---

**Last Updated**: April 2, 2026  
**Version**: 1.0.0
