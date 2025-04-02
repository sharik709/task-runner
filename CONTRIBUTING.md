# Contributing to Task Runner

Thank you for your interest in contributing to Task Runner! This document provides guidelines and instructions for contributing to the project.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/sharik709/task-runner.git
cd task-runner
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
```

## Code Style

We use several tools to maintain code quality and consistency:

### Code Formatting

Before committing your changes, please format your code using:

```bash
# Format code with black
black .

# Sort imports with isort
isort .
```

You can also set up pre-commit hooks to automatically format your code before each commit. To do this:

1. Install pre-commit:
```bash
pip install pre-commit
```

2. Install the git hooks:
```bash
pre-commit install
```

Now your code will be automatically formatted before each commit.

### Type Checking

We use mypy for static type checking. Run it locally with:

```bash
mypy task_runner tests
```

### Linting

We use flake8 for code linting. Run it locally with:

```bash
flake8 task_runner tests
```

## Running Tests

Before submitting a pull request, ensure all tests pass:

```bash
# Run tests with coverage
pytest --cov=task_runner --cov-report=term-missing
```

## Pull Request Process

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit them:
```bash
git add .
git commit -m "feat: your feature description"
```

3. Push your changes:
```bash
git push origin feature/your-feature-name
```

4. Create a pull request from your branch to main.

## Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification. Your commit messages should be formatted as:

```
type(scope): description
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

Example:
```
feat(scheduler): add support for one-time tasks
```

## CI/CD Pipeline

Our CI/CD pipeline runs the following checks:
- Code formatting (black and isort)
- Type checking (mypy)
- Linting (flake8)
- Tests with coverage reporting
- Package building and validation

All checks must pass before a pull request can be merged.

## Need Help?

If you have any questions or need help, please:
1. Check the existing documentation
2. Open an issue
3. Join our community discussions

Thank you for contributing to Task Runner!
