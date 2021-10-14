from dq0.sdk.data.metadata.connector.meta_connector import MetaConnector
from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaNode:
    TYPE_NAME_DATASET = 'dataset'
    TYPE_NAME_DATABASE = 'database'
    TYPE_NAME_SCHEMA = 'schema'
    TYPE_NAME_TABLE = 'table'
    TYPE_NAME_COLUMN = 'column'

    @staticmethod
    def isValidTypeName(type_name):
        if type_name is None:
            return False
        if type_name == MetaNode.TYPE_NAME_DATASET or type_name == MetaNode.TYPE_NAME_DATABASE or type_name == MetaNode.TYPE_NAME_SCHEMA or type_name == MetaNode.TYPE_NAME_TABLE or type_name == MetaNode.TYPE_NAME_COLUMN:
            return True
        return False

    @staticmethod
    def fromYamlDict(yaml_dict):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict.pop('type_name', None)
        name = yaml_dict.pop('name', None)
        description = yaml_dict.pop('description', None)
        is_public = bool(yaml_dict.pop('is_public', False))
        connector_yaml_dict = yaml_dict.pop('connector', None)
        connector = MetaConnector.fromYamlDict(connector_yaml_dict) if connector_yaml_dict is not None else None
        sections_yaml_list = yaml_dict.pop('sections', None)
        sections = MetaSection.fromYamlList(sections_yaml_list) if sections_yaml_list is not None else None
        child_nodes_yaml_list = yaml_dict.pop('child_nodes', None)
        child_nodes = MetaNode.fromYamlList(child_nodes_yaml_list) if child_nodes_yaml_list is not None else None
        return MetaNode(type_name, name, description, is_public, connector, sections, child_nodes)

    @staticmethod
    def fromYamlList(yaml_list):
        if yaml_list is None:
            raise Exception("yaml_list is None")
        if not isinstance(yaml_list, list):
            raise Exception("yaml_list is not a list instance")
        nodes = []
        for yaml_dict in yaml_list:
            nodes.append(MetaNode.fromYamlDict(yaml_dict))
        return nodes    

    def __init__(self, type_name, name=None, description=None, is_public=False, connector=None, sections=None, child_nodes=None):
        if not MetaNode.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        self.type_name = type_name
        self.name = name
        self.description = description
        self.is_public = is_public
        self.connector = connector
        self.sections = sections
        self.child_nodes = child_nodes
