# Kubernetes Task Runner

A flexible task scheduler designed to work with your Kubernetes homelab environment. This tool allows you to define custom tasks with various scheduling patterns and integrates with your existing Pushover notification system.

## Features

- Schedule tasks at different intervals: minutely, hourly, daily, weekly, or monthly
- Easily add new task scripts
- Notification integration with your existing webhook
- Task status monitoring and reporting
- Command-line interface for task management

## Installation

1. Clone the repository or copy the files to your Kubernetes master node:

```bash
mkdir -p ~/k8s-task-runner/tasks
cd ~/k8s-task-runner
```

2. Save the main script (`task_runner.py`) to your directory.

3. Create a virtual environment and install the required packages:

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests schedule
```

4. Copy the example task files to the `tasks` directory or create your own.

## Configuration

The tool creates a default `config.json` file on first run:

```json
{
  "webhook_url": "http://192.168.0.141:30070/webhook"
}
```

You can modify this file to change the webhook URL or add additional configuration options.

## Creating Tasks

Tasks are Python scripts stored in the `tasks` directory. Each task must define:

1. A `run()` function that performs the actual task and returns `True` for success or `False` for failure
2. A `SCHEDULE` constant that defines when the task should run
3. Optional constants for task behavior (`ENABLED`, `NOTIFY_ON_COMPLETION`, etc.)

You can create a task template with:

```bash
python task_runner.py create check_new_pods "@every_5m" "Check for new pods in the cluster"
```

This will create a new file at `tasks/check_new_pods.py` with a basic structure that you can edit.

### Schedule Formats

The scheduler supports several formats:

- `@every_5m` - Run every 5 minutes
- `@every_1h` - Run every hour
- `@every_1d` - Run every day
- `@daily_10:00` - Run every day at 10:00
- `@weekly_monday_09:00` - Run every Monday at 09:00
- `@monthly_1_03:00` - Run on the 1st day of each month at 03:00

## Running the Task Runner

Start the task runner with:

```bash
python task_runner.py
```

For other commands:

```bash
# List all tasks
python task_runner.py list

# Run a specific task immediately
python task_runner.py run check_pod_health
```

## Running as a Service

To run the task runner as a systemd service:

1. Create a systemd service file:

```bash
sudo nano /etc/systemd/system/k8s-task-runner.service
```

2. Add the following content:

```
[Unit]
Description=Kubernetes Task Runner
After=network.target

[Service]
Type=simple
User=sharik
WorkingDirectory=/home/sharik/k8s-task-runner
ExecStart=/home/sharik/k8s-task-runner/venv/bin/python /home/sharik/k8s-task-runner/task_runner.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable k8s-task-runner
sudo systemctl start k8s-task-runner
```

4. Check the status:

```bash
sudo systemctl status k8s-task-runner
```

## Example Tasks

The repository includes several example tasks:

1. **check_pod_health.py** - Checks the health of all pods every 15 minutes
2. **backup_etcd.py** - Backs up the etcd database daily at 3 AM
3. **check_certificates.py** - Checks Kubernetes certificate expiration weekly
4. **monitor_disk_space.py** - Monitors disk space on nodes hourly

## Integration with Kubernetes

This task runner works directly with your Kubernetes cluster using the `kubectl` command-line tool. Make sure the user running the service has the proper kubeconfig setup.

## Logs

Logs are stored in `task_runner.log` in the application directory. You can monitor them with:

```bash
tail -f task_runner.log
```

## Creating Custom Tasks

Here's an example of a simple custom task that checks for high CPU usage pods:

```python
# File: tasks/check_high_cpu_pods.py
DESCRIPTION = "Detect pods with high CPU usage"
SCHEDULE = "@every_10m"
ENABLED = True
NOTIFY_ON_COMPLETION = False
NOTIFY_ON_FAILURE = True
NOTIFY_ON_ERROR = True

import subprocess
import json

def run():
    """
    Check for pods using high CPU resources
    """
    try:
        # Get top pods sorted by CPU
        result = subprocess.run(
            ["kubectl", "top", "pods", "--all-namespaces"],
            capture_output=True,
            text=True,
            check=True
        )
        
        lines = result.stdout.strip().split('\n')
        high_cpu_pods = []
        
        # Skip header
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 5:
                namespace = parts[0]
                pod_name = parts[1]
                cpu = parts[2]
                
                # Remove 'm' suffix and convert to int
                if cpu.endswith('m'):
                    cpu_value = int(cpu[:-1])
                else:
                    cpu_value = int(cpu) * 1000
                
                # Alert if CPU usage is over 500m
                if cpu_value > 500:
                    high_cpu_pods.append(f"{namespace}/{pod_name}: {cpu}")
        
        if high_cpu_pods:
            message = "High CPU usage pods detected:\n" + "\n".join(high_cpu_pods)
            print(message)
            return False
        
        print("No pods with high CPU usage detected")
        return True
    except Exception as e:
        print(f"Error checking high CPU pods: {e}")
        return False
```

With this flexible system, you can easily add more tasks or customize existing ones to suit your specific needs.
