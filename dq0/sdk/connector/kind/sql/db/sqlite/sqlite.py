from pathlib import Path

from dq0.sdk.connector.connector_kind import ConnectorKind
from dq0.sdk.connector.kind.sql.db.sqlite.sqlite_query import SQLiteQuery
from dq0.sdk.connector.kind.sql.sql import SQL

import sqlalchemy


class SQLite(SQL):
    @staticmethod
    def connection_uri(filepath):
        absolute_path = filepath.resolve()
        return f"sqlite:///{absolute_path}"

    def __init__(self, filepath):
        super().__init__(ConnectorKind.SQL_SQLITE)
        self._filepath = Path(filepath)
        if not self._filepath.is_file():
            raise ValueError(f"filepath={filepath} is not a file")
        self._connection_uri = SQLite.connection_uri(filepath=self._filepath)
        self._engine = sqlalchemy.create_engine(self.get_connection_uri())

    def get_filepath(self):
        return self._filepath

    def get_connection_uri(self):
        return self._connection_uri

    def get_engine(self):
        return self._engine

    def new_query(self, query_string):
        return SQLiteQuery(connector=self, query_string=query_string)
