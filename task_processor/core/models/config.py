from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ScheduleConfig(BaseModel):
    type: str = Field(..., description="Type of schedule: 'one-time' or 'recurring'")
    interval: Optional[str] = Field(
        None, description="Interval for recurring tasks (e.g., '1h', '1d')"
    )
    start_time: Optional[datetime] = Field(None, description="Start time for one-time tasks")


class RetryConfig(BaseModel):
    max_attempts: int = Field(default=3, description="Maximum number of retry attempts")
    delay: int = Field(default=60, description="Delay between retries in seconds")


class TaskConfig(BaseModel):
    name: str = Field(..., description="Unique name for the task")
    command: str = Field(..., description="Command or script to execute")
    schedule: ScheduleConfig
    retry: RetryConfig = Field(default_factory=RetryConfig)
    dependencies: List[str] = Field(
        default_factory=list, description="List of task names this task depends on"
    )
    log_level: str = Field(default="INFO", description="Logging level for the task")


class Config(BaseModel):
    tasks: List[TaskConfig]
