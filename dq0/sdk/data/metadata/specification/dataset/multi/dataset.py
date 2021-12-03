from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.node.node import Node
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.dataset.multi.database import Database
from dq0.sdk.data.metadata.specification.dataset.standard.dataset import Dataset as StandardDataset


class Dataset:
    @staticmethod
    def apply_defaults(node, role_uuids=None):
        return StandardDataset.apply_defaults(node=node, role_uuids=role_uuids)

    @staticmethod
    def verify(node, role_uuids=None):
        Node.check(node=node, allowed_type_names=[NodeType.TYPE_NAME_DATASET], allowed_permissions=DefaultPermissions.shared_node(role_uuids=role_uuids))
        StandardDataset.verify_attributes(attributes=node.attributes, role_uuids=role_uuids)
        Dataset.verify_child_nodes(child_nodes=node.child_nodes, role_uuids=role_uuids)

    @staticmethod
    def verify_child_nodes(child_nodes, role_uuids=None):
        for child_node in child_nodes if child_nodes is not None else []:
            Database.verify(node=child_node, role_uuids=role_uuids)
