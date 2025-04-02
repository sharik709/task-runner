# Contributing to Task Runner

Thank you for your interest in contributing to Task Runner! This document provides guidelines and steps for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/task-runner.git
   cd task-runner
   ```
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Code Style

We use several tools to maintain code quality:

- `black` for code formatting
- `isort` for import sorting
- `mypy` for type checking
- `flake8` for linting

Before committing, run:
```bash
black task_runner tests
isort task_runner tests
mypy task_runner
flake8 task_runner
```

## Testing

We use `pytest` for testing. Run tests with:
```bash
pytest
```

For coverage report:
```bash
pytest --cov=task_runner
```

## Pull Request Process

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Run tests and code quality checks
4. Commit your changes:
   ```bash
   git commit -m "Description of your changes"
   ```
5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
6. Create a Pull Request

## Code Review Guidelines

- Keep changes focused and atomic
- Write clear commit messages
- Include tests for new features
- Update documentation as needed
- Follow existing code style

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Keep documentation up to date with code changes

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. Build and publish to PyPI:
   ```bash
   python -m build
   python -m twine upload dist/*
   ```

## Questions?

Feel free to open an issue for any questions or concerns. We're happy to help!
