class ConnectorKind:
    CSV = 'csv'
    SQL_MYSQL = 'sql_mysql'
    SQL_POSTGRESQL = 'sql_postgresql'
    SQL_SQLITE = 'sql_sqlite'

    @staticmethod
    def is_valid(kind):
        return \
            kind == ConnectorKind.CSV or \
            ConnectorKind.is_valid_sql(kind=kind)

    @staticmethod
    def is_valid_sql(kind):
        return \
            kind == ConnectorKind.SQL_MYSQL or \
            kind == ConnectorKind.SQL_POSTGRESQL or \
            kind == ConnectorKind.SQL_SQLITE
