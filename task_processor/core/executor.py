import subprocess
from typing import Optional
import time

from task_processor.core.models import Task
from task_processor.utils.logging import LogManager, LogConfig


class TaskExecutor:
    def __init__(self, log_manager: Optional[LogManager] = None):
        """Initialize the task executor."""
        self.log_manager = log_manager or LogManager(LogConfig())

    def execute_task(self, task: Task) -> None:
        """Execute a task and handle its output."""
        logger = self.log_manager.get_logger(task.name)
        logger.info(f"Starting task: {task.name}")

        try:
            result = subprocess.run(
                task.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=task.timeout if hasattr(task, "timeout") else None,
            )

            if result.returncode == 0:
                logger.info(f"Task {task.name} completed successfully")
                logger.debug(result.stdout)
            else:
                logger.error(f"Task {task.name} failed with exit code {result.returncode}")
                logger.error(result.stderr)
                self._handle_failure(task)

        except subprocess.TimeoutExpired:
            logger.error(f"Task {task.name} timed out")
            self._handle_failure(task)
        except Exception as e:
            logger.error(f"Task {task.name} failed with error: {str(e)}")
            self._handle_failure(task)

    def _handle_failure(self, task: Task) -> None:
        """Handle task failure and retry logic."""
        if task.retry and task.retry.max_attempts > 0:
            task.retry.max_attempts -= 1
            logger = self.log_manager.get_logger(task.name)
            logger.info(f"Retrying task {task.name} in {task.retry.delay} seconds")
            time.sleep(task.retry.delay)
            self.execute_task(task)
