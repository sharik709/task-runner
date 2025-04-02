from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    command = Column(String, nullable=False)
    schedule_type = Column(String, nullable=False)  # 'one-time' or 'recurring'
    schedule_interval = Column(String)  # For recurring tasks (e.g., '1h', '1d')
    start_time = Column(DateTime)  # For one-time tasks
    retry_max_attempts = Column(Integer, default=3)
    retry_delay = Column(Integer, default=60)  # seconds
    dependencies = Column(JSON)  # List of task names this task depends on
    is_active = Column(Boolean, default=True)
    last_run = Column(DateTime)
    next_run = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Task(name='{self.name}', schedule_type='{self.schedule_type}')>"
