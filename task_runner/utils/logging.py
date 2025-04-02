import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict
from loguru import logger
from pydantic import BaseModel, Field
from dataclasses import dataclass


@dataclass
class LogConfig:
    log_dir: str = "logs"
    max_files: int = 10
    rotation: str = "100 MB"
    retention: str = "1 week"


class TaskLogger:
    """Manages logging for a specific task"""

    def __init__(self, task_name: str, log_dir: Path, config: LogConfig):
        self.task_name = task_name
        self.log_dir = log_dir / task_name
        self.config = config
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Configure task-specific logger
        self.logger = logger.bind(task=task_name)
        log_file = (
            self.log_dir / f"{task_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        self.logger.add(
            str(log_file),
            rotation=config.rotation,
            retention=config.retention,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        )

    def log_start(self):
        self.logger.info(f"Starting task: {self.task_name}")

    def log_success(self, message: str = ""):
        self.logger.success(f"Task completed successfully: {message}")

    def log_error(self, error: str):
        self.logger.error(f"Task failed: {error}")

    def cleanup_old_logs(self):
        """Remove old log files if we exceed max_files"""
        log_files = sorted(
            self.log_dir.glob("*.log"), key=os.path.getctime, reverse=True
        )
        for log_file in log_files[self.config.max_files :]:
            log_file.unlink()


class LogManager:
    """Manages logging for all tasks"""

    def __init__(self, config: LogConfig):
        self.config = config
        self.log_dir = Path(config.log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.task_loggers: Dict[str, TaskLogger] = {}

    def get_logger(self, task_name: str) -> TaskLogger:
        """Get or create a logger for a task"""
        if task_name not in self.task_loggers:
            self.task_loggers[task_name] = TaskLogger(
                task_name, self.log_dir, self.config
            )
        return self.task_loggers[task_name]

    def cleanup_all_logs(self):
        """Cleanup logs for all tasks"""
        for logger in self.task_loggers.values():
            logger.cleanup_old_logs()

    def rotate_all_logs(self):
        """Rotate logs for all tasks"""
        for logger in self.task_loggers.values():
            logger.log_dir.glob("*.log")
