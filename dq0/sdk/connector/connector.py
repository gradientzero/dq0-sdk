from dq0.sdk.connector.connector_kind import ConnectorKind


class Connector:
    def __init__(self, kind):
        if not ConnectorKind.is_valid(kind=kind):
            raise ValueError(f"kind {kind} is not valid")
        self._kind = kind

    def get_kind(self):
        return self._kind

    def to_pandas(self):
        raise NotImplementedError

    def new_query(self, query_string):
        raise NotImplementedError
