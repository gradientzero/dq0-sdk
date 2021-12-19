from dq0.sdk.data.metadata.node.node import Node
from dq0.sdk.data.metadata.node.node_type import NodeType


class Column:
    def __init__(self, node):
        if not isinstance(node, Node):
            raise Exception(f"node is not of type Node, is of type {type(node)} instead")
        if node.type_name != NodeType.TYPE_NAME_COLUMN:
            raise Exception(f"node must have type_name {NodeType.TYPE_NAME_COLUMN}, has {node.type_name} instead")
        self.node = node
