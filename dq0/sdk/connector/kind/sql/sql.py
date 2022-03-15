from dq0.sdk.connector.connector import Connector
from dq0.sdk.connector.connector_kind import ConnectorKind


class SQL(Connector):
    def __init__(self, kind):
        super().__init__(kind=kind)
        if not ConnectorKind.is_valid_sql(kind=kind):
            raise ValueError(f"kind={kind} is not a valid sql kind")

    def new_query(self, query_string):
        raise NotImplementedError
