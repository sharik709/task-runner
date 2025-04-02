from typing import Any, Dict, List, Optional
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel, Field
from ..base import BasePlugin, PluginConfig


class MySQLConfig(PluginConfig):
    """MySQL plugin configuration"""

    host: str = Field(..., description="MySQL host")
    port: int = Field(3306, description="MySQL port")
    user: str = Field(..., description="MySQL user")
    password: str = Field(..., description="MySQL password")
    database: str = Field(..., description="MySQL database name")
    pool_size: int = Field(5, description="Connection pool size")
    pool_name: str = Field("task_runner_pool", description="Connection pool name")


class MySQLPlugin(BasePlugin):
    """MySQL plugin for database operations"""

    def __init__(self, config: MySQLConfig):
        super().__init__(config)
        self._connection = None
        self._pool = None

    def initialize(self) -> None:
        """Initialize MySQL connection pool"""
        try:
            self._pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name=self.config.pool_name,
                pool_size=self.config.pool_size,
                host=self.config.host,
                port=self.config.port,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database,
            )
            self._initialized = True
        except Error as e:
            raise RuntimeError(f"Failed to initialize MySQL connection pool: {e}")

    def cleanup(self) -> None:
        """Cleanup MySQL connections"""
        if self._pool:
            self._pool._remove_connections()
            self._pool = None
        self._initialized = False

    def get_connection(self):
        """Get a connection from the pool"""
        if not self._initialized:
            raise RuntimeError("MySQL plugin not initialized")
        return self._pool.get_connection()

    def execute_query(
        self, query: str, params: Optional[List[Any]] = None
    ) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results"""
        with self.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall()

    def execute_command(self, query: str, params: Optional[List[Any]] = None) -> int:
        """Execute an INSERT/UPDATE/DELETE query and return affected rows"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                conn.commit()
                return cursor.rowcount

    def execute_many(self, query: str, params: List[List[Any]]) -> int:
        """Execute multiple commands in a single transaction"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(query, params)
                conn.commit()
                return cursor.rowcount
