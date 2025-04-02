# Task Runner

A powerful yet simple task runner that helps you schedule and automate tasks with ease. Perfect for running periodic backups, generating reports, or any other scheduled operations.

## Features

- 🕒 **Flexible Scheduling**: Run tasks every minute, hour, day, or year
- 🔄 **Recurring & One-time Tasks**: Support for both recurring and one-time task execution
- 📝 **Smart Logging**: Per-task logging with automatic rotation and cleanup
- 🔄 **Retry Mechanism**: Automatic retries for failed tasks
- 🔗 **Task Dependencies**: Tasks can depend on other tasks
- 🔒 **Secure**: No shell injection vulnerabilities, safe command execution
- 🎯 **Simple**: Easy to use, yet powerful enough for complex workflows

## Installation

```bash
# Install from PyPI
pip install task-runner

# For development, install with all dev dependencies
pip install "task-runner[dev]"
```

## Quick Start

### 1. Create Your First Task

Create a file `config/tasks.yaml`:

```yaml
tasks:
  - name: "daily_backup"
    command: "python /path/to/backup.py"
    schedule:
      type: "recurring"
      interval: "1d"
    retry:
      max_attempts: 3
      delay: 300  # 5 minutes
```

### 2. Run the Task Runner

```bash
# Using the command-line tool
task-runner

# Or using Python
python -m task_runner
```

### 3. Using in Your Python Code

```python
from task_runner import TaskScheduler, ConfigLoader, LogManager, LogConfig

# Initialize components with custom log directory (optional)
config = LogConfig(log_dir="/path/to/logs")  # Default: ~/.task_runner/logs
log_manager = LogManager(config)
config_loader = ConfigLoader()
scheduler = TaskScheduler()

# Load and schedule tasks
tasks = config_loader.load_configs()
for task in tasks:
    scheduler.schedule_task(task)

# Run the scheduler
scheduler.run()
```

## Configuration Guide

### Task Configuration

Tasks are configured using YAML files. Here's a complete example:

```yaml
tasks:
  - name: "daily_backup"
    command: "python /path/to/backup.py"
    schedule:
      type: "recurring"  # or "one-time"
      interval: "1d"     # for recurring tasks
      start_time: "2024-03-25T15:00:00"  # for one-time tasks
    retry:
      max_attempts: 3
      delay: 300  # seconds
    dependencies: ["other_task"]  # Optional dependencies
```

### Schedule Types

- **Recurring Tasks**:
  - `interval`: "1m" (minute), "1h" (hour), "1d" (day), "1y" (year)
  - Example: `interval: "30m"` for every 30 minutes

- **One-time Tasks**:
  - `start_time`: ISO format datetime
  - Example: `start_time: "2024-03-25T15:00:00"`

## Logging System

Logs are automatically organized by task and invocation:

```
~/.task_runner/logs/
├── daily_backup/
│   ├── invocation_20240325_150000.log
│   └── invocation_20240326_150000.log
└── weekly_report/
    ├── invocation_20240325_160000.log
    └── invocation_20240326_160000.log
```

Features:
- Per-task logging directories
- Per-invocation log files
- Automatic log rotation and cleanup
- Configurable log directory
- Default max of 10 log files per task

## Security Features

- Command execution is done safely without shell injection vulnerabilities
- All file operations use secure paths
- Log files are created with appropriate permissions
- No sensitive data is stored in logs
- Input validation for all configuration files

## Development

### Running Tests

```bash
# Install dev dependencies
pip install "task-runner[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=task_runner
```

### Code Style

```bash
# Format code
black task_runner tests

# Sort imports
isort task_runner tests

# Type checking
mypy task_runner
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
