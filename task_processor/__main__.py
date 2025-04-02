import argparse
import sys
from pathlib import Path
from task_processor import TaskScheduler, ConfigLoader, LogManager, LogConfig


def main():
    parser = argparse.ArgumentParser(description="Task Processor - A flexible task processing system")
    parser.add_argument(
        "--config-dir",
        type=str,
        default="config",
        help="Directory containing task configuration files",
    )
    parser.add_argument(
        "--log-dir",
        type=str,
        default="~/.task_processor/logs",
        help="Directory for log files",
    )
    parser.add_argument(
        "--max-log-files",
        type=int,
        default=10,
        help="Maximum number of log files to keep per task",
    )

    args = parser.parse_args()

    try:
        # Initialize components
        log_config = LogConfig(log_dir=args.log_dir)
        log_manager = LogManager(log_config)
        config_loader = ConfigLoader(config_dir=args.config_dir)
        scheduler = TaskScheduler(log_manager)

        # Load and schedule tasks
        tasks = config_loader.load_configs()
        for task in tasks:
            scheduler.add_task(task)

        print(f"Loaded {len(tasks)} tasks from {args.config_dir}")
        print("Task Processor is running. Press Ctrl+C to stop.")

        # Run the scheduler
        scheduler.run()

    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        scheduler.stop()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
