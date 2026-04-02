# Testing Guide

Comprehensive guide to testing Helix Spirals workflows, integrations, and error handling.

## Table of Contents

1. [Setup](#setup)
2. [Running Tests](#running-tests)
3. [Test Structure](#test-structure)
4. [Writing Tests](#writing-tests)
5. [Fixtures and Builders](#fixtures-and-builders)
6. [Testing Patterns](#testing-patterns)
7. [Best Practices](#best-practices)

---

## Setup

### Install Test Dependencies

```bash
# Install pytest and plugins
pip install pytest pytest-asyncio pytest-cov pytest-mock

# Or with dev dependencies
pip install -e ".[dev]"
```

### Configure pytest

The project includes `pytest.ini` configuration:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
```

---

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_engine.py
```

### Run Specific Test Class

```bash
pytest tests/test_engine.py::TestSpiralEngine
```

### Run Specific Test

```bash
pytest tests/test_engine.py::TestSpiralEngine::test_engine_initialization
```

### Run with Coverage

```bash
pytest --cov=helix_spirals --cov-report=html
```

### Run Only Unit Tests

```bash
pytest -m unit
```

### Run Only Integration Tests

```bash
pytest -m integration
```

### Run Only Async Tests

```bash
pytest -m async
```

### Run Tests in Parallel

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run with 4 workers
pytest -n 4
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Print Statements

```bash
pytest -s
```

---

## Test Structure

### Directory Layout

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_engine.py           # Engine tests
├── test_integrations.py     # Integration connector tests
├── test_error_handling.py   # Error handling tests
├── test_workflows.py        # Workflow execution tests
└── test_utils.py            # Test utilities and builders
```

### Test File Organization

```python
"""
Module docstring describing what's being tested.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

# Import what you're testing
from helix_spirals import ...


@pytest.mark.unit
class TestFeature:
    """Test class for a feature."""

    def test_basic_functionality(self):
        """Test basic functionality."""
        # Arrange
        # Act
        # Assert

    @pytest.mark.async
    async def test_async_functionality(self):
        """Test async functionality."""
        # Arrange
        # Act
        # Assert
```

---

## Writing Tests

### Basic Test Structure

```python
def test_something():
    # Arrange: Set up test data
    input_data = {"key": "value"}
    
    # Act: Execute the code being tested
    result = function_under_test(input_data)
    
    # Assert: Verify the result
    assert result == expected_value
```

### Testing Async Functions

```python
@pytest.mark.async
async def test_async_function():
    """Test async function."""
    result = await async_function()
    assert result == expected_value
```

### Testing Exceptions

```python
def test_raises_exception():
    """Test that exception is raised."""
    with pytest.raises(ValueError):
        function_that_raises()

def test_exception_message():
    """Test exception message."""
    with pytest.raises(ValueError, match="Expected error"):
        function_that_raises()
```

### Testing with Mocks

```python
def test_with_mock(mock_storage):
    """Test with mocked dependency."""
    mock_storage.save = MagicMock(return_value=None)
    
    result = function_that_uses_storage(mock_storage)
    
    mock_storage.save.assert_called_once()
```

### Testing with Fixtures

```python
def test_with_fixture(spiral_engine):
    """Test using fixture."""
    assert spiral_engine is not None
    assert spiral_engine.storage is not None
```

---

## Fixtures and Builders

### Available Fixtures

#### `event_loop`

Provides event loop for async tests.

```python
@pytest.mark.async
async def test_with_event_loop(event_loop):
    """Test with event loop."""
    result = await async_function()
```

#### `mock_storage`

Mocked storage instance.

```python
def test_with_storage(mock_storage):
    """Test with mocked storage."""
    mock_storage.save_workflow = AsyncMock(return_value=None)
```

#### `spiral_engine`

SpiralEngine instance with mocked storage.

```python
def test_engine(spiral_engine):
    """Test with engine."""
    assert spiral_engine.storage is not None
```

#### `sample_execution_context`

Sample ExecutionContext for testing.

```python
def test_context(sample_execution_context):
    """Test with sample context."""
    assert sample_execution_context.workflow_id == "test_workflow_123"
```

#### `mock_redis`

Mocked Redis client.

```python
def test_with_redis(mock_redis):
    """Test with mocked Redis."""
    mock_redis.zadd = AsyncMock(return_value=1)
```

#### `mock_integration`

Mocked integration connector.

```python
def test_integration(mock_integration):
    """Test with mocked integration."""
    mock_integration.execute_action = AsyncMock(return_value={"success": True})
```

### Test Builders

#### WorkflowTestBuilder

Build workflows for testing.

```python
def test_with_builder(workflow_builder):
    """Test using workflow builder."""
    workflow = (
        workflow_builder
        .add_trigger("webhook")
        .add_action("validate")
        .add_integration("stripe", "charge")
        .connect(0, 1)
        .connect(1, 2)
        .build()
    )
    
    assert len(workflow["nodes"]) == 3
```

#### ExecutionContextBuilder

Build execution contexts for testing.

```python
def test_context_builder(context_builder):
    """Test using context builder."""
    context = (
        context_builder
        .with_variable("order_id", "ORD-123")
        .with_node_result("validate", {"valid": True})
        .with_status("completed")
        .build()
    )
    
    assert context["variables"]["order_id"] == "ORD-123"
```

#### TestDataGenerator

Generate realistic test data.

```python
def test_with_data():
    """Test with generated data."""
    order = TestDataGenerator.sample_order()
    customer = TestDataGenerator.sample_customer()
    payment = TestDataGenerator.sample_payment()
```

#### AssertionHelpers

Common assertions for workflows.

```python
def test_with_assertions(assertions):
    """Test using assertion helpers."""
    workflow = build_workflow()
    assertions.assert_workflow_valid(workflow)
    
    context = execute_workflow(workflow)
    assertions.assert_execution_successful(context)
```

---

## Testing Patterns

### Testing Retry Logic

```python
@pytest.mark.async
async def test_retry_on_transient_error():
    """Test retry on transient error."""
    call_count = 0
    
    @retry(policy=RetryPolicy(max_attempts=3, initial_delay=0.01))
    async def flaky_function():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise TimeoutError("Temporary")
        return "success"
    
    result = await flaky_function()
    assert result == "success"
    assert call_count == 2
```

### Testing Error Recovery

```python
@pytest.mark.async
async def test_error_recovery():
    """Test error recovery."""
    strategy = FallbackRecoveryStrategy(fallback_value="default")
    
    error = Exception("Something failed")
    can_recover = await strategy.can_recover(error)
    assert can_recover is True
    
    result = await strategy.recover(error, {})
    assert result == "default"
```

### Testing Integrations

```python
@pytest.mark.async
async def test_slack_integration(mock_integration):
    """Test Slack integration."""
    mock_integration.name = "slack"
    mock_integration.execute_action = AsyncMock(
        return_value={"success": True, "message_ts": "123"}
    )
    
    result = await mock_integration.execute_action(
        action="send_message",
        params={"channel": "#alerts", "message": "Test"}
    )
    
    assert result["success"] is True
    mock_integration.execute_action.assert_called_once()
```

### Testing Workflows

```python
def test_order_processing_workflow(workflow_builder, test_data):
    """Test order processing workflow."""
    workflow = (
        workflow_builder
        .add_trigger("webhook")
        .add_action("validate_order")
        .add_integration("stripe", "create_charge")
        .add_integration("email", "send_email")
        .connect(0, 1)
        .connect(1, 2)
        .connect(2, 3)
        .build()
    )
    
    order = test_data.sample_order()
    assert order["order_id"] is not None
    assert len(workflow["nodes"]) == 4
```

---

## Best Practices

### 1. Use Descriptive Test Names

```python
# Good
def test_retry_succeeds_after_transient_failure():
    pass

# Avoid
def test_retry():
    pass
```

### 2. Follow AAA Pattern

```python
def test_something():
    # Arrange
    data = setup_test_data()
    
    # Act
    result = function_under_test(data)
    
    # Assert
    assert result == expected
```

### 3. Test One Thing Per Test

```python
# Good
def test_validates_email():
    assert validate_email("test@example.com") is True

def test_rejects_invalid_email():
    assert validate_email("invalid") is False

# Avoid
def test_email_validation():
    assert validate_email("test@example.com") is True
    assert validate_email("invalid") is False
```

### 4. Use Fixtures for Setup

```python
# Good
def test_with_fixture(spiral_engine):
    result = spiral_engine.validate_workflow(workflow)
    assert result is True

# Avoid
def test_without_fixture():
    engine = SpiralEngine(storage=MockStorage())
    result = engine.validate_workflow(workflow)
    assert result is True
```

### 5. Mock External Dependencies

```python
# Good
def test_with_mock(mock_storage):
    mock_storage.save = AsyncMock(return_value=None)
    # Test code

# Avoid
def test_without_mock():
    # Actual database call
    storage.save(data)
```

### 6. Test Error Cases

```python
def test_handles_validation_error():
    """Test error handling."""
    with pytest.raises(ValidationError):
        validate_order(invalid_order)

def test_handles_rate_limit():
    """Test rate limit handling."""
    with pytest.raises(RateLimitError):
        call_rate_limited_api()
```

### 7. Use Markers for Organization

```python
@pytest.mark.unit
def test_unit_test():
    pass

@pytest.mark.integration
def test_integration_test():
    pass

@pytest.mark.async
async def test_async_test():
    pass

@pytest.mark.slow
def test_slow_test():
    pass
```

---

## Coverage Goals

| Component | Target Coverage |
|-----------|-----------------|
| Engine | 90%+ |
| Integrations | 85%+ |
| Error Handling | 95%+ |
| Workflows | 80%+ |
| Overall | 85%+ |

### Generate Coverage Report

```bash
pytest --cov=helix_spirals --cov-report=html --cov-report=term-missing
```

---

## Troubleshooting

### Async Tests Not Running

**Problem**: Async tests not being discovered.

**Solution**: Add `@pytest.mark.async` decorator and ensure `pytest-asyncio` is installed.

```python
@pytest.mark.async
async def test_async():
    result = await async_function()
```

### Fixture Not Found

**Problem**: Fixture not available in test.

**Solution**: Ensure fixture is defined in `conftest.py` or imported correctly.

```python
# In conftest.py
@pytest.fixture
def my_fixture():
    return SomeObject()
```

### Mock Not Being Called

**Problem**: Mock not recording calls.

**Solution**: Use `AsyncMock` for async functions, `MagicMock` for sync.

```python
# Good
mock = AsyncMock()
await mock()
mock.assert_called_once()

# Avoid
mock = MagicMock()
await mock()  # Won't work correctly
```

---

## References

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Testing Best Practices](https://testdriven.io/)

---

**Last Updated**: April 2, 2026  
**Version**: 1.0.0
