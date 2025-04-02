import schedule
import time
import subprocess
from datetime import datetime, timedelta
from typing import Dict, Optional
from task_runner.utils.logging import LogManager
from task_runner.core.models import Task

class TaskScheduler:
    def __init__(self, log_manager: LogManager):
        self.log_manager = log_manager
        self.scheduled_tasks: Dict[str, Task] = {}

    def schedule_task(self, task: Task) -> None:
        """Schedule a task based on its configuration"""
        self.scheduled_tasks[task.name] = task
        logger = self.log_manager.get_logger(task.name)

        if task.schedule.type == "recurring":
            interval = task.schedule.interval
            if interval.endswith("m"):
                schedule.every(int(interval[:-1])).minutes.do(self._run_task, task)
            elif interval.endswith("h"):
                schedule.every(int(interval[:-1])).hours.do(self._run_task, task)
            elif interval.endswith("d"):
                schedule.every(int(interval[:-1])).days.do(self._run_task, task)
            else:
                raise ValueError(f"Unsupported interval format: {interval}")
        elif task.schedule.type == "one-time":
            if task.schedule.start_time > datetime.now():
                schedule.every().day.at(task.schedule.start_time.strftime("%H:%M")).do(self._run_task, task)

    def _run_task(self, task: Task) -> None:
        """Execute a task and handle its output"""
        logger = self.log_manager.get_logger(task.name)
        logger.log_start()

        try:
            result = subprocess.run(
                task.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=task.timeout if hasattr(task, 'timeout') else None
            )

            task.last_run = datetime.now()
            if result.returncode == 0:
                task.last_status = "success"
                logger.log_success(result.stdout)
            else:
                task.last_status = "failed"
                logger.log_error(f"Exit code {result.returncode}: {result.stderr}")
                self._handle_failure(task)

        except subprocess.TimeoutExpired:
            task.last_status = "timeout"
            logger.log_error("Task execution timed out")
            self._handle_failure(task)
        except Exception as e:
            task.last_status = "error"
            logger.log_error(str(e))
            self._handle_failure(task)

    def _handle_failure(self, task: Task) -> None:
        """Handle task failure and retry logic"""
        task.attempts += 1
        if task.should_retry():
            time.sleep(task.retry_delay)
            self._run_task(task)

    def run(self) -> None:
        """Run the scheduler loop"""
        while True:
            schedule.run_pending()
            time.sleep(1)

    def stop(self) -> None:
        """Stop all scheduled tasks"""
        schedule.clear()
        self.scheduled_tasks.clear()
