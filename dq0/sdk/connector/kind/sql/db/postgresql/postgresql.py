from dq0.sdk.connector.connector_kind import ConnectorKind
from dq0.sdk.connector.kind.sql.db.postgresql.postgresql_query import PostgreSQLQuery
from dq0.sdk.connector.kind.sql.sql import SQL

import sqlalchemy


class PostgreSQL(SQL):
    @staticmethod
    def connection_uri(username='', password='', host='', port='', database=''):
        if len(username) == 0:
            password = ''
        if len(host) == 0:
            raise Exception("host not provided")
        password_sep = ':' if 0 < len(password) else ''
        user_sep = '@' if 0 < len(username) else ''
        port_sep = ':' if 0 < len(port) else ''
        database_sep = '/' if 0 < len(database) else ''
        return f"postgresql+psycopg2://{username}{password_sep}{password}{user_sep}{host}{port_sep}{port}{database_sep}{database}"

    def __init__(self, username='', password='', host='', port='', database=''):
        super().__init__(ConnectorKind.SQL_POSTGRESQL)
        self._connection_uri = PostgreSQL.connection_uri(username=username, password=password, host=host, port=port, database=database)
        self._engine = sqlalchemy.create_engine(self.get_connection_uri())

    def get_connection_uri(self):
        return self._connection_uri

    def get_engine(self):
        return self._engine

    def new_query(self, query_string):
        return PostgreSQLQuery(connector=self, query_string=query_string)
