import os
import sys
from loguru import logger
from models.database import Database
from utils.config_loader import ConfigLoader
from scheduler.task_scheduler import TaskScheduler, Task

def setup_logging():
    """Setup logging configuration"""
    # Remove default logger
    logger.remove()

    # Add console logger
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )

    # Add file logger
    os.makedirs("logs", exist_ok=True)
    logger.add(
        "logs/task_runner.log",
        rotation="1 day",
        retention="7 days",
        level="DEBUG"
    )

def main():
    """Main entry point"""
    # Setup logging
    setup_logging()
    logger.info("Starting Task Runner")

    try:
        # Initialize database
        db = Database.get_instance()
        db.init_db()

        # Load and sync tasks from config
        config_loader = ConfigLoader()
        config_loader.sync_tasks()

        # Initialize and run scheduler
        scheduler = TaskScheduler()

        # Load tasks from database and schedule them
        session = db.session
        tasks = session.query(Task).filter_by(is_active=True).all()
        for task in tasks:
            scheduler.schedule_task(task)

        # Run the scheduler
        scheduler.run()

    except Exception as e:
        logger.exception(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
