from dq0.sdk.connector.connector_kind import ConnectorKind
from dq0.sdk.connector.kind.sql.db.mysql.mysql_query import MySQLQuery
from dq0.sdk.connector.kind.sql.sql import SQL

import sqlalchemy


class MySQL(SQL):
    @staticmethod
    def connection_uri(username='', password='', host='', port='', database='', charset=''):
        if len(username) == 0:
            password = ''
        if len(host) == 0:
            raise Exception("host not provided")
        password_sep = ':' if 0 < len(password) else ''
        user_sep = '@' if 0 < len(username) else ''
        port_sep = ':' if 0 < len(port) else ''
        database_sep = '/' if 0 < len(database) else ''
        charset_sep = '?charset=' if 0 < len(charset) else ''
        return f"mysql+mysqlconnector://{username}{password_sep}{password}{user_sep}{host}{port_sep}{port}{database_sep}{database}{charset_sep}{charset}"

    def __init__(self, username='', password='', host='', port='', database='', charset=''):
        super().__init__(ConnectorKind.SQL_MYSQL)
        self._connection_uri = MySQL.connection_uri(username=username, password=password, host=host, port=port, database=database, charset=charset)
        self._engine = sqlalchemy.create_engine(self.get_connection_uri())

    def get_connection_uri(self):
        return self._connection_uri

    def get_engine(self):
        return self._engine

    def new_query(self, query_string):
        return MySQLQuery(connector=self, query_string=query_string)
