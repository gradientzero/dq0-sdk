from dq0.sdk.connector.connector_kind import ConnectorKind
from dq0.sdk.connector.kind.sql.db.mysql.mysql_query import MySQLQuery
from dq0.sdk.connector.kind.sql.sql import SQL

import sqlalchemy


class MySQL(SQL):
    @staticmethod
    def mysql_from(meta_database):
        meta_connector = meta_database.connector
        if meta_connector.type_name != 'mysql':
            raise ValueError(f"type_name={meta_connector.type_name} != mysql")
        username = meta_connector.username if meta_connector.username is not None else ''
        password = meta_connector.password if meta_connector.password is not None else ''
        host = meta_connector.host if meta_connector.host is not None else ''
        port = meta_connector.port if meta_connector.port is not None else ''
        database = meta_database.data.name if meta_database.data.name is not None else ''
        charset = meta_connector.charset if meta_connector.charset is not None else ''
        return MySQL(username=username, password=password, host=host, port=port, database=database, charset=charset)

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
