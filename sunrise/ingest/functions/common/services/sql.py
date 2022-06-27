import logging
import pyodbc
import time

from typing import Any


class SqlServerClient:
    _RETRY_NUMBER = 3
    _CONNECTION_TIMEOUT = 30
    _TIME_SLEEP = 20

    def __init__(self, host: str, db: str, user: str, pw: str):
        self._host = host
        self._db = db
        self._user = user
        self._pass = pw
        self.log = logging.getLogger(self.__class__.__name__)
        self._connection = self.connect()

    @property
    def connection_string(self) -> str:
        return (
            "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
            + self._host
            + ";DATABASE="
            + self._db
            + ";UID="
            + self._user
            + ";PWD="
            + self._pass
        )

    @property
    def connection(self) -> pyodbc.Connection:
        return self._connection

    def connect(self) -> pyodbc.Connection:
        retry_count = 1
        retry_flag = True
        while retry_flag and retry_count <= self._RETRY_NUMBER:
            try:
                self.log.info(f"Try {retry_count} to connect")
                conn = pyodbc.connect(
                    self.connection_string,
                    autocommit=True,
                    timeout=self._CONNECTION_TIMEOUT,
                )
                self.log.info("Connected!")
                with conn.cursor() as cursor:
                    cursor.execute("SELECT @@version;")
                    row = cursor.fetchone()
                    while row:
                        self.log.debug(row[0])
                        row = cursor.fetchone()
                return conn
            except Exception as e:
                self.log.error(f"Failed: {e}")
                self.log.info(f"Retry after {self._TIME_SLEEP} seconds...")
                retry_count += 1
                time.sleep(self._TIME_SLEEP)

    def execute_sql(self, sql_statement: str, wake_up: bool = False) -> Any:
        retry_count = 1
        retry_flag = True
        while retry_flag and retry_count <= self._RETRY_NUMBER:
            try:
                logging.info(f"Try number {retry_count}")
                conn = pyodbc.connect(
                    self.connection_string,
                    autocommit=True,
                    timeout=self._CONNECTION_TIMEOUT,
                )
                with conn.cursor() as cursor:
                    if wake_up:
                        cursor.execute("SELECT @@version;")
                        row = cursor.fetchone()
                        while row:
                            logging.info(row[0])
                            row = cursor.fetchone()
                        return None
                    logging.info("Executing sql...")
                    res = cursor.execute(sql_statement)
                    retry_flag = False
                    logging.info("Success!")
                    return res
            except Exception as e:
                logging.error(f"Failed: {e}")
                logging.info(f"Retry after {self._TIME_SLEEP} seconds...")
                retry_count += 1
                time.sleep(self._TIME_SLEEP)
