from dq0.sdk.data.metadata.connector.meta_connector_csv import MetaConnectorCSV
from dq0.sdk.data.metadata.connector.meta_connector_postgres import MetaConnectorPostgres


class MetaConnector:
    TYPE_NAME_CSV = 'csv'
    TYPE_NAME_POSTGRES = 'postgres'

    @staticmethod
    def isValidTypeName(type_name):
        if type_name is None:
            return False
        if type_name == MetaConnector.TYPE_NAME_CSV or type_name == MetaConnector.TYPE_NAME_POSTGRES:
            return True
        return False

    @staticmethod
    def verifyYamlDict(yaml_dict, expected_type_name=None):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if not MetaConnector.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if expected_type_name is not None and type_name != expected_type_name:
            raise Exception(f"type_name must be {expected_type_name} was {type_name}")
        return type_name

    @staticmethod
    def fromYamlDict(yaml_dict):
        type_name = MetaConnector.verifyYamlDict(yaml_dict)
        if type_name == MetaConnector.TYPE_NAME_CSV:
            return MetaConnectorCSV.fromYamlDict(yaml_dict)
        if type_name == MetaConnector.TYPE_NAME_POSTGRES:
            return MetaConnectorPostgres.fromYamlDict(yaml_dict)
        raise Exception(f"no factory configured for type_name {type_name}")

    def __init__(self, type_name):
        if not MetaConnector.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        self.type_name = type_name
