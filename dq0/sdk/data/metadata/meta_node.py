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
    def verifyYamlDict(yaml_dict, expected_type_name=None):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if not MetaNode.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if expected_type_name is not None and type_name != expected_type_name:
            raise Exception(f"type_name must be {expected_type_name} was {type_name}")
        return type_name

    @staticmethod
    def fromYamlDict(yaml_dict):
        type_name = MetaNode.verifyYamlDict(yaml_dict)
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

    @staticmethod
    def merge_many(lst_a, lst_b):
        if lst_a is None:
            return lst_b
        if lst_b is None:
            return lst_a
        merged = []
        for elem_a in lst_a:
            elem_merged = elem_a.copy()
            for elem_b in lst_b:
                if elem_a.merge_precheck_with(elem_b):
                    lst_b.remove(elem_b)
                    elem_merged = elem_a.merge_with(elem_b)
                    break
            merged.append(elem_merged)
        for elem_b in lst_b:
            for elem_a in lst_a:
                if elem_b.merge_precheck_with(elem_a):
                    raise Exception("this can never happen")
            merged.append(elem_b.copy())
        return merged

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

    def copy(self):
        return MetaNode(self.type_name, self.name, self.description, self.is_public, self.connector.copy(), [section.copy() for section in self.sections], [child_node.copy() for child_node in self.child_nodes])

    def to_dict(self):
        return {
            "type_name": self.type_name,
            "name": self.name,
            "description": self.description,
            "is_public": self.is_public,
            "connector": self.connector,
            "sections": [section.to_dict() for section in self.sections],
            "child_nodes": [child_node.to_dict() for child_node in self.child_nodes],
        }

    def merge_precheck_with(self, other):
        if other is None or self.type_name != other.type_name or self.name != other.name:
            return False
        if self.description != other.description:
            raise Exception(f"nodes with same type_name {self.type_name} and name {self.name if self.name is not None else 'None'} cannot have diverging descriptions {self.description if self.description is not None else 'None'} <--> {other.description if other.description is not None else 'None'}")
        if self.is_public != other.is_public:
            raise Exception(f"nodes with same type_name {self.type_name} and name {self.name if self.name is not None else 'None'} cannot have diverging is_public flags {self.is_public} <--> {other.is_public}")
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge nodes that fail the precheck")
        merged = self.copy()
        merged.connector = self.connector.merge_with(other.connector)
        merged.sections = MetaSection.merge_many(self.sections, other.sections)
        merged.child_nodes = MetaNode.merge_many(self.child_nodes, other.child_nodes)
        return merged
