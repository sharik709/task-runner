import os
from pathlib import Path
from typing import List
import yaml
from task_runner.core.models import Task

class ConfigLoader:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)

    def load_configs(self) -> List[Task]:
        if not self.config_dir.exists():
            raise FileNotFoundError(f"Config directory not found: {self.config_dir}")

        tasks = []
        for config_file in self.config_dir.glob("*.yaml"):
            try:
                with open(config_file, "r") as f:
                    config = yaml.safe_load(f)
                    if "tasks" in config:
                        for task_config in config["tasks"]:
                            tasks.append(Task(**task_config))
            except Exception as e:
                raise ValueError(f"Error loading config file {config_file}: {str(e)}")

        return tasks
