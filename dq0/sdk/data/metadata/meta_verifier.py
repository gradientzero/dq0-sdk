from dq0.sdk.data.metadata.meta_node import MetaNode
from dq0.sdk.data.metadata.meta_node_type import MetaNodeType


class MetaVerifier:
    @staticmethod
    def check(node):
        if node is None:
            raise Exception("node is none")
        if not isinstance(node, MetaNode):
            raise Exception("node is not an instance of MetaNode")
        if node.type_name is None:
            raise Exception("node.type_name is none")

    @staticmethod
    def verify(node, expected_type_names=None):
        MetaVerifier.check(node)
        if expected_type_names is not None and node.type_name not in expected_type_names:
            raise Exception(f"node.type_name {node.type_name} is not in expected type_names {expected_type_names}")
        if node.sections is not None:
            for section in node.sections:
                if section.type_name is None:
                    raise Exception("section.type_name is none")
                if not section.type_name.startswith(node.type_name):
                    raise Exception(f"section.type_name {section.type_name} does not start with node.type_name {node.type_name}")
        if node.child_nodes is not None:
            expected_type_name = None
            type_name = None
            for child_node in node.child_nodes:
                if node.type_name == MetaNodeType.TYPE_NAME_DATASET:
                    type_name = MetaVerifier.verify(child_node, [MetaNodeType.TYPE_NAME_DATABASE])
                elif node.type_name == MetaNodeType.TYPE_NAME_DATABASE:
                    type_name = MetaVerifier.verify(child_node, [MetaNodeType.TYPE_NAME_SCHEMA, MetaNodeType.TYPE_NAME_TABLE])
                elif node.type_name == MetaNodeType.TYPE_NAME_SCHEMA:
                    type_name = MetaVerifier.verify(child_node, [MetaNodeType.TYPE_NAME_TABLE])
                elif node.type_name == MetaNodeType.TYPE_NAME_TABLE:
                    type_name = MetaVerifier.verify(child_node, [MetaNodeType.TYPE_NAME_COLUMN])
                elif node.type_name == MetaNodeType.TYPE_NAME_COLUMN:
                    type_name = MetaVerifier.verify(child_node, [])
                else:
                    raise Exception(f"node.type_name {node.type_name} unknown")
                if expected_type_name is None:
                    expected_type_name = type_name
                if type_name != expected_type_name:
                    raise Exception(f"child_node must all be of same type. found {type_name} and {expected_type_name}")
        return node.type_name
    
    @staticmethod
    def verifySingleTable(node, expected_type_names=None):
        MetaVerifier.check(node)
        if expected_type_names is not None and node.type_name not in expected_type_names:
            raise Exception(f"node.type_name {node.type_name} is not in expected type_names {expected_type_names}")
        if node.sections is not None:
            for section in node.sections:
                if section.type_name is None:
                    raise Exception("section.type_name is none")
                if not section.type_name.startswith(node.type_name):
                    raise Exception(f"section.type_name {section.type_name} does not start with node.type_name {node.type_name}")
        if node.child_nodes is not None:
            expected_type_name = None
            type_name = None
            if (node.type_name == MetaNodeType.TYPE_NAME_DATASET or node.type_name == MetaNodeType.TYPE_NAME_DATABASE or node.type_name == MetaNodeType.TYPE_NAME_SCHEMA) and 1 != len(node.child_nodes):
                raise Exception(f"node of type {node.type_name} must have exactly one child node, has {len(node.child_nodes)}")
            for child_node in node.child_nodes:
                if node.type_name == MetaNodeType.TYPE_NAME_DATASET:
                    type_name = MetaVerifier.verify(child_node, [MetaNodeType.TYPE_NAME_DATABASE])
                elif node.type_name == MetaNodeType.TYPE_NAME_DATABASE:
                    type_name = MetaVerifier.verify(child_node, [MetaNodeType.TYPE_NAME_SCHEMA])
                elif node.type_name == MetaNodeType.TYPE_NAME_SCHEMA:
                    type_name = MetaVerifier.verify(child_node, [MetaNodeType.TYPE_NAME_TABLE])
                elif node.type_name == MetaNodeType.TYPE_NAME_TABLE:
                    type_name = MetaVerifier.verify(child_node, [MetaNodeType.TYPE_NAME_COLUMN])
                elif node.type_name == MetaNodeType.TYPE_NAME_COLUMN:
                    type_name = MetaVerifier.verify(child_node, [])
                else:
                    raise Exception(f"node.type_name {node.type_name} unknown")
                if expected_type_name is None:
                    expected_type_name = type_name
                if type_name != expected_type_name:
                    raise Exception(f"child nodes must all be of same type. found {type_name} and {expected_type_name}")
        return node.type_name

