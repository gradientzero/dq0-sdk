from dq0.sdk.data.metadata.connector.meta_connector_type import MetaConnectorType
from dq0.sdk.data.metadata.connector.meta_connector import MetaConnector


class MetaConnectorPostgres(MetaConnector):
    def __init__(self):
        super().__init__(MetaConnectorType.TYPE_NAME_POSTGRES)

    def copy(self):
        return super().copy()

    def to_dict(self):
        return super().to_dict()

    def merge_precheck_with(self, other):
        return super.merge_precheck_with(other)

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge connectors that fail the precheck")
        return self.copy()
