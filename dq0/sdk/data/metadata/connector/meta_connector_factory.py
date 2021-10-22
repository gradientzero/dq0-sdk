from dq0.sdk.data.metadata.connector.meta_connector_csv import MetaConnectorCSV
from dq0.sdk.data.metadata.connector.meta_connector_postgres import MetaConnectorPostgres
from dq0.sdk.data.metadata.connector.meta_connector_type import MetaConnectorType


class MetaConnectorFactory:
    @staticmethod
    def verifyYamlDict(yaml_dict, expected_type_name=None):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if not MetaConnectorType.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if expected_type_name is not None and type_name != expected_type_name:
            raise Exception(f"type_name must be {expected_type_name} was {type_name}")

    @staticmethod
    def metaConnectorCSVFromYamlDict(yaml_dict):
        MetaConnectorFactory.verifyYamlDict(yaml_dict, MetaConnectorType.TYPE_NAME_CSV)
        uri = yaml_dict.pop('uri', None)
        use_original_header = bool(yaml_dict.pop('use_original_header', True))
        header_row = yaml_dict.pop('header_row', 0)
        header_columns = yaml_dict.pop('header_columns', None)
        sep = yaml_dict.pop('sep', ',')
        decimal = yaml_dict.pop('decimal', '.')
        na_values = yaml_dict.pop('na_values', None)
        index_col = yaml_dict.pop('index_col', None)
        skipinitialspace = bool(yaml_dict.pop('skipinitialspace', False))
        return MetaConnectorCSV(uri, use_original_header, header_row, header_columns, sep, decimal, na_values, index_col, skipinitialspace)

    @staticmethod
    def metaConnectorPostgresFromYamlDict(yaml_dict):
        MetaConnectorFactory.verifyYamlDict(yaml_dict, MetaConnectorType.TYPE_NAME_POSTGRES)
        return MetaConnectorPostgres()

    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaConnectorFactory.verifyYamlDict(yaml_dict)
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if type_name == MetaConnectorType.TYPE_NAME_CSV:
            return MetaConnectorFactory.metaConnectorCSVFromYamlDict(yaml_dict)
        if type_name == MetaConnectorType.TYPE_NAME_POSTGRES:
            return MetaConnectorFactory.metaConnectorPostgresFromYamlDict(yaml_dict)
        raise Exception(f"no factory configured for type_name {type_name}")
