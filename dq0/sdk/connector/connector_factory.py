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
            return CSV.csv_from(meta_connector=meta_connector)
        if type_name == 'mysql':
            return MySQL.mysql_from(meta_database=meta_database)
        if type_name == 'postgresql':
            return PostgreSQL.postgresql_from(meta_database=meta_database)
        if type_name == 'sqlite':
            return SQLite.sqlite_from(meta_connector=meta_connector)
        raise ValueError(f"type_name={type_name} is unknown")
