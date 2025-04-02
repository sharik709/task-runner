"""
Example script for using TaskOps directly in Python code.
"""
from datetime import datetime
from task_processor import Task, Schedule, RetryConfig, TaskScheduler, LogManager, LogConfig

def main():
    # Initialize logging (optional but recommended)
    log_config = LogConfig(log_dir="./logs")
    log_manager = LogManager(log_config)

    # Create a task scheduler with logging
    scheduler = TaskScheduler(log_manager=log_manager)

    # Define a recurring task
    recurring_task = Task(
        name="data_processing",
        command="echo 'Processing data...'",
        schedule=Schedule(
            type="recurring",
            interval="1m"  # Run every minute (for testing)
        ),
        retry=RetryConfig(
            max_attempts=3,
            delay=5  # Retry after 5 seconds
        )
    )

    # Define a one-time task
    # Schedule it to run 10 seconds from now
    future_time = datetime.now().replace(microsecond=0)
    future_time = future_time.replace(second=future_time.second + 10)

    one_time_task = Task(
        name="cleanup_task",
        command="echo 'Cleaning up...'",
        schedule=Schedule(
            type="one-time",
            start_time=future_time
        ),
        retry=RetryConfig(
            max_attempts=2,
            delay=5  # Retry after 5 seconds
        )
    )

    # Add tasks to the scheduler
    scheduler.add_task(recurring_task)
    scheduler.add_task(one_time_task)

    # Start the scheduler (this will block and run until stopped)
    try:
        print("Task scheduler is running. Press Ctrl+C to stop.")
        scheduler.run()
    except KeyboardInterrupt:
        print("\nShutting down scheduler...")
        scheduler.stop()
        print("Scheduler stopped.")

if __name__ == "__main__":
    main()
