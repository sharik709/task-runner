import pytest
from pathlib import Path
from task_processor import Task, Schedule, RetryConfig, TaskScheduler, TaskExecutor, LogManager, LogConfig
import os
import time
from datetime import datetime, timedelta
from task_runner import ConfigLoader


@pytest.fixture
def temp_log_dir(tmp_path):
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    return log_dir


@pytest.fixture
def sample_task_config():
    return {
        "name": "test_task",
        "command": "echo 'test'",
        "schedule": {"type": "recurring", "interval": "1m"},
        "retry": {"max_attempts": 3, "delay": 1},
    }


def test_task_creation(sample_task_config):
    task = Task(**sample_task_config)
    assert task.name == "test_task"
    assert task.command == "echo 'test'"
    assert task.schedule.type == "recurring"
    assert task.schedule.interval == "1m"


def test_log_manager(temp_log_dir):
    config = LogConfig(log_dir=str(temp_log_dir))
    log_manager = LogManager(config)
    logger = log_manager.get_logger("test_task")

    # Test log file creation
    logger.log_start()
    assert len(list(temp_log_dir.glob("test_task/*.log"))) > 0

    # Test log rotation
    logger.cleanup_old_logs()
    assert len(list(temp_log_dir.glob("test_task/*.log"))) <= config.max_files


def test_scheduler(sample_task_config):
    log_manager = LogManager(LogConfig())
    scheduler = TaskScheduler(log_manager)
    task = Task(**sample_task_config)

    # Test task scheduling
    scheduler.schedule_task(task)
    assert task.name in scheduler.scheduled_tasks

    # Test task execution through run_task
    scheduler._run_task(task)
    assert task.last_run is not None
    assert task.last_status == "success"


def test_config_loader(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir()

    # Create test config file
    config_file = config_dir / "tasks.yaml"
    config_file.write_text(
        """
    tasks:
      - name: "test_task"
        command: "echo 'test'"
        schedule:
          type: "recurring"
          interval: "1m"
        retry:
          max_attempts: 3
          delay: 1
    """
    )

    loader = ConfigLoader(config_dir=str(config_dir))
    tasks = loader.load_configs()
    assert len(tasks) == 1
    assert tasks[0].name == "test_task"


def test_retry_mechanism(sample_task_config):
    task = Task(**sample_task_config)

    # Simulate task failure
    task.last_run = datetime.now()
    task.last_status = "failed"
    task.attempts = 1

    assert task.should_retry()
    assert task.retry_delay == 1  # seconds

    # Test max attempts
    task.attempts = 3
    assert not task.should_retry()


def test_schedule_types():
    # Test recurring schedule
    recurring_task = Task(
        name="recurring",
        command="echo 'test'",
        schedule={"type": "recurring", "interval": "1h"},
        retry={"max_attempts": 3, "delay": 1},
    )
    assert recurring_task.schedule.type == "recurring"
    assert recurring_task.schedule.interval == "1h"

    # Test one-time schedule
    one_time_task = Task(
        name="one_time",
        command="echo 'test'",
        schedule={"type": "one-time", "start_time": datetime.now().isoformat()},
        retry={"max_attempts": 3, "delay": 1},
    )
    assert one_time_task.schedule.type == "one-time"
    assert isinstance(one_time_task.schedule.start_time, datetime)
