import yaml
import os
from typing import List
from datetime import datetime
from models.config import Config, TaskConfig
from models.task import Task
from models.database import Database

class ConfigLoader:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.db = Database.get_instance()

    def load_configs(self) -> List[Task]:
        """Load all task configurations from YAML files in the config directory"""
        tasks = []

        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)

        # Load all YAML files in the config directory
        for filename in os.listdir(self.config_dir):
            if filename.endswith(('.yaml', '.yml')):
                file_path = os.path.join(self.config_dir, filename)
                try:
                    with open(file_path, 'r') as f:
                        config_data = yaml.safe_load(f)
                        config = Config(**config_data)

                        # Convert config to Task objects
                        for task_config in config.tasks:
                            task = self._create_task(task_config)
                            if task:
                                tasks.append(task)
                except Exception as e:
                    print(f"Error loading config file {filename}: {str(e)}")

        return tasks

    def _create_task(self, task_config: TaskConfig) -> Task:
        """Convert TaskConfig to Task model"""
        try:
            task = Task(
                name=task_config.name,
                command=task_config.command,
                schedule_type=task_config.schedule.type,
                schedule_interval=task_config.schedule.interval,
                start_time=task_config.schedule.start_time,
                retry_max_attempts=task_config.retry.max_attempts,
                retry_delay=task_config.retry.delay,
                dependencies=task_config.dependencies
            )
            return task
        except Exception as e:
            print(f"Error creating task from config: {str(e)}")
            return None

    def sync_tasks(self):
        """Sync tasks from config files to database"""
        session = self.db.session

        # Load tasks from config
        config_tasks = self.load_configs()

        # Get existing tasks from database
        existing_tasks = {task.name: task for task in session.query(Task).all()}

        # Update or create tasks
        for task in config_tasks:
            if task.name in existing_tasks:
                # Update existing task
                existing_task = existing_tasks[task.name]
                # Update only the fields that should be updated from config
                existing_task.command = task.command
                existing_task.schedule_type = task.schedule_type
                existing_task.schedule_interval = task.schedule_interval
                existing_task.start_time = task.start_time
                existing_task.retry_max_attempts = task.retry_max_attempts
                existing_task.retry_delay = task.retry_delay
                existing_task.dependencies = task.dependencies
                existing_task.is_active = True
                # Don't update last_run, next_run, created_at, or updated_at
            else:
                # Create new task
                session.add(task)

        # Remove tasks that no longer exist in config
        config_task_names = {task.name for task in config_tasks}
        for task_name, task in existing_tasks.items():
            if task_name not in config_task_names:
                session.delete(task)

        session.commit()
