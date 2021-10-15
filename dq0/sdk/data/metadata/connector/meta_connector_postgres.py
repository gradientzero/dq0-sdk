from dq0.sdk.data.metadata.connector.meta_connector import MetaConnector


class MetaConnectorPostgres(MetaConnector):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaConnector.verifyYamlDict(yaml_dict, MetaConnector.TYPE_NAME_POSTGRES)
        return MetaConnectorPostgres()

    def __init__(self):
        super().__init__(MetaConnector.TYPE_NAME_POSTGRES)
