from dq0.sdk.data.metadata.attribute.attribute_factory import AttributeFactory
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.node.node import Node
from dq0.sdk.data.metadata.permissions.permissions_factory import PermissionsFactory

class NodeFactory:
    FORMAT_TYPE_FULL = 'full'
    FORMAT_TYPE_SIMPLE = 'simple'
    
    NODE_YAML_TYPE_DICT = 'yaml_dict'
    NODE_YAML_TYPE_LIST = 'yaml_list'
    NODE_YAML_TYPE_SIMPLE = 'yaml_simple'

    @staticmethod
    def get_node_yaml_type(yaml_content, format_type=None):
        if isinstance(yaml_content, list):
            if format_type is not None:
                raise Exception(f"when the yaml content is a list, the format type may not be given")
            return NodeFactory.NODE_YAML_TYPE_LIST
        if isinstance(yaml_content, dict):
            if format_type is None:
                if 'type_name' not in yaml_content:
                    return NodeFactory.NODE_YAML_TYPE_SIMPLE
                return NodeFactory.NODE_YAML_TYPE_DICT
            elif format_type == NodeFactory.FORMAT_TYPE_FULL:
                return NodeFactory.NODE_YAML_TYPE_DICT
            elif format_type == NodeFactory.FORMAT_TYPE_SIMPLE:
                return NodeFactory.NODE_YAML_TYPE_SIMPLE
            else:
                raise Exception(f"format_type {format_type} is invalid")
        raise Exception(f"yaml_content is of unknown type {type(yaml_content)}")

    @staticmethod
    def verify_yaml_dict(yaml_dict):
        if not isinstance(yaml_dict, dict):
            raise Exception(f"yaml_dict is not of type dict, is of type {type(yaml_dict)} instead")
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if not NodeType.is_valid_type_name(type_name):
            raise Exception(f"invalid type_name {type_name}")

    @staticmethod
    def from_yaml_dict(yaml_dict):
        NodeFactory.verify_yaml_dict(yaml_dict=yaml_dict)
        type_name = yaml_dict.pop('type_name', None)
        attributes_yaml_list = yaml_dict.pop('attributes', None)
        attributes = [AttributeFactory.from_yaml_dict(yaml_dict=attribute_yaml_dict) for attribute_yaml_dict in attributes_yaml_list] if attributes_yaml_list is not None else None
        child_nodes_yaml_content = yaml_dict.pop('child_nodes', None)
        child_nodes = NodeFactory.from_yaml_content(yaml_content=child_nodes_yaml_content, force_list=True) if child_nodes_yaml_content is not None else None
        permissions_dict = yaml_dict.pop('permissions', None)
        permissions = PermissionsFactory.from_yaml_dict(yaml_dict=permissions_dict) if permissions_dict is not None else None
        return Node(type_name=type_name, attributes=attributes, child_nodes=child_nodes, permissions=permissions)

    @staticmethod
    def verify_yaml_simple_and_get_type_name(yaml_simple):
        if not isinstance(yaml_simple, dict):
            raise Exception(f"yaml_simple is not of type dict, is of type {type(yaml_simple)} instead")
        if len(yaml_simple) == 0:
            raise Exception("yaml_simple is empty")
        type_name = None
        indexes = set()
        for tmp_key in yaml_simple:
            if not isinstance(tmp_key, str):
                raise Exception(f"key in yaml_simple is not of type str, is of type {type(tmp_key)} instead")
            if '_' in tmp_key:
                tmp_type_name, _, tmp_index_string = tmp_key.rpartition('_')
            else:
                tmp_type_name = tmp_key
                tmp_index_string = '0'
            if type_name is None:
                type_name = tmp_type_name
            if type_name != tmp_type_name:
                raise Exception(f"types in yaml_simple differ, all must be the same, {type_name} and {tmp_type_name} found")
            index = int(tmp_index_string)
            if index in indexes:
                raise Exception(f"duplicate indexes in yaml_simple, found {index} multiple times")
            indexes.add(index)
        if not NodeType.is_valid_type_name(type_name):
            raise Exception(f"invalid type_name {type_name}")
        index = 0
        while len(indexes) != 0:
            if index not in indexes:
                raise Exception(f"simple_yaml is missing index {index} in its sequence")
            indexes.remove(index)
            index += 1
        return type_name

    @staticmethod
    def from_yaml_simple(yaml_simple, force_list=False):
        type_name = NodeFactory.verify_yaml_simple_and_get_type_name(yaml_simple=yaml_simple)
        nodes = []
        index = 0
        key = type_name
        if key not in yaml_simple:
            key = type_name + '_' + str(index)
        while key in yaml_simple:
            yaml_simple_dict = yaml_simple[key]
            attributes_yaml_content = yaml_simple_dict.pop('attributes', None)
            attributes = AttributeFactory.from_yaml_simple(yaml_simple_key=None, yaml_simple_value=attributes_yaml_content) if attributes_yaml_content is not None else None
            child_nodes_yaml_content = yaml_simple_dict.pop('child_nodes', None)
            child_nodes = NodeFactory.from_yaml_content(yaml_content=child_nodes_yaml_content, force_list=True) if child_nodes_yaml_content is not None else None
            nodes.append(Node(type_name=type_name, attributes=attributes, child_nodes=child_nodes, permissions=None))
            index += 1
            key = type_name + '_' + str(index)
        if not force_list and len(nodes) == 1:
            return nodes[0]
        return nodes

    @staticmethod
    def from_yaml_content(yaml_content, format_type=None, force_list=False):
        node_yaml_type = NodeFactory.get_node_yaml_type(yaml_content=yaml_content, format_type=format_type)
        if node_yaml_type == NodeFactory.NODE_YAML_TYPE_DICT:
            return NodeFactory.from_yaml_dict(yaml_dict=yaml_content)
        if node_yaml_type == NodeFactory.NODE_YAML_TYPE_LIST:
            return [NodeFactory.from_yaml_content(yaml_content=tmp_yaml_content, force_list=force_list) for tmp_yaml_content in yaml_content]
        if node_yaml_type == NodeFactory.NODE_YAML_TYPE_SIMPLE:
            return NodeFactory.from_yaml_simple(yaml_simple=yaml_content, force_list=force_list)
