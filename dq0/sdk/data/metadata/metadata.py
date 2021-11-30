import os
import yaml
from dq0.sdk.data.metadata import node
from dq0.sdk.data.metadata.default.default import Default
from dq0.sdk.data.metadata.node.node_factory import NodeFactory
from dq0.sdk.data.metadata.node.node import Node


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
        default_version = yaml_dict.pop('metadata_default_version', None)
        format_type = yaml_dict.pop('metadata_format_type', None)
        node_dict = yaml_dict.pop('metadata_node', None)
        default = Default.obtain_with(version=default_version, role_uuids=role_uuids)
        return Metadata(node=NodeFactory.from_yaml_content(yaml_content=node_dict, format_type=format_type, force_list=False), default=default), default

    def __init__(self, node, default=None):
        if not isinstance(node, Node):
            raise Exception(f"node is not of type Node, is of type {type(node)} instead")
        self.node = node
        self.version = 0
        if default is not None:
            Default.check(default=default)
            self.node = default.apply_defaults(node=self.node)
            default.verify(node=self.node)
            self.version = default.version(requested_version=self.version)

    def __str__(self, request_uuids=set()):
        return_string = f"metadata_default_version: {self.version}" + '\n'
        return_string += f"metadata_format_type: '{NodeFactory.FORMAT_TYPE_SIMPLE}'"
        node_string = self.node.__str__(request_uuids=request_uuids)
        if node_string is not None:
            return_string += "\nmetadata_node:\n  " + node_string.replace('\n', "\n  ")
        return return_string

    def __repr__(self):
        return "Metadata(node=" + repr(self.node) + ", default=None)"

    def apply_defaults_and_verify(self, default):
        return Metadata(node=self.node.copy(), default=default)

    def filter(self, filter_func, default=None):
        if filter_func is None:
            raise Exception("filter_func is None")
        return Metadata(node=filter_func(node=self.node.copy()), default=default)

    def to_dict(self, request_uuids=set()):
        return {tmp_key: tmp_value for tmp_key, tmp_value in [
                ('metadata_default_version', self.version),
                ('metadata_format_type', NodeFactory.FORMAT_TYPE_FULL),
                ('metadata_node', self.node.to_dict(request_uuids=request_uuids) if self.node is not None else None),
            ] if tmp_value is not None}

    def to_yaml(self, request_uuids=set()):
        return yaml.dump(self.to_dict(request_uuids=request_uuids))

    def merge_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=set(), default=None):
        if other is None:
            raise Exception("other is None")
        if other.node is None:
            raise Exception("other.node is None")
        return Metadata(node=self.node.merge_with(other=other.node, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids), default=default)
