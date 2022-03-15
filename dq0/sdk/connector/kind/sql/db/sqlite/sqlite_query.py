from dq0.sdk.connector.connector_kind import ConnectorKind
from dq0.sdk.connector.kind.sql.query import Query

import pandas


class SQLiteQuery(Query):
    def __init__(self, connector, query_string):
        super().__init__(connector, query_string)
        if not connector.get_kind() == ConnectorKind.SQL_SQLITE:
            raise ValueError(f"connector with kind={connector.get_kind()} is not of valid {ConnectorKind.SQL_SQLITE} kind")

    def to_pandas(self):
        engine = self.get_connector().get_engine()
        if engine is None:
            raise ValueError("engine is None")
        connection = engine.raw_connection()
        df = pandas.read_sql_query(sql=self.get_query_string(), con=connection)
        connection.close()
        return df
