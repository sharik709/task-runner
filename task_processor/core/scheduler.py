import schedule
import time
from datetime import datetime
from typing import Dict, List, Optional

from task_processor.utils.logging import LogManager, LogConfig
from task_processor.core.executor import TaskExecutor
from task_processor.core.models import Task


class TaskScheduler:
    def __init__(self, log_manager: Optional[LogManager] = None):
        """Initialize the task scheduler."""
        if log_manager is None:
            config = LogConfig()
            self.log_manager = LogManager(config=config)
        else:
            self.log_manager = log_manager
        self.executor = TaskExecutor(log_manager=self.log_manager)
        self.tasks: Dict[str, Task] = {}
        self.schedule = schedule.default_scheduler

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        self.tasks[task.name] = task
        if task.schedule.type == "recurring":
            interval = task.schedule.interval
            if interval.endswith("m"):
                minutes = int(interval[:-1])
                self.schedule.every(minutes).minutes.do(self.executor.execute_task, task)
            elif interval.endswith("h"):
                hours = int(interval[:-1])
                self.schedule.every(hours).hours.do(self.executor.execute_task, task)
            elif interval.endswith("d"):
                days = int(interval[:-1])
                self.schedule.every(days).days.do(self.executor.execute_task, task)
            elif interval.endswith("y"):
                years = int(interval[:-1])
                self.schedule.every(years * 365).days.do(self.executor.execute_task, task)
        elif task.schedule.type == "one-time" and task.schedule.start_time:
            self.schedule.every().day.at(task.schedule.start_time.strftime("%H:%M")).do(self.executor.execute_task, task)

    def add_tasks(self, tasks: List[Task]) -> None:
        """Add multiple tasks to the scheduler."""
        for task in tasks:
            self.add_task(task)

    def run(self) -> None:
        """Run the scheduler."""
        while True:
            self.schedule.run_pending()
            time.sleep(1)

    def stop(self) -> None:
        """Stop all scheduled tasks"""
        schedule.clear()
        self.tasks.clear()
