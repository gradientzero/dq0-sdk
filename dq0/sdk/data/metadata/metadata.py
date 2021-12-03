import os
import yaml
from dq0.sdk.data.metadata.node.node_factory import NodeFactory
from dq0.sdk.data.metadata.node.node import Node
from dq0.sdk.data.metadata.specification.specification import Specification
from dq0.sdk.data.metadata.specification.specification_factory import SpecificationFactory


# The other_node and other_specifications are not used yet and may be removed or replaced.
# They are here to demonstrate how to implement another root node next to the dataset root.
class Metadata:
    @staticmethod
    def from_yaml_file(filename, role_uuids=None):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"Could not find {filename}")
        with open(filename) as file:
            return Metadata.from_yaml(yaml_content=file, role_uuids=role_uuids)  

    @staticmethod
    def from_yaml(yaml_content, role_uuids=None):
        yaml_dict = yaml.load(stream=yaml_content, Loader=yaml.FullLoader)
        dataset_dict = yaml_dict.pop('meta_dataset', None)
        dataset_node, dataset_specification = Metadata.from_yaml_dict(yaml_dict=dataset_dict, role_uuids=role_uuids)
        other_dict = yaml_dict.pop('meta_other', None)
        other_node, other_specification = Metadata.from_yaml_dict(yaml_dict=other_dict, role_uuids=role_uuids)
        return Metadata(dataset_node=dataset_node, other_node=other_node, dataset_specification=dataset_specification, other_specification=other_specification), dataset_specification, other_specification

    @staticmethod
    def from_yaml_dict(yaml_dict, role_uuids=None):
        if yaml_dict is None:
            return None, None
        format_type = yaml_dict.pop('format', None)
        node_dict = yaml_dict.pop('node', None)
        specification_string = yaml_dict.pop('specification', None)
        specification = SpecificationFactory.from_specification_string(specification_string=specification_string, role_uuids=role_uuids)
        return NodeFactory.from_yaml_content(yaml_content=node_dict, format_type=format_type, force_list=False), specification

    def __init__(self, dataset_node=None, other_node=None, dataset_specification=None, other_specification=None):
        if dataset_node is not None and not isinstance(dataset_node, Node):
            raise Exception(f"dataset_node is not of type Node, is of type {type(dataset_node)} instead")
        if other_node is not None and not isinstance(other_node, Node):
            raise Exception(f"other_node is not of type Node, is of type {type(other_node)} instead")
        self.dataset_node = dataset_node
        self.other_node = other_node
        self.dataset_specification = None
        self.other_specification = None
        if dataset_specification is not None:
            Specification.check(specification=dataset_specification)
            self.dataset_node = dataset_specification.apply_defaults(node=self.dataset_node)
            dataset_specification.verify(node=self.dataset_node)
            self.dataset_specification = dataset_specification
        if other_specification is not None:
            Specification.check(specification=other_specification)
            self.other_node = other_specification.apply_defaults(node=self.other_node)
            other_specification.verify(node=self.other_node)
            self.other_specification = other_specification

    def __str__(self, request_uuids=set()):
        return_string = ''
        if self.dataset_node is not None:
            return_string += "meta_dataset:\n  " + self.dataset_str(request_uuids=request_uuids).replace('\n', "\n  ")
        if self.dataset_node is not None and self.other_node is not None:
            return_string += '\n'
        if self.other_node is not None:
            return_string += "meta_other:\n  " + self.other_str(request_uuids=request_uuids).replace('\n', "\n  ")
        return return_string

    def __repr__(self):
        return "Metadata(dataset_node=" + repr(self.dataset_node) + ", other_node=" + repr(self.other_node) + ", dataset_specification=None, other_specification=None)"

    def dataset_str(self, request_uuids=set()):
        return_string = f"format: {NodeFactory.FORMAT_TYPE_SIMPLE}"
        node_string = self.dataset_node.__str__(request_uuids=request_uuids)
        if node_string is not None:
            return_string += "\nnode:\n  " + node_string.replace('\n', "\n  ")
        if self.dataset_specification is not None:
            return_string += '\n' + f"specification: '{self.dataset_specification}'"
        return return_string

    def other_str(self, request_uuids=set()):
        return_string = f"format: {NodeFactory.FORMAT_TYPE_SIMPLE}"
        node_string = self.other_node.__str__(request_uuids=request_uuids)
        if node_string is not None:
            return_string += "\nnode:\n  " + node_string.replace('\n', "\n  ")
        if self.other_specification is not None:
            return_string += '\n' + f"specification: '{self.other_specification}'"
        return return_string

    def apply_defaults_and_verify(self, dataset_specification=None, other_specification=None):
        if dataset_specification is None:
            dataset_specification = self.dataset_specification
        if other_specification is None:
            other_specification = self.other_specification
        applied_dataset_node = None
        applied_other_node = None
        if self.dataset_node is not None:
            applied_dataset_node = self.dataset_node.copy()
        if self.other_node is not None:
            applied_other_node = self.other_node.copy()
        return Metadata(dataset_node=applied_dataset_node, other_node=applied_other_node, dataset_specification=dataset_specification, other_specification=self.other_specification)

    def filter(self, dataset_filter_func=None, other_filter_func=None, dataset_specification=None, other_specification=None):
        if dataset_specification is None:
            dataset_specification = self.dataset_specification
        if other_specification is None:
            other_specification = self.other_specification
        filtered_dataset_node = None
        filtered_other_node = None
        if self.dataset_node is not None:
            if dataset_filter_func is not None:
                filtered_dataset_node = dataset_filter_func(node=self.dataset_node.copy())
            else:
                filtered_dataset_node = self.dataset_node.copy()
        if self.other_node is not None:
            if other_filter_func is not None:
                filtered_other_node = other_filter_func(node=self.other_node.copy())
            else:
                filtered_other_node = self.other_node.copy()        
        return Metadata(dataset_node=filtered_dataset_node, other_node=filtered_other_node, dataset_specification=dataset_specification, other_specification=self.other_specification)

    def to_dict(self, request_uuids=set()):
        return {tmp_key: tmp_value for tmp_key, tmp_value in [
                ('meta_dataset', self.dataset_to_dict(request_uuids=request_uuids)),
                ('meta_other', self.other_to_dict(request_uuids=request_uuids)),
            ] if tmp_value is not None}

    def dataset_to_dict(self, request_uuids=set()):
        if self.dataset_node is None:
            return None
        return {tmp_key: tmp_value for tmp_key, tmp_value in [
                ('format', NodeFactory.FORMAT_TYPE_FULL),
                ('node', self.dataset_node.to_dict(request_uuids=request_uuids) if self.dataset_node is not None else None),
                ('specification', str(self.dataset_specification) if self.dataset_specification is not None else None),
            ] if tmp_value is not None}

    def other_to_dict(self, request_uuids=set()):
        if self.other_node is None:
            return None
        return {tmp_key: tmp_value for tmp_key, tmp_value in [
                ('format', NodeFactory.FORMAT_TYPE_FULL),
                ('node', self.other_node.to_dict(request_uuids=request_uuids) if self.other_node is not None else None),
                ('specification', str(self.other_specification) if self.other_specification is not None else None),
            ] if tmp_value is not None}

    def to_yaml(self, request_uuids=set()):
        return yaml.dump(self.to_dict(request_uuids=request_uuids))

    def merge_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=set(), dataset_specification=None, other_specification=None):
        if other is None:
            raise Exception("other is None")
        if dataset_specification is None:
            dataset_specification = self.dataset_specification
        if other_specification is None:
            other_specification = self.other_specification
        merged_dataset_node = None
        merged_other_node = None
        if self.dataset_node is not None:
            if other.dataset_node is not None:
                merged_dataset_node = self.dataset_node.merge_with(
                    other=other.dataset_node,
                    overwrite_value=overwrite_value,
                    overwrite_permissions=overwrite_permissions,
                    request_uuids=request_uuids)
            else:
                merged_dataset_node = self.dataset_node.copy()
        else:
            merged_dataset_node = other.dataset_node.copy() if other.dataset_node is not None else None
        if self.other_node is not None:
            if other.other_node is not None:
                merged_other_node = self.other_node.merge_with(
                    other=other.other_node,
                    overwrite_value=overwrite_value,
                    overwrite_permissions=overwrite_permissions,
                    request_uuids=request_uuids)
            else:
                merged_other_node = self.other_node.copy()
        else:
            merged_other_node = other.other_node.copy() if other.other_node is not None else None
        return Metadata(dataset_node=merged_dataset_node, other_node=merged_other_node, dataset_specification=dataset_specification, other_specification=other_specification)
