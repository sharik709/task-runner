import os
from pathlib import Path
from typing import List

from task_processor.core.models import Task
import yaml


class ConfigLoader:
    """Load task configurations from YAML files."""

    def __init__(self, config_dir: str):
        """Initialize the config loader."""
        self.config_dir = Path(config_dir)

    def load_configs(self) -> List[Task]:
        """Load all task configurations from YAML files in the config directory."""
        tasks = []
        if not self.config_dir.exists():
            raise FileNotFoundError(f"Config directory not found: {self.config_dir}")

        for config_file in self.config_dir.glob("*.yaml"):
            with open(config_file, "r") as f:
                config_data = yaml.safe_load(f)
                if config_data and "tasks" in config_data:
                    for task_data in config_data["tasks"]:
                        tasks.append(Task(**task_data))

        return tasks
