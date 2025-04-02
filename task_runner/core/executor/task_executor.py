import subprocess
import time
from datetime import datetime
from loguru import logger
import os
from typing import Optional

class TaskExecutor:
    def __init__(self, task_name: str, command: str, retry_max_attempts: int = 3, retry_delay: int = 60):
        self.task_name = task_name
        self.command = command
        self.retry_max_attempts = retry_max_attempts
        self.retry_delay = retry_delay

        # Setup task-specific logger
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        logger.add(
            f"{log_dir}/{task_name}.log",
            rotation="1 day",
            retention="7 days",
            level="INFO"
        )

    def execute(self) -> bool:
        """
        Execute the task with retry mechanism.
        Returns True if task completed successfully, False otherwise.
        """
        attempt = 0
        while attempt < self.retry_max_attempts:
            attempt += 1
            logger.info(f"Starting task '{self.task_name}' (attempt {attempt}/{self.retry_max_attempts})")

            try:
                # Execute the command
                process = subprocess.Popen(
                    self.command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                # Read output in real-time
                while True:
                    output = process.stdout.readline()
                    if output:
                        logger.info(output.strip())
                    error = process.stderr.readline()
                    if error:
                        logger.error(error.strip())

                    # Check if process has finished
                    if process.poll() is not None:
                        break

                # Get the return code
                return_code = process.poll()

                if return_code == 0:
                    logger.success(f"Task '{self.task_name}' completed successfully")
                    return True
                else:
                    logger.error(f"Task '{self.task_name}' failed with return code {return_code}")

            except Exception as e:
                logger.exception(f"Error executing task '{self.task_name}': {str(e)}")

            # If we get here, the task failed
            if attempt < self.retry_max_attempts:
                logger.warning(f"Retrying task '{self.task_name}' in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)

        logger.error(f"Task '{self.task_name}' failed after {self.retry_max_attempts} attempts")
        return False
