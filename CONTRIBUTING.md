# Contributing to Task Processor

Thank you for your interest in contributing to Task Processor! This document provides guidelines and instructions for contributing to the project.

## Development Setup

1. Fork the repository:
   ```bash
   git clone https://github.com/sharik709/task-processor.git
   cd task-processor
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov black isort
   ```

## Code Style

We use the following tools to maintain code quality:

- `black` for code formatting
- `isort` for import sorting
- `pytest` for testing
- `pytest-cov` for coverage reporting

Before submitting a pull request, please run:

```bash
black task_processor tests
isort task_processor tests
pytest --cov=task_processor --cov-report=term-missing
```

## Pull Request Process

1. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

3. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a pull request from your fork to the main repository.

## Testing

We use pytest for testing. To run the tests:

```bash
pytest --cov=task_processor --cov-report=term-missing
```

Make sure all tests pass and maintain or improve the test coverage before submitting a pull request.

## Documentation

- Update the README.md if you add new features or change existing ones
- Add docstrings to all new functions and classes
- Update the API documentation if you modify the public API

## Release Process

1. Update the version in `pyproject.toml`
2. Update the changelog in `CHANGELOG.md`
3. Create a new release on GitHub
4. Build and publish to PyPI:
   ```bash
   python -m build
   python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
   ```

## Questions?

If you have any questions, please open an issue or contact the maintainers.

Thank you for contributing to Task Processor!
