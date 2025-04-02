"""
Task Runner - A powerful yet simple task scheduling and automation tool.
"""

from .core.models import Task
from .core.database import Database
from .core.scheduler import TaskScheduler
from .core.executor import TaskExecutor
from .utils.config_loader import ConfigLoader
from .utils.logging import LogManager, LogConfig
from .plugins.base import PluginManager, BasePlugin, PluginConfig

__version__ = "0.1.0"
__all__ = [
    "Task",
    "Database",
    "TaskScheduler",
    "TaskExecutor",
    "ConfigLoader",
    "LogManager",
    "LogConfig",
    "PluginManager",
    "BasePlugin",
    "PluginConfig",
]
