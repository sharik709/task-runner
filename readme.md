# Task Processor

A flexible and extensible task processing system that allows you to schedule, execute, and monitor tasks with ease.

## Features

- **Flexible Task Scheduling**: Support for recurring and one-time tasks
- **Extensible Plugin System**: Easy integration with various services and databases
- **Robust Error Handling**: Built-in retry mechanisms and error logging
- **YAML Configuration**: Simple task configuration using YAML files
- **Comprehensive Logging**: Detailed logging with rotation and retention policies
- **Type Safety**: Full type hints and validation using Pydantic

## Installation

```bash
pip install task-processor
```

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
task-processor --config-dir /path/to/config
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
task-processor [OPTIONS]

Options:
  --config-dir TEXT     Directory containing task configuration files
  --log-dir TEXT       Directory for log files
  --max-log-files INT  Maximum number of log files to keep per task
  --help              Show this message and exit
```

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
