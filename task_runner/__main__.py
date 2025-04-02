import argparse
import sys
from pathlib import Path
from task_runner import TaskScheduler, ConfigLoader, LogManager, LogConfig


def main():
    parser = argparse.ArgumentParser(
        description="Task Runner - A powerful yet simple task scheduler"
    )
    parser.add_argument(
        "--config-dir",
        default="config",
        help="Directory containing task configuration files (default: config)",
    )
    parser.add_argument(
        "--log-dir", help="Directory for log files (default: ~/.task_runner/logs)"
    )
    parser.add_argument(
        "--max-log-files",
        type=int,
        default=10,
        help="Maximum number of log files to keep per task (default: 10)",
    )

    args = parser.parse_args()

    try:
        # Initialize components
        log_config = LogConfig(log_dir=args.log_dir, max_files=args.max_log_files)
        log_manager = LogManager(log_config)
        config_loader = ConfigLoader(args.config_dir)
        scheduler = TaskScheduler(log_manager)

        # Load and schedule tasks
        tasks = config_loader.load_configs()
        for task in tasks:
            scheduler.schedule_task(task)

        print(f"Loaded {len(tasks)} tasks from {args.config_dir}")
        print("Task Runner is running. Press Ctrl+C to stop.")

        # Run the scheduler
        scheduler.run()

    except KeyboardInterrupt:
        print("\nShutting down Task Runner...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
