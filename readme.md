# Task Runner

A robust and simple task runner that can schedule tasks from every minute to once a year, with support for one-time and recurring tasks.

## Features

- Flexible scheduling (minutes, hours, days, years)
- One-time and recurring tasks
- Per-task logging
- Configurable retry mechanism
- Task dependencies
- SQLite-based persistence
- Configuration-based task management

## Project Structure

```
task_runner/
├── config/             # Task configuration files
├── logs/              # Task logs
├── src/               # Source code
│   ├── models/        # Database models
│   ├── scheduler/     # Scheduling logic
│   ├── executor/      # Task execution
│   └── utils/         # Utility functions
├── tests/             # Test files
└── requirements.txt   # Project dependencies
```

## Configuration

Tasks are configured using YAML files in the `config` directory. Example configuration:

```yaml
tasks:
  - name: "example_task"
    schedule:
      type: "recurring"  # or "one-time"
      interval: "1h"     # for recurring tasks
      start_time: "2024-03-20T10:00:00"  # for one-time tasks
    command: "python /path/to/script.py"
    retry:
      max_attempts: 3
      delay: 60  # seconds
    dependencies: ["other_task"]
    log_level: "INFO"
```

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure your tasks in YAML files in the `config` directory

3. Run the task runner:
   ```bash
   python src/main.py
   ```

## Docker

To build and run with Docker:

```bash
docker build -t task-runner .
docker run -d --name task-runner task-runner
```

## Kubernetes

The task runner can be deployed to Kubernetes using the provided manifests in the `k8s` directory.

```python
from runner import run


@run("1", "daily", "10:00")
def daily_running_task():
    print("Daily running task")

@run("1", "hour")
def every_hour_task():
    print("Every hour task")

@run("1", "minute"):
def every_minute_task():
    print("Every minute task")

@run("once", "month")
def once_a_month_task():
    print("Once a month task")
```
