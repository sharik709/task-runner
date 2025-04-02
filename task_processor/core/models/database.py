import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


class Database:
    _instance = None
    _engine = None
    _Session = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._engine is not None:
            return

        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)

        # Create SQLite database
        db_path = "data/tasks.db"
        self._engine = create_engine(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self._Session = sessionmaker(bind=self._engine)

    @property
    def session(self):
        return self._Session()

    def init_db(self):
        """Initialize the database, creating all tables."""
        from .task import Base

        Base.metadata.create_all(self._engine)
