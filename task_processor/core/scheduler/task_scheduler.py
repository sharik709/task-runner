import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, Optional
from loguru import logger
from models.task import Task
from models.database import Database
from executor.task_executor import TaskExecutor


class TaskScheduler:
    def __init__(self):
        self.db = Database.get_instance()
        self.scheduled_tasks: Dict[str, schedule.Job] = {}
        self.running_tasks: Dict[str, bool] = {}

    def _parse_interval(self, interval: str) -> Optional[timedelta]:
        """Parse interval string (e.g., '1h', '30m', '1d') into timedelta"""
        try:
            value = int(interval[:-1])
            unit = interval[-1].lower()

            if unit == "m":
                return timedelta(minutes=value)
            elif unit == "h":
                return timedelta(hours=value)
            elif unit == "d":
                return timedelta(days=value)
            elif unit == "y":
                return timedelta(days=value * 365)
            else:
                logger.error(f"Invalid interval unit: {unit}")
                return None
        except (ValueError, IndexError):
            logger.error(f"Invalid interval format: {interval}")
            return None

    def _check_dependencies(self, task: Task) -> bool:
        """Check if all dependencies are completed"""
        if not task.dependencies:
            return True

        session = self.db.session
        for dep_name in task.dependencies:
            dep_task = session.query(Task).filter_by(name=dep_name).first()
            if not dep_task or not dep_task.last_run:
                return False
        return True

    def _execute_task(self, task: Task):
        """Execute a task if its dependencies are met"""
        if self.running_tasks.get(task.name, False):
            logger.warning(f"Task '{task.name}' is already running")
            return

        if not self._check_dependencies(task):
            logger.info(f"Task '{task.name}' dependencies not met, skipping")
            return

        self.running_tasks[task.name] = True
        try:
            executor = TaskExecutor(
                task_name=task.name,
                command=task.command,
                retry_max_attempts=task.retry_max_attempts,
                retry_delay=task.retry_delay,
            )

            success = executor.execute()

            # Update task status
            session = self.db.session
            task.last_run = datetime.utcnow()
            if success:
                task.next_run = self._calculate_next_run(task)
            session.commit()

        finally:
            self.running_tasks[task.name] = False

    def _calculate_next_run(self, task: Task) -> Optional[datetime]:
        """Calculate the next run time for a task"""
        if task.schedule_type == "one-time":
            return None

        if task.schedule_type == "recurring" and task.schedule_interval:
            interval = self._parse_interval(task.schedule_interval)
            if interval:
                return datetime.utcnow() + interval
        return None

    def schedule_task(self, task: Task):
        """Schedule a task for execution"""
        if task.name in self.scheduled_tasks:
            logger.warning(f"Task '{task.name}' is already scheduled")
            return

        if task.schedule_type == "one-time":
            if task.start_time and task.start_time > datetime.utcnow():
                job = (
                    schedule.every()
                    .day.at(task.start_time.strftime("%H:%M"))
                    .do(self._execute_task, task)
                )
                self.scheduled_tasks[task.name] = job
                logger.info(
                    f"Scheduled one-time task '{task.name}' for {task.start_time}"
                )
            else:
                logger.warning(f"One-time task '{task.name}' start time is in the past")
        else:
            interval = self._parse_interval(task.schedule_interval)
            if interval:
                job = schedule.every(interval.total_seconds()).seconds.do(
                    self._execute_task, task
                )
                self.scheduled_tasks[task.name] = job
                logger.info(
                    f"Scheduled recurring task '{task.name}' with interval {task.schedule_interval}"
                )

    def run(self):
        """Run the scheduler"""
        logger.info("Starting task scheduler")
        while True:
            schedule.run_pending()
            time.sleep(1)
