from dq0.sdk.connector.connector_kind import ConnectorKind


class Query:
    def __init__(self, connector, query_string):
        if not ConnectorKind.is_valid_sql(kind=connector.get_kind()):
            raise ValueError(f"connector with kind={connector.get_kind()} is not of valid sql kind")
        self._connector = connector
        self._query_string = query_string

    def get_connector(self):
        return self._connector

    def get_query_string(self):
        return self._query_string

    def to_pandas(self):
        raise NotImplementedError
