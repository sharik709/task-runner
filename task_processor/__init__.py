"""
Task Processor - A flexible and extensible task processing system
"""

from task_processor.core.models import Task, Schedule, RetryConfig
from task_processor.core.scheduler import TaskScheduler
from task_processor.core.executor import TaskExecutor
from task_processor.utils.config_loader import ConfigLoader
from task_processor.utils.logging import LogManager, LogConfig

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
