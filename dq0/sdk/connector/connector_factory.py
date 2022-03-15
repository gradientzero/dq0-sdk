from dq0.sdk.connector.kind.csv.csv import CSV
from dq0.sdk.connector.kind.sql.db.mysql.mysql import MySQL
from dq0.sdk.connector.kind.sql.db.postgresql.postgresql import PostgreSQL
from dq0.sdk.connector.kind.sql.db.sqlite.sqlite import SQLite


class ConnectorFactory:
    @staticmethod
    def connector_from(meta_database):
        meta_connector = meta_database.connector
        type_name = meta_connector.type_name
        if type_name == 'csv':
            return ConnectorFactory.csv_from(meta_connector=meta_connector)
        if type_name == 'mysql':
            return ConnectorFactory.mysql_from(meta_database=meta_database)
        if type_name == 'postgresql':
            return ConnectorFactory.postgresql_from(meta_database=meta_database)
        if type_name == 'sqlite':
            return ConnectorFactory.sqlite_from(meta_connector=meta_connector)
        raise ValueError(f"type_name={type_name} is unknown")

    @staticmethod
    def csv_from(meta_connector):
        if meta_connector.type_name != 'csv':
            raise ValueError(f"type_name={meta_connector.type_name} != csv")
        filepath = meta_connector.uri
        if len(filepath) == 0:
            raise ValueError("uri not specified")
        sep = meta_connector.sep if meta_connector.sep is not None else ','
        header = meta_connector.header_row if meta_connector.header_row is not None else 'infer'
        names = meta_connector.header_columns
        index_col = meta_connector.index_col
        skipinitialspace = meta_connector.skipinitialspace \
            if meta_connector.skipinitialspace is not None else False
        na_values = meta_connector.na_values
        decimal = meta_connector.decimal if meta_connector.decimal is not None else '.'
        return CSV(filepath=filepath, sep=sep, header=header, names=names, index_col=index_col,
                   skipinitialspace=skipinitialspace, na_values=na_values, decimal=decimal)

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
    def postgresql_from(meta_database):
        meta_connector = meta_database.connector
        if meta_connector.type_name != 'postgresql':
            raise ValueError(f"type_name={meta_connector.type_name} != postgresql")
        username = meta_connector.username if meta_connector.username is not None else ''
        password = meta_connector.password if meta_connector.password is not None else ''
        host = meta_connector.host if meta_connector.host is not None else ''
        port = meta_connector.port if meta_connector.port is not None else ''
        database = meta_database.data.name if meta_database.data.name is not None else ''
        return PostgreSQL(username=username, password=password, host=host, port=port, database=database)

    @staticmethod
    def sqlite_from(meta_connector):
        if meta_connector.type_name != 'sqlite':
            raise ValueError(f"type_name={meta_connector.type_name} != sqlite")
        uri = meta_connector.uri if meta_connector.uri is not None else ''
        return SQLite(filepath=uri)
