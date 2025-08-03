import datetime as dt
import decimal
import logging
from contextlib import contextmanager
from typing import Optional, Any

import psycopg2
import psycopg2.extras
import pytz

from database.drivers.driver import DatabaseDriver
from database.exceptions import DatabaseException
from database.drivers.postgres_credentials import PostgresCredentials

logger = logging.getLogger(__name__)



from pydantic import BaseSettings, Field
class PostgresCredentials(BaseSettings):
    host: str = Field(..., env="POSTGRES_HOST")
    port: int = Field(..., env="POSTGRES_PORT")
    username: str = Field(..., env="POSTGRES_USERNAME")
    password: str = Field(..., env="POSTGRES_PASSWORD")
    database: str = Field(..., env="POSTGRES_DATABASE")

    class Config:
        env_file = ".env"
        case_sensitive = False



class PostgresDriver(DatabaseDriver):
    def __init__(self, credentials: Optional[PostgresCredentials] = None):
        self.credentials = credentials or PostgresCredentials()
        self.connection = self.connect()

    def connect(self):
        try:
            return psycopg2.connect(
                host=self.credentials.host,
                port=self.credentials.port,
                database=self.credentials.database,
                user=self.credentials.username,
                password=self
            )
        except Exception as e:
            raise DatabaseException(f"Unable to connect to database: {e}") from e

    def close(self):
        if self.connection:
            self.connection.close()

    def execute(self, query, data, resp: bool = True, cursor=None, connection=None):
        conn = connection or self.connection
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            logger.info("Executing SQL:\n%s", query.as_string(conn))
            logger.info("With data:\n%s", data)
            cur.execute(query, data)

            results = self.cursor_row_as_dict(cur) if resp else None

            if not connection:
                conn.commit()

            logger.debug("SQL Response: %s", results)
            return results

        except psycopg2.ProgrammingError as e:
            logger.exception("SQL execution failed")
            raise DatabaseException(str(e)) from e

        finally:
            if not connection:
                self.close()

    def cursor_row_as_dict(self, cursor):
        column_names = [desc[0] for desc in cursor.description]
        return [
            {k: self._to_str(v) if isinstance(v, (dt.datetime, str, decimal.Decimal)) else v
             for k, v in zip(column_names, row)}
            for row in cursor
        ]

    def _to_str(self, value: Any) -> Any:
        if isinstance(value, dt.datetime):
            return value.replace(tzinfo=pytz.UTC).isoformat()
        if isinstance(value, decimal.Decimal):
            return float(value)
        return str(value).strip()


@contextmanager
def postgres_connection(credentials: Optional[PostgresCredentials] = None):
    driver = PostgresDriver(credentials)
    try:
        yield driver.connection
        driver.connection.commit()
    finally:
        driver.close()
