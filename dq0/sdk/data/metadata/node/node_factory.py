from dq0.sdk.data.metadata.attribute.attribute_factory import AttributeFactory
from dq0.sdk.data.metadata.default.default_applicator import DefaultApplicator
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.node.node import Node

class NodeFactory:
    @staticmethod
    def verifyYamlDict(yaml_dict, expected_type_name=None):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if not NodeType.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if expected_type_name is not None and type_name != expected_type_name:
            raise Exception(f"type_name must be {expected_type_name} was {type_name}")

    @staticmethod
    def fromYamlDict(yaml_dict, apply_default_attributes=None):
        if apply_default_attributes is None:
            apply_default_attributes = DefaultApplicator.applyDefaultAttributes
        NodeFactory.verifyYamlDict(yaml_dict=yaml_dict)
        type_name = yaml_dict.pop('type_name', None)
        attributes_yaml_list = yaml_dict.pop('attributes', None)
        attributes = apply_default_attributes([AttributeFactory.fromYamlDict(yaml_dict=attribute_yaml_dict) for attribute_yaml_dict in attributes_yaml_list]) if attributes_yaml_list is not None else None
        child_nodes_yaml_list = yaml_dict.pop('child_nodes', None)
        child_nodes = [NodeFactory.fromYamlDict(yaml_dict=child_node_yaml_dict) for child_node_yaml_dict in child_nodes_yaml_list] if child_nodes_yaml_list is not None else None
        return Node(type_name=type_name, attributes=attributes, child_nodes=child_nodes)
