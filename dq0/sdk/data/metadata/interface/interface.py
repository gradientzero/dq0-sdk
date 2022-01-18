from dq0.sdk.data.metadata.interface.dataset.entity import Entity
from dq0.sdk.data.metadata.interface.dataset.v1.dataset.dataset import Dataset
from dq0.sdk.data.metadata.interface.interface_iterator import InterfaceIterator
from dq0.sdk.data.metadata.metadata import Metadata
from dq0.sdk.data.metadata.node.node import Node
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.specification.dataset.v1.specification_v1 import SpecificationV1
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class Interface(Entity):
    @staticmethod
    def check_specifications(metadata):
        for root_key in Metadata.ROOT_KEYS:
            node = metadata.get_node(root_key=root_key)
            if node is not None:
                specification = metadata.get_specification(root_key=root_key)
                if specification is None:
                    raise Exception(f"specification for {root_key} is missing")
                specification.verify(node=node)

    def __init__(self, metadata, role_uuids=None):
        super().__init__(name='metadata', type_name='Metadata', parent=self, role_uuids=role_uuids)
        if not isinstance(metadata, Metadata):
            raise Exception(f"metadata is not of type Metadata, is of type {type(metadata)} instead")
        Interface.check_specifications(metadata=metadata)
        self._metadata = metadata
        self._entities = {}

    def __len__(self):
        return len(self._metadata)

    def __iter__(self):
        return InterfaceIterator(interface=self)

    def to_dict(self, request_uuids=set()):
        return self.get_metadata().to_dict(request_uuids=request_uuids) if self.get_metadata() is not None else None

    def get_metadata(self):
        return self._metadata

    def dataset(self, name=None):
        node = self._metadata.get_node(root_key='dataset')
        if name is None:
            if node is None:
                raise Exception("get without name may only work for existing dataset node")
            name = Entity.name_of(node=node)
        if 'dataset' not in self._entities:
            specification = self._metadata.get_specification(root_key='dataset')
            if isinstance(specification, SpecificationV1):
                self._entities['dataset'] = Dataset(name=name, parent=self,
                                                    permissions=DefaultPermissions.shared_node(role_uuids=self.get_role_uuids()),
                                                    data_permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()),
                                                    name_permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()),
                                                    role_uuids=self.get_role_uuids(), node=node)
            else:
                raise Exception("no interface for specified version available")
        if name != self._entities['dataset'].get_name():
            raise Exception(f"name mismatch: {name} != {self._entities['dataset'].get_name()}")
        return self._entities['dataset']

    def create(self):
        pass

    def delete(self):
        pass

    def add_child_node(self, child_node):
        if not isinstance(child_node, Node):
            raise Exception(f"child_node is not of type Node, is of type {type(child_node)} instead")
        if child_node.get_type_name() != NodeType.TYPE_NAME_DATASET:
            raise Exception(f"child_node.get_type_name() mismatch: {child_node.get_type_name()} != {NodeType.TYPE_NAME_DATASET}")
        self._metadata.set_node(root_key='dataset', node=child_node)

    def remove_child_node(self, name):
        if self._metadata.get_node(root_key='dataset') is None:
            return
        self._metadata.delete_node(root_key='dataset')
        if self._entities['dataset'] is not None:
            if name != self._entities['dataset'].get_name():
                raise Exception(f"name mismatch: {name} != {self._entities['dataset'].get_name()}")
            self._entities['dataset'].wipe()

    def set_name(self, old_name, new_name):
        pass

    def set_child_name(self, old_name, new_name):
        pass
