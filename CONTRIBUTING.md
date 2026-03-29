# Contributing to Helix Spirals

Thank you for your interest in contributing to Helix Spirals! This document provides guidelines and instructions for contributing.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and adhere to our Code of Conduct.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots and animated GIFs if possible**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and the expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

- Fill in the required template
- Follow the Python styleguides
- Include appropriate test cases
- Update documentation as needed
- End all files with a newline

## Development Setup

### Prerequisites

- Python 3.9 or higher
- pip or poetry
- Git

### Local Development

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/helix-spirals.git
   cd helix-spirals
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e ".[dev,integrations]"
   ```

5. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src/helix_spirals

# Run specific test file
pytest tests/test_engine.py

# Run tests matching a pattern
pytest -k "test_workflow"
```

### Code Style

We use Black for code formatting and isort for import sorting.

```bash
# Format code
black src/

# Sort imports
isort src/

# Check code style
flake8 src/

# Type checking
mypy src/
```

### Before Submitting a Pull Request

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure all tests pass:
   ```bash
   pytest
   ```
4. Ensure code style compliance:
   ```bash
   black --check src/
   isort --check-only src/
   flake8 src/
   mypy src/
   ```

## Styleguides

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for function arguments and return values
- Write docstrings for all public functions and classes
- Use meaningful variable names
- Keep functions focused and concise

### Docstring Format

```python
def my_function(param1: str, param2: int) -> bool:
    """
    Brief description of what the function does.
    
    More detailed description if needed. Explain the purpose,
    behavior, and any important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When something is invalid
        RuntimeError: When something fails at runtime
    
    Examples:
        >>> result = my_function("test", 42)
        >>> print(result)
        True
    """
    pass
```

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:
```
Add workflow validation for circular dependencies

- Implement cycle detection algorithm
- Add comprehensive test coverage
- Update documentation

Fixes #123
```

## Adding New Integrations

To add a new integration:

1. Create a new file in `src/helix_spirals/integrations/`:
   ```python
   # src/helix_spirals/integrations/my_service_connector.py
   from .base import BaseIntegration
   
   class MyServiceIntegration(BaseIntegration):
       name = "my_service"
       display_name = "My Service"
       description = "Integration with My Service API"
       
       def authenticate(self, credentials):
           # Implement authentication
           pass
       
       def execute_action(self, action, params):
           # Implement action execution
           pass
   ```

2. Register the integration in `src/helix_spirals/integrations/__init__.py`

3. Add tests in `tests/integrations/test_my_service_connector.py`

4. Update documentation with examples

5. Submit a pull request

## Documentation

- Update README.md if adding new features
- Add docstrings to all new functions and classes
- Update API documentation if changing endpoints
- Include examples for new features

## Questions?

Feel free to open an issue with the `question` label or reach out to the community on our Discord server.

## License

By contributing to Helix Spirals, you agree that your contributions will be licensed under its Apache 2.0 License.

---

**Thank you for contributing to Helix Spirals! 🎉**
