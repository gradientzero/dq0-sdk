from dq0.sdk.data.metadata.interface.dataset.v1.dataset.dataset import Dataset
from dq0.sdk.data.metadata.interface.entity import Entity
from dq0.sdk.data.metadata.interface.interface_iterator import InterfaceIterator
from dq0.sdk.data.metadata.interface.run.v1.run.run import Run
from dq0.sdk.data.metadata.specification.dataset.v1.specification_v1 import SpecificationV1 as DatasetSpecificationV1
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.run.v1.specification_v1 import SpecificationV1 as RunSpecificationV1
from dq0.sdk.data.metadata.structure.metadata import Metadata
from dq0.sdk.data.metadata.structure.node.node import Node
from dq0.sdk.data.metadata.structure.node.node_type import NodeType


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

    def __str__(self, request_uuids=set()):
        return self.get_metadata().__str__(request_uuids=request_uuids) if self.get_metadata() is not None else "Empty interface"

    def __len__(self):
        return len(self._metadata)

    def __iter__(self):
        return InterfaceIterator(interface=self)

    def to_dict(self, request_uuids=set(), full=True):
        return self.get_metadata().to_dict(request_uuids=request_uuids, full=full) if self.get_metadata() is not None else None

    def get_metadata(self):
        return self._metadata

    def create(self):
        pass

    def delete(self):
        pass

    def add_child_node(self, child_node):
        if not isinstance(child_node, Node):
            raise Exception(f"child_node is not of type Node, is of type {type(child_node)} instead")
        child_node_type_name = child_node.get_type_name()
        if child_node_type_name == NodeType.TYPE_NAME_DATASET:
            self._metadata.set_node(root_key=NodeType.TYPE_NAME_DATASET, node=child_node)
        elif child_node_type_name == NodeType.TYPE_NAME_RUN:
            self._metadata.set_node(root_key=NodeType.TYPE_NAME_RUN, node=child_node)
        else:
            raise Exception(f"unknown child_node_type_name={child_node_type_name}, must be one of [{NodeType.TYPE_NAME_DATASET}, {NodeType.TYPE_NAME_RUN}]")

    def remove_child_node(self, type_name, name):
        if self._metadata.get_node(root_key=NodeType.TYPE_NAME_DATASET) is None and self._metadata.get_node(root_key=NodeType.TYPE_NAME_RUN) is None:
            return
        if type_name not in [NodeType.TYPE_NAME_DATASET, NodeType.TYPE_NAME_RUN]:
            raise ValueError(f"unknown type_name={type_name}, must be one of [{NodeType.TYPE_NAME_DATASET}, {NodeType.TYPE_NAME_RUN}]")
        self._metadata.delete_node(root_key=type_name)
        if self._entities[type_name] is not None:
            if name != self._entities[type_name].get_name():
                raise Exception(f"name mismatch: {name} != {self._entities[type_name].get_name()}")
            self._entities[type_name].wipe()

    def set_name(self, old_name, new_name):
        pass

    def set_child_name(self, old_name, new_name):
        pass

    def apply_defaults_and_verify(self, specifications=None):
        return Interface(metadata=self._metadata.apply_defaults_and_verify(specifications=specifications), role_uuids=self.get_role_uuids())

    def dataset(self, name=None, specification=None):
        node = self._metadata.get_node(root_key=NodeType.TYPE_NAME_DATASET)
        if name is None:
            if node is None:
                raise Exception("get without name may only work for existing dataset node")
            name = Entity.name_of(node=node)
        if NodeType.TYPE_NAME_DATASET not in self._entities:
            internal_specification = self._metadata.get_specification(root_key=NodeType.TYPE_NAME_DATASET)
            if internal_specification is None and specification is not None:
                internal_specification = specification
            if isinstance(internal_specification, DatasetSpecificationV1):
                self._entities[NodeType.TYPE_NAME_DATASET] = Dataset(name=name, parent=self,
                                                                     permissions=DefaultPermissions.shared_node(role_uuids=self.get_role_uuids()),
                                                                     data_permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()),
                                                                     name_permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()),
                                                                     role_uuids=self.get_role_uuids(), node=node)
            else:
                raise Exception(f"no interface for specified version={internal_specification} available")
        if name != self._entities[NodeType.TYPE_NAME_DATASET].get_name():
            raise Exception(f"name mismatch: {name} != {self._entities[NodeType.TYPE_NAME_DATASET].get_name()}")
        return self._entities[NodeType.TYPE_NAME_DATASET]

    def run(self, name=None, specification=None):
        node = self._metadata.get_node(root_key=NodeType.TYPE_NAME_RUN)
        if name is None:
            if node is None:
                raise Exception("get without name may only work for existing run node")
            name = Entity.name_of(node=node)
        if NodeType.TYPE_NAME_RUN not in self._entities:
            internal_specification = self._metadata.get_specification(root_key=NodeType.TYPE_NAME_RUN)
            if internal_specification is None and specification is not None:
                internal_specification = specification
            if isinstance(internal_specification, RunSpecificationV1):
                self._entities[NodeType.TYPE_NAME_RUN] = Run(name=name, parent=self,
                                                             permissions=DefaultPermissions.analyst_node(role_uuids=self.get_role_uuids()),
                                                             data_permissions=DefaultPermissions.analyst_attribute(role_uuids=self.get_role_uuids()),
                                                             name_permissions=DefaultPermissions.analyst_attribute(role_uuids=self.get_role_uuids()),
                                                             role_uuids=self.get_role_uuids(), node=node)
            else:
                raise Exception(f"no interface for specified version={internal_specification} available")
        if name != self._entities[NodeType.TYPE_NAME_RUN].get_name():
            raise Exception(f"name mismatch: {name} != {self._entities[NodeType.TYPE_NAME_RUN].get_name()}")
        return self._entities[NodeType.TYPE_NAME_RUN]
