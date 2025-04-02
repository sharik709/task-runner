import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from loguru import logger
from pydantic import BaseModel, Field


class LogConfig(BaseModel):
    """Configuration for logging."""

    log_dir: str = Field(default="~/.task_processor/logs")
    max_files: int = Field(default=10)
    rotation: str = Field(default="1 day")
    retention: str = Field(default="1 week")
    compression: str = Field(default="zip")
    format: str = Field(
        default="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )


class TaskLogger:
    """Manages logging for a specific task"""

    def __init__(self, task_name: str, log_dir: Path, config: LogConfig):
        self.task_name = task_name
        self.log_dir = log_dir / task_name
        self.config = config
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Configure task-specific logger
        self.logger = logger.bind(task=task_name)
        log_file = self.log_dir / f"{task_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.logger.add(
            str(log_file),
            rotation=config.rotation,
            retention=config.retention,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        )

    def info(self, message: str):
        """Log an info message."""
        self.logger.info(message)

    def debug(self, message: str):
        """Log a debug message."""
        self.logger.debug(message)

    def error(self, message: str):
        """Log an error message."""
        self.logger.error(message)

    def log_start(self):
        self.logger.info(f"Starting task: {self.task_name}")

    def log_success(self, message: str = ""):
        self.logger.success(f"Task completed successfully: {message}")

    def log_error(self, error: str):
        self.logger.error(f"Task failed: {error}")

    def cleanup_old_logs(self):
        """Remove old log files if we exceed max_files"""
        log_files = sorted(self.log_dir.glob("*.log"), key=os.path.getctime, reverse=True)
        for log_file in log_files[self.config.max_files :]:
            log_file.unlink()


class LogManager:
    """Manages logging configuration and log file rotation."""

    def __init__(self, config: LogConfig):
        self.config = config
        self.log_dir = Path(config.log_dir).expanduser()
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.task_loggers: Dict[str, TaskLogger] = {}
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging with the specified settings."""
        # Remove default handler
        logger.remove()

        # Add console handler
        logger.add(sys.stderr, format=self.config.format, level="INFO", colorize=True)

        # Add file handler
        log_file = self.log_dir / "task_processor.log"
        logger.add(
            str(log_file),
            format=self.config.format,
            level="DEBUG",
            rotation=self.config.rotation,
            retention=self.config.retention,
            compression=self.config.compression,
        )

    def get_log_file(self, task_name: str) -> Path:
        """Get the log file path for a specific task."""
        return self.log_dir / f"{task_name}.log"

    def setup_task_logging(self, task_name: str):
        """Set up logging for a specific task."""
        log_file = self.get_log_file(task_name)
        logger.add(
            str(log_file),
            format=self.config.format,
            level="DEBUG",
            rotation=self.config.rotation,
            retention=self.config.retention,
            compression=self.config.compression,
            filter=lambda record: record["extra"].get("task_name") == task_name,
        )

    def get_logger(self, task_name: str) -> TaskLogger:
        """Get or create a logger for a task"""
        if task_name not in self.task_loggers:
            log_file = self.get_log_file(task_name)
            logger.add(
                str(log_file),
                format=self.config.format,
                level="DEBUG",
                rotation=self.config.rotation,
                retention=self.config.retention,
                compression=self.config.compression,
                filter=lambda record: record["extra"].get("task_name") == task_name,
            )
            self.task_loggers[task_name] = TaskLogger(task_name, self.log_dir, self.config)
        return self.task_loggers[task_name]

    def cleanup_all_logs(self):
        """Cleanup logs for all tasks"""
        for logger in self.task_loggers.values():
            logger.cleanup_old_logs()

    def rotate_all_logs(self):
        """Rotate logs for all tasks"""
        for logger in self.task_loggers.values():
            logger.log_dir.glob("*.log")
