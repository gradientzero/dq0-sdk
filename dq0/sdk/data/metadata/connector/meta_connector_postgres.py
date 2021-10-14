from dq0.sdk.data.metadata.connector.meta_connector import MetaConnector


class MetaConnectorPostgres(MetaConnector):
    @staticmethod
    def fromYamlDict(yaml_dict):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if not MetaConnector.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if type_name != MetaConnector.TYPE_NAME_POSTGRES:
            raise Exception(f"type_name must be {MetaConnector.TYPE_NAME_POSTGRES} was {type_name}")
        return MetaConnectorPostgres()

    def __init__(self):
        super().__init__(MetaConnector.TYPE_NAME_POSTGRES)
