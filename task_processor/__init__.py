"""
Task Runner - A powerful yet simple task scheduler and automation tool.
"""

from task_runner.core.models import Task, Schedule, RetryConfig
from task_runner.core.scheduler import TaskScheduler
from task_runner.core.executor import TaskExecutor
from task_runner.utils.config_loader import ConfigLoader
from task_runner.utils.logging import LogManager, LogConfig

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "Task",
    "Schedule",
    "RetryConfig",
    "TaskScheduler",
    "TaskExecutor",
    "ConfigLoader",
    "LogManager",
    "LogConfig",
]
