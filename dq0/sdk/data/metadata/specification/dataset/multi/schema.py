from dq0.sdk.data.metadata.node.node import Node
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.dataset.standard.schema import Schema as StandardSchema
from dq0.sdk.data.metadata.specification.dataset.standard.table import Table as StandardTable


class Schema:
    @staticmethod
    def apply_defaults(node, role_uuids=None):
        return StandardSchema.apply_defaults(node=node, role_uuids=role_uuids)

    @staticmethod
    def verify(node, role_uuids=None):
        Node.check(node=node, allowed_type_names=[NodeType.TYPE_NAME_SCHEMA], allowed_permissions=DefaultPermissions.shared_node(role_uuids=role_uuids))
        StandardSchema.verify_attributes(attributes=node.attributes, role_uuids=role_uuids)
        Schema.verify_child_nodes(child_nodes=node.child_nodes, role_uuids=role_uuids)

    @staticmethod
    def verify_child_nodes(child_nodes, role_uuids=None):
        for child_node in child_nodes if child_nodes is not None else []:
            StandardTable.verify(node=child_node, role_uuids=role_uuids)
