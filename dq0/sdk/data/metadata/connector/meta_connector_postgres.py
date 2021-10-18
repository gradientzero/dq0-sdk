from dq0.sdk.data.metadata.connector.meta_connector import MetaConnector


class MetaConnectorPostgres(MetaConnector):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaConnector.verifyYamlDict(yaml_dict, MetaConnector.TYPE_NAME_POSTGRES)
        return MetaConnectorPostgres()

    def __init__(self):
        super().__init__(MetaConnector.TYPE_NAME_POSTGRES)

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
