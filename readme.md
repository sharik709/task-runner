# Task Runner

A powerful yet simple task runner that helps you schedule and automate tasks with ease. Perfect for running periodic backups, generating reports, or any other scheduled operations.

## Features

- 🕒 **Flexible Scheduling**: Run tasks every minute, hour, day, or year
- 🔄 **Recurring & One-time Tasks**: Support for both recurring and one-time task execution
- 🔌 **Plugin System**: Built-in support for MySQL, PostgreSQL, Redis, and HTTP operations
- 📝 **Smart Logging**: Per-task logging with automatic rotation and cleanup
- 🔄 **Retry Mechanism**: Automatic retries for failed tasks
- 🔗 **Task Dependencies**: Tasks can depend on other tasks
- 🐳 **Docker Ready**: Easy to containerize and deploy
- ☸️ **Kubernetes Support**: Ready to run in your K8s cluster

## Installation

```bash
# Install from PyPI
pip install task-runner

# Or install with all optional dependencies
pip install "task-runner[all]"
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
    plugins:
      - name: "mysql"
        config:
          host: "localhost"
          port: 3306
          user: "backup_user"
          database: "my_db"
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

# Initialize components
config_loader = ConfigLoader()
log_manager = LogManager(LogConfig())
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
      delay: 300
    dependencies: ["other_task"]  # Optional dependencies
    plugins:  # Optional plugins
      - name: "mysql"
        config:
          host: "localhost"
          port: 3306
          user: "user"
          database: "db"
```

### Schedule Types

- **Recurring Tasks**:
  - `interval`: "1m" (minute), "1h" (hour), "1d" (day), "1y" (year)
  - Example: `interval: "30m"` for every 30 minutes

- **One-time Tasks**:
  - `start_time`: ISO format datetime
  - Example: `start_time: "2024-03-25T15:00:00"`

### Available Plugins

#### MySQL Plugin
```yaml
plugins:
  - name: "mysql"
    config:
      host: "localhost"
      port: 3306
      user: "user"
      password: "password"
      database: "db"
```

#### PostgreSQL Plugin
```yaml
plugins:
  - name: "postgres"
    config:
      host: "localhost"
      port: 5432
      user: "user"
      password: "password"
      database: "db"
```

#### Redis Plugin
```yaml
plugins:
  - name: "redis"
    config:
      host: "localhost"
      port: 6379
      password: "password"
      db: 0
```

#### HTTP Plugin
```yaml
plugins:
  - name: "http"
    config:
      base_url: "https://api.example.com"
      headers:
        Authorization: "Bearer token"
```

## Logging System

Logs are automatically organized by task and invocation:

```
logs/
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
- Automatic log rotation and compression
- Configurable retention policy

## Deployment

### Docker

```bash
# Build the image
docker build -t task-runner .

# Run the container
docker run -d \
  -v /path/to/config:/app/config \
  -v /path/to/logs:/app/logs \
  task-runner
```

### Kubernetes

1. Apply the Kubernetes manifests:
```bash
kubectl apply -f k8s/
```

2. Configure your tasks in the ConfigMap:
```bash
kubectl edit configmap task-runner-config
```

3. Monitor the deployment:
```bash
kubectl logs -f deployment/task-runner
```

## Development

### Project Structure
```
task_runner/
├── core/           # Core functionality
├── plugins/        # Plugin implementations
│   ├── mysql/
│   ├── postgres/
│   ├── redis/
│   └── http/
└── utils/          # Utility functions
```

### Adding New Plugins

1. Create a new plugin class in `plugins/your_plugin/plugin.py`
2. Inherit from `BasePlugin`
3. Implement required methods
4. Register the plugin in `setup.py`

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
