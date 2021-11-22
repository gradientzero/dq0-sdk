import os
import yaml
from dq0.sdk.data.metadata.default.default import Default
from dq0.sdk.data.metadata.node.node_factory import NodeFactory
from dq0.sdk.data.metadata.node.node import Node


class Metadata:
    @staticmethod
    def from_yaml_file(filename, default=None):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"Could not find {filename}")
        with open(filename) as file:
            return Metadata.from_yaml(yaml_content=file, default=default)  

    @staticmethod
    def from_yaml(yaml_content, default=None):
        yaml_dict = yaml.load(stream=yaml_content, Loader=yaml.FullLoader)
        return Metadata(node=NodeFactory.from_yaml_content(yaml_content=yaml_dict, force_list=False), default=default)

    def __init__(self, node, default=None):
        if not isinstance(node, Node):
            raise Exception(f"node is not of type Node, is of type {type(node)} instead")
        self.node = node
        if default is not None:
            Default.check(default=default)
            self.node = default.apply_defaults(node=self.node)
            default.verify(node=self.node)

    def __str__(self, request_uuids=[]):
        return self.node.__str__(request_uuids=request_uuids)

    def __repr__(self):
        return "Metadata(node=" + repr(self.node) + ", verify_func=None, role_uuids=None)"

    def apply_defaults_and_verify(self, default):
        return Metadata(node=self.node, default=default)

    def filter(self, filter_func, default=None):
        if filter_func is None:
            raise Exception("filter_func is None")
        return Metadata(node=filter_func(node=self.node), default=default)

    def to_dict(self, request_uuids=[]):
        tmp_dict = self.node.to_dict(request_uuids=request_uuids) if self.node is not None else None
        return tmp_dict if tmp_dict is not None else {}

    def to_yaml(self, request_uuids=[]):
        return yaml.dump(self.to_dict(request_uuids=request_uuids))

    def merge_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=[], default=None):
        if other is None:
            raise Exception("other is None")
        if other.node is None:
            raise Exception("other.node is None")
        return Metadata(node=self.node.merge_with(other=other.node, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids), default=default)
