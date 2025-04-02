from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class Schedule(BaseModel):
    type: str = Field(..., description="Schedule type: 'recurring' or 'one-time'")
    interval: Optional[str] = Field(
        None, description="Interval for recurring tasks (e.g., '1m', '1h', '1d', '1y')"
    )
    start_time: Optional[datetime] = Field(
        None, description="Start time for one-time tasks"
    )

    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        if v not in ["recurring", "one-time"]:
            raise ValueError("Schedule type must be 'recurring' or 'one-time'")
        return v

    @field_validator("interval")
    @classmethod
    def validate_interval(cls, v, info):
        if info.data.get("type") == "recurring" and not v:
            raise ValueError("Interval is required for recurring tasks")
        if v and not v.endswith(("m", "h", "d", "y")):
            raise ValueError(
                "Interval must end with m (minutes), h (hours), d (days), or y (years)"
            )
        return v

    @field_validator("start_time")
    @classmethod
    def validate_start_time(cls, v, info):
        if info.data.get("type") == "one-time" and not v:
            raise ValueError("Start time is required for one-time tasks")
        return v


class RetryConfig(BaseModel):
    max_attempts: int = Field(..., ge=1, description="Maximum number of retry attempts")
    delay: int = Field(..., ge=1, description="Delay between retries in seconds")


class Task(BaseModel):
    name: str = Field(..., description="Unique name for the task")
    command: str = Field(..., description="Command to execute")
    schedule: Schedule
    retry: RetryConfig
    dependencies: List[str] = Field(
        default_factory=list,
        description="Names of tasks that must complete before this task",
    )
    last_run: Optional[datetime] = None
    last_status: Optional[str] = None
    attempts: int = 0

    def should_retry(self) -> bool:
        if not self.last_status == "failed":
            return False
        return self.attempts < self.retry.max_attempts

    @property
    def retry_delay(self) -> int:
        return self.retry.delay
