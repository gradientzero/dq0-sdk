from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.node.node import Node


class Verifier:
    @staticmethod
    def check(node):
        if node is None:
            raise Exception("node is none")
        if not isinstance(node, Node):
            raise Exception(f"node is not of type Node, is of type {type(Node)} instead")
        if node.type_name is None:
            raise Exception("node.type_name is none")

    @staticmethod
    def verify(node, expected_type_names=None):
        Verifier.check(node)
        if expected_type_names is not None and node.type_name not in expected_type_names:
            raise Exception(f"node.type_name {node.type_name} is not in expected type_names {expected_type_names}")
        Attribute.check_list_and_is_explicit_list(list=node.attributes, additional=None)
        if node.child_nodes is not None:
            expected_type_name = None
            type_name = None
            for child_node in node.child_nodes:
                if node.type_name == NodeType.TYPE_NAME_DATASET:
                    type_name = Verifier.verify(node=child_node, expected_type_names=[NodeType.TYPE_NAME_DATABASE])
                elif node.type_name == NodeType.TYPE_NAME_DATABASE:
                    type_name = Verifier.verify(node=child_node, expected_type_names=[NodeType.TYPE_NAME_SCHEMA, NodeType.TYPE_NAME_TABLE])
                elif node.type_name == NodeType.TYPE_NAME_SCHEMA:
                    type_name = Verifier.verify(node=child_node, expected_type_names=[NodeType.TYPE_NAME_TABLE])
                elif node.type_name == NodeType.TYPE_NAME_TABLE:
                    type_name = Verifier.verify(node=child_node, expected_type_names=[NodeType.TYPE_NAME_COLUMN])
                elif node.type_name == NodeType.TYPE_NAME_COLUMN:
                    type_name = Verifier.verify(node=child_node, expected_type_names=[])
                else:
                    raise Exception(f"node.type_name {node.type_name} unknown")
                if expected_type_name is None:
                    expected_type_name = type_name
                if type_name != expected_type_name:
                    raise Exception(f"child_nodes must all be of same type. found {type_name} and {expected_type_name}")
        return node.type_name
    
    @staticmethod
    def verifyAllSingleWithSchema(node, expected_type_names=None):
        Verifier.check(node=node)
        if expected_type_names is not None and node.type_name not in expected_type_names:
            raise Exception(f"node.type_name {node.type_name} is not in expected type_names {expected_type_names}")
        Attribute.check_list_and_is_explicit_list(list=node.attributes, additional=None)
        if node.child_nodes is not None:
            expected_type_name = None
            type_name = None
            if (node.type_name == NodeType.TYPE_NAME_DATASET or node.type_name == NodeType.TYPE_NAME_DATABASE or node.type_name == NodeType.TYPE_NAME_SCHEMA) and 1 != len(node.child_nodes):
                raise Exception(f"node of type {node.type_name} must have exactly one child node, has {len(node.child_nodes)}")
            for child_node in node.child_nodes:
                if node.type_name == NodeType.TYPE_NAME_DATASET:
                    type_name = Verifier.verify(node=child_node, expected_type_names=[NodeType.TYPE_NAME_DATABASE])
                elif node.type_name == NodeType.TYPE_NAME_DATABASE:
                    type_name = Verifier.verify(node=child_node, expected_type_names=[NodeType.TYPE_NAME_SCHEMA])
                elif node.type_name == NodeType.TYPE_NAME_SCHEMA:
                    type_name = Verifier.verify(node=child_node, expected_type_names=[NodeType.TYPE_NAME_TABLE])
                elif node.type_name == NodeType.TYPE_NAME_TABLE:
                    type_name = Verifier.verify(node=child_node, expected_type_names=[NodeType.TYPE_NAME_COLUMN])
                elif node.type_name == NodeType.TYPE_NAME_COLUMN:
                    type_name = Verifier.verify(node=child_node, expected_type_names=[])
                else:
                    raise Exception(f"node.type_name {node.type_name} unknown")
                if expected_type_name is None:
                    expected_type_name = type_name
                if type_name != expected_type_name:
                    raise Exception(f"child nodes must all be of same type. found {type_name} and {expected_type_name}")
        return node.type_name

