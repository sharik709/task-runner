import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional
from loguru import logger
from pydantic import BaseModel

class LogConfig(BaseModel):
    """Logging configuration"""
    base_dir: str = "logs"
    retention_days: int = 30
    max_invocations: int = 100
    rotation_size: str = "100 MB"
    compression: str = "zip"

class TaskLogger:
    """Manages logging for a specific task"""

    def __init__(self, task_name: str, config: LogConfig):
        self.task_name = task_name
        self.config = config
        self._setup_logging()

    def _setup_logging(self):
        """Setup logging for the task"""
        # Create task-specific log directory
        self.log_dir = Path(self.config.base_dir) / self.task_name
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Create invocation-specific log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"invocation_{timestamp}.log"

        # Add file logger
        logger.add(
            str(self.log_file),
            rotation=self.config.rotation_size,
            compression=self.config.compression,
            retention=f"{self.config.retention_days} days",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
            level="DEBUG"
        )

        # Add console logger with task context
        logger.add(
            lambda msg: print(f"[{self.task_name}] {msg}"),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
            level="INFO"
        )

    def cleanup_old_logs(self):
        """Cleanup old log files based on retention policy"""
        try:
            # Get all log files for this task
            log_files = sorted(self.log_dir.glob("invocation_*.log*"))

            # Remove old files if we exceed max_invocations
            if len(log_files) > self.config.max_invocations:
                for old_file in log_files[:-self.config.max_invocations]:
                    old_file.unlink()

            # Remove files older than retention_days
            cutoff_time = time.time() - (self.config.retention_days * 24 * 60 * 60)
            for log_file in log_files:
                if log_file.stat().st_mtime < cutoff_time:
                    log_file.unlink()
        except Exception as e:
            logger.error(f"Error cleaning up logs for task {self.task_name}: {e}")

    def log_start(self):
        """Log task start"""
        logger.info(f"Starting task execution")

    def log_end(self, success: bool):
        """Log task end"""
        status = "completed successfully" if success else "failed"
        logger.info(f"Task {status}")

    def log_error(self, error: Exception):
        """Log error details"""
        logger.exception(f"Task error: {str(error)}")

    def log_retry(self, attempt: int, max_attempts: int):
        """Log retry attempt"""
        logger.warning(f"Retry attempt {attempt}/{max_attempts}")

class LogManager:
    """Manages logging for all tasks"""

    def __init__(self, config: LogConfig):
        self.config = config
        self._loggers: dict[str, TaskLogger] = {}

    def get_logger(self, task_name: str) -> TaskLogger:
        """Get or create a logger for a task"""
        if task_name not in self._loggers:
            self._loggers[task_name] = TaskLogger(task_name, self.config)
        return self._loggers[task_name]

    def cleanup_all_logs(self):
        """Cleanup logs for all tasks"""
        for logger in self._loggers.values():
            logger.cleanup_old_logs()
