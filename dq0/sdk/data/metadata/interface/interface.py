from dq0.sdk.data.metadata.interface.dataset.entity import Entity
from dq0.sdk.data.metadata.interface.dataset.v1.dataset.dataset import Dataset
from dq0.sdk.data.metadata.metadata import Metadata
from dq0.sdk.data.metadata.node.node import Node
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.specification.dataset.v1.specification_v1 import SpecificationV1
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class Interface(Entity):
    def __init__(self, metadata, role_uuids=None, dataset_specification=None, other_specification=None):
        super().__init__(name='metadata', type_name='Metadata', parent=self, role_uuids=role_uuids)
        if not isinstance(metadata, Metadata):
            raise Exception(f"metadata is not of type Metadata, is of type {type(metadata)} instead")
        if metadata.dataset_node is not None and dataset_specification is None:
            raise Exception("dataset_specification missing")
        self.dataset_specification = dataset_specification
        if dataset_specification is not None:
            dataset_specification.verify(node=metadata.dataset_node)
        if metadata.other_node is not None and other_specification is None:
            raise Exception("other_specification missing")
        self.other_specification = other_specification
        if other_specification is not None:
            other_specification.verify(node=metadata.other_node)
        self.metadata = metadata
        self._dataset_entity = None

    def dataset(self, name=None):
        if name is None:
            if self.metadata.dataset_node is None:
                raise Exception("get without name may only work for existing dataset node")
            name = Entity.name_of(node=self.metadata.dataset_node)
        if self._dataset_entity is None:
            if isinstance(self.dataset_specification, SpecificationV1):
                self._dataset_entity = Dataset(name=name, parent=self,
                                               permissions=DefaultPermissions.shared_node(role_uuids=self.get_role_uuids()),
                                               data_permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()),
                                               name_permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()),
                                               role_uuids=self.get_role_uuids(), node=self.metadata.dataset_node)
            else:
                raise Exception("no interface for specified version available")
        if name != self._dataset_entity.get_name():
            raise Exception(f"name mismatch: {name} != {self._dataset_entity.get_name()}")
        return self._dataset_entity

    def create(self):
        pass

    def delete(self):
        pass

    def add_child_node(self, child_node):
        if not isinstance(child_node, Node):
            raise Exception(f"child_node is not of type Node, is of type {type(child_node)} instead")
        if child_node.get_type_name() != NodeType.TYPE_NAME_DATASET:
            raise Exception(f"child_node.get_type_name() mismatch: {child_node.get_type_name()} != {NodeType.TYPE_NAME_DATASET}")
        self.metadata.dataset_node = child_node

    def remove_child_node(self, name):
        if self.metadata.dataset_node is None:
            return
        self.metadata.dataset_node = None
        if self._dataset_entity is not None:
            if name != self._dataset_entity.get_name():
                raise Exception(f"name mismatch: {name} != {self._dataset_entity.get_name()}")
            self._dataset_entity.wipe()

    def set_name(self, old_name, new_name):
        pass

    def set_child_name(self, old_name, new_name):
        if not isinstance(old_name, str):
            raise Exception(f"old_name {old_name} is not of type str, is of type {type(old_name)} instead")
        if not isinstance(new_name, str):
            raise Exception(f"new_name {new_name} is not of type str, is of type {type(new_name)} instead")
