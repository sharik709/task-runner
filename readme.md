# TaskOps

A flexible and extensible task processing system that allows you to schedule, execute, and monitor tasks with ease.

## Features

- **Flexible Task Scheduling**: Support for recurring and one-time tasks
- **Extensible Plugin System**: Easy integration with various services and databases
- **Robust Error Handling**: Built-in retry mechanisms and error logging
- **YAML Configuration**: Simple task configuration using YAML files
- **Comprehensive Logging**: Detailed logging with rotation and retention policies
- **Type Safety**: Full type hints and validation using Pydantic

## Installation

### From GitHub (Recommended)
```bash
pip install git+https://github.com/sharik709/task-processor.git
```

### From TestPyPI
```bash
pip install -i https://test.pypi.org/simple/ taskops
```

### From PyPI
```bash
pip install taskops
```

This will install TaskOps along with its dependencies (pydantic, schedule, loguru, and pyyaml).

## Quick Start

1. Create a task configuration file (`tasks.yaml`):

```yaml
tasks:
  - name: "backup_database"
    command: "pg_dump mydb > backup.sql"
    schedule:
      type: "recurring"
      interval: "1d"
    retry:
      max_attempts: 3
      delay: 300  # 5 minutes
```

2. Run the task processor:

```bash
taskops --config-dir /path/to/config
```

## Configuration

### Task Configuration

Tasks can be configured using YAML files. Each task can have the following properties:

```yaml
name: "task_name"          # Unique identifier for the task
command: "command_to_run"  # Shell command to execute
schedule:
  type: "recurring"        # or "one-time"
  interval: "1h"          # for recurring tasks (e.g., "1m", "1h", "1d")
  start_time: "2024-02-20T10:00:00"  # for one-time tasks
retry:
  max_attempts: 3         # Maximum number of retry attempts
  delay: 60              # Delay between retries in seconds
```

### Command Line Options

```bash
taskops [OPTIONS]

Options:
  --config-dir TEXT     Directory containing task configuration files
  --log-dir TEXT       Directory for log files
  --max-log-files INT  Maximum number of log files to keep per task
  --help              Show this message and exit
```

### Python API Usage

You can also use TaskOps directly in your Python code:

```python
from datetime import datetime
from task_processor import Task, Schedule, RetryConfig, TaskScheduler, LogManager, LogConfig

# Initialize logging (optional but recommended)
log_config = LogConfig(log_dir="./logs")
log_manager = LogManager(log_config)

# Create a task scheduler with logging
scheduler = TaskScheduler(log_manager=log_manager)

# Define a recurring task
recurring_task = Task(
    name="data_processing",
    command="python process_data.py",
    schedule=Schedule(
        type="recurring",
        interval="1h"  # Run every hour
    ),
    retry=RetryConfig(
        max_attempts=3,
        delay=60  # Retry after 60 seconds
    )
)

# Define a one-time task
one_time_task = Task(
    name="database_cleanup",
    command="python cleanup_db.py",
    schedule=Schedule(
        type="one-time",
        start_time=datetime(2024, 5, 1, 3, 0, 0)  # Run at 3 AM on May 1, 2024
    ),
    retry=RetryConfig(
        max_attempts=2,
        delay=300  # Retry after 5 minutes
    )
)

# Add tasks to the scheduler
scheduler.add_task(recurring_task)
scheduler.add_task(one_time_task)

# Start the scheduler (this will block and run until stopped)
try:
    print("Task scheduler is running. Press Ctrl+C to stop.")
    scheduler.run()
except KeyboardInterrupt:
    print("Shutting down scheduler...")
    scheduler.stop()
```

For a complete working example, see [example_taskops.py](example_taskops.py).

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/sharik709/task-processor.git
cd task-processor
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

### Running Tests

```bash
pytest
```

For coverage report:
```bash
pytest --cov=task_processor --cov-report=term-missing
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
