from dq0.sdk.data.metadata.connector.meta_connector_factory import MetaConnectorFactory
from dq0.sdk.data.metadata.meta_node_type import MetaNodeType
from dq0.sdk.data.metadata.section.meta_section_factory import MetaSectionFactory
from dq0.sdk.data.metadata.meta_node import MetaNode


class MetaNodeFactory:
    @staticmethod
    def verifyYamlDict(yaml_dict, expected_type_name=None):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if not MetaNodeType.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if expected_type_name is not None and type_name != expected_type_name:
            raise Exception(f"type_name must be {expected_type_name} was {type_name}")

    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaNodeFactory.verifyYamlDict(yaml_dict)
        type_name = yaml_dict.pop('type_name', None)
        name = yaml_dict.pop('name', None)
        description = yaml_dict.pop('description', None)
        is_public = bool(yaml_dict.pop('is_public', False))
        connector_yaml_dict = yaml_dict.pop('connector', None)
        connector = MetaConnectorFactory.fromYamlDict(connector_yaml_dict) if connector_yaml_dict is not None else None
        sections_yaml_list = yaml_dict.pop('sections', None)
        sections = MetaSectionFactory.fromYamlList(sections_yaml_list) if sections_yaml_list is not None else []
        sections.extend(MetaSectionFactory.generateMissingDefaultSections(type_name, sections))
        child_nodes_yaml_list = yaml_dict.pop('child_nodes', None)
        child_nodes = MetaNodeFactory.fromYamlList(child_nodes_yaml_list) if child_nodes_yaml_list is not None else None
        return MetaNode(type_name, name, description, is_public, connector, sections, child_nodes)

    @staticmethod
    def fromYamlList(yaml_list):
        if yaml_list is None:
            raise Exception("yaml_list is None")
        if not isinstance(yaml_list, list):
            raise Exception("yaml_list is not a list instance")
        nodes = []
        for yaml_dict in yaml_list:
            nodes.append(MetaNodeFactory.fromYamlDict(yaml_dict))
        return nodes    