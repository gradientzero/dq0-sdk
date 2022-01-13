from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.explanation import Explanation
from dq0.sdk.data.metadata.merge_exception import MergeException
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.permissions.action import Action
from dq0.sdk.data.metadata.permissions.permissions import Permissions
from dq0.sdk.data.metadata.utils.list_utils import ListUtils
from dq0.sdk.data.metadata.utils.str_utils import StrUtils


class Node:
    @staticmethod
    def check(node, allowed_type_names=None, allowed_permissions=None):
        if not isinstance(node, Node):
            raise Exception(f"node is not of type Node, is of type {type(node)} instead")
        if not NodeType.is_valid_type_name(type_name=node._type_name):
            raise Exception(f"node._type_name {node._type_name} is not valid")
        if allowed_type_names is not None and node._type_name not in allowed_type_names:
            raise Exception(f"node._type_name {node._type_name} is not in allowed_type_names {allowed_type_names}")
        if not Permissions.is_subset_of(permissions_a=node._permissions, permissions_b=allowed_permissions):
            raise Exception(f"node.permissions {node._permissions} are not in allowed_permissions {allowed_permissions}")

    @staticmethod
    def check_list(node_list, allowed_type_names=None, allowed_permissions=None):
        if node_list is None:
            return
        if not isinstance(node_list, list):
            raise Exception(f"node_list is not of type list, is of type {type(node_list)} instead")
        for node in node_list:
            Node.check(node=node, allowed_type_names=allowed_type_names, allowed_permissions=allowed_permissions)

    @staticmethod
    def check_list_merge_duplicates(node_list, allowed_type_names=None, allowed_permissions=None):
        Node.check_list(node_list=node_list, allowed_type_names=allowed_type_names, allowed_permissions=allowed_permissions)
        tmp_list = node_list.copy() if node_list is not None else []
        while 0 < len(tmp_list):
            elem_a = tmp_list.pop()
            for elem_b in tmp_list:
                try:
                    if elem_a.is_mergeable_with(other=elem_b, overwrite_value=False, overwrite_permissions=False, request_uuids=None):
                        raise Exception("mergeable nodes:\n" + str(elem_a) + "\nand:\n" + str(elem_b) + "\ndetected in:\n" + str(list))
                except MergeException:
                    pass

    @staticmethod
    def are_merge_compatible(node_list_a, node_list_b, explanation=None):
        Node.check_list(node_list=node_list_a, allowed_type_names=None, allowed_permissions=None)
        Node.check_list(node_list=node_list_b, allowed_type_names=None, allowed_permissions=None)
        if node_list_a is None or len(node_list_a) == 0 or node_list_b is None or len(node_list_b) == 0:
            return True
        for elem_a in node_list_a:
            for elem_b in node_list_b:
                if not elem_a.is_merge_compatible_with(other=elem_b, explanation=explanation):
                    Explanation.dynamic_add_message(explanation=explanation,
                                                    message="Node.are_merge_compatible(...): "
                                                    f"nodes[{elem_a._type_name}] are not compatible")
                    return False
        return True

    @staticmethod
    def are_mergeable(list_a, list_b, overwrite_value=False, overwrite_permissions=False, request_uuids=set(), explanation=None):
        if not Node.are_merge_compatible(node_list_a=list_a, node_list_b=list_b):
            Explanation.dynamic_add_message(explanation=explanation, message="Node.are_mergeable(...): nodes are not compatible")
            return False
        if list_a is None or len(list_a) == 0:
            return True
        if list_b is None or len(list_b) == 0:
            return True
        for elem_a in list_a:
            found_match = False
            for elem_b in list_b:
                if elem_a.is_mergeable_with(other=elem_b, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                            request_uuids=request_uuids, explanation=None):
                    if found_match:
                        Explanation.dynamic_add_message(explanation=explanation,
                                                        message=f"Node.are_mergeable(...): duplicate mergeable nodes[{elem_a._type_name}] are not allowed")
                        return False
                    found_match = True
        return True

    @staticmethod
    def merge_many(list_a, list_b, overwrite_value=False, overwrite_permissions=False, request_uuids=set()):
        explanation = Explanation()
        if not Node.are_mergeable(list_a=list_a, list_b=list_b, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                  request_uuids=request_uuids, explanation=explanation):
            raise MergeException(f"cannot merge nodes that are not mergeable; list_a: {list_a} list_b: {list_b} explanation: {explanation}")
        if list_a is None or len(list_a) == 0:
            return None if list_b is None or len(list_b) == 0 else list_b
        if list_b is None or len(list_b) == 0:
            return None if list_a is None or len(list_a) == 0 else list_a
        merged = []
        tmp_list_b = list_b.copy()
        for elem_a in list_a:
            elem_merged = elem_a.copy()
            for elem_b in tmp_list_b:
                if elem_a.is_mergeable_with(other=elem_b, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                            request_uuids=request_uuids):
                    tmp_list_b.remove(elem_b)
                    elem_merged = elem_a.merge_with(other=elem_b, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                                    request_uuids=request_uuids)
                    break
            merged.append(elem_merged)
        for elem_b in tmp_list_b:
            for elem_a in list_a:
                if elem_a.is_mergeable_with(other=elem_b, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                            request_uuids=request_uuids):
                    raise Exception("this can never happen")
            merged.append(elem_b.copy())
        return merged

    @staticmethod
    def attributes_list_matches_map(attributes_list, attributes_map):
        if attributes_list is None:
            return attributes_map is None
        for key, value in attributes_map.items() if attributes_map is not None else {}:
            tmp_attributes_list = None
            if key is None:
                tmp_attributes_list = [tmp_attribute for tmp_attribute in attributes_list if tmp_attribute is not None and tmp_attribute.get_value() == value]
            else:
                tmp_attributes_list = [tmp_attribute for tmp_attribute in attributes_list if tmp_attribute is not None and tmp_attribute.get_key() == key]
            if 0 < len(tmp_attributes_list):
                tmp_attribute = tmp_attributes_list[0]
                if isinstance(value, dict):
                    if not Node.attributes_list_matches_map(attributes_list=tmp_attribute.get_value(), attributes_map=value):
                        return False
                elif tmp_attribute.get_value() != value:
                    return False
            else:
                return False
        return True

    def __init__(self, type_name, attributes=None, child_nodes=None, permissions=None):
        if not NodeType.is_valid_type_name(type_name=type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if Attribute.check_list(attribute_list=attributes, check_data=None):
            raise Exception("node may not have list of attributes with multiple null keys")
        Node.check_list_merge_duplicates(node_list=child_nodes, allowed_type_names=None, allowed_permissions=None)
        Permissions.check(permissions=permissions)
        self._type_name = type_name
        self._attributes = attributes
        self._child_nodes = child_nodes
        for index, tmp_child_node in enumerate(self._child_nodes if self._child_nodes is not None else []):
            tmp_child_node._list_index = index if 1 < len(self._child_nodes) else -1
        self._permissions = permissions
        self._list_index = -1

    def __str__(self, request_uuids=set()):
        if not Permissions.is_allowed_with(permissions=self._permissions, action=Action.READ, request_uuids=request_uuids):
            return None
        index_string = f"_{self._list_index}" if -1 < self._list_index else ''
        return_string = StrUtils.str_from(object=self._type_name, quoted=False) + index_string + ':'
        if self._attributes is not None and len(self._attributes) > 0:
            return_string += "\n  attributes:" + StrUtils.restricted_str_from_list(list=self._attributes, sort=False,
                                                                                   request_uuids=request_uuids).replace('\n', "\n  ")
        if self._child_nodes is not None and len(self._child_nodes) > 0:
            return_string += "\n  child_nodes:" + StrUtils.restricted_str_from_list(list=self._child_nodes, sort=False,
                                                                                    request_uuids=request_uuids).replace('\n', "\n    ")
        return return_string

    def __repr__(self):
        return "Node(" + \
            "type_name=" + repr(self._type_name) + ", " + \
            "attributes=" + repr(self._attributes) + ", " + \
            "child_nodes=" + repr(self._child_nodes) + ", " + \
            "permissions=" + repr(self._permissions) + ')'

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        if not ListUtils.list_equals_unordered(list_a=self._attributes, list_b=other._attributes):
            return False
        if not ListUtils.list_equals_unordered(list_a=self._child_nodes, list_b=other._child_nodes):
            return False
        return \
            self._type_name == other._type_name and \
            self._permissions == other._permissions

    def get_type_name(self):
        return self._type_name

    def get_attributes(self):
        return self._attributes

    def get_permissions(self):
        return self._permissions

    def copy(self):
        copied_node = Node(
            type_name=self._type_name,
            attributes=[tmp_attribute.copy() for tmp_attribute in self._attributes] if self._attributes is not None else None,
            child_nodes=[tmp_child_node.copy() for tmp_child_node in self._child_nodes] if self._child_nodes is not None else None,
            permissions=self._permissions.copy() if self._permissions is not None else None
        )
        copied_node._list_index = self._list_index
        return copied_node

    def to_dict(self, request_uuids=set()):
        if not Permissions.is_allowed_with(permissions=self._permissions, action=Action.READ, request_uuids=request_uuids):
            return None
        return {tmp_key: tmp_value for tmp_key, tmp_value in [
            ('type_name', self._type_name),
            ('attributes', ListUtils.list_map_to_dict(self._attributes, request_uuids=request_uuids)),
            ('child_nodes', ListUtils.list_map_to_dict(self._child_nodes, request_uuids=request_uuids)),
            ('permissions', self._permissions.to_dict() if self._permissions is not None else None),
        ] if tmp_value is not None}

    def is_merge_compatible_with(self, other, explanation=None):
        if not isinstance(other, Node):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Node[{self._type_name}].is_merge_compatible_with(...): "
                                            f"other is not of type Node, is of type {type(other)} instead")
            return False
        if self._type_name != other._type_name:
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Node[{self._type_name}].is_merge_compatible_with(...): "
                                            f"type_name mismatch {self._type_name} != {other._type_name}")
            return False
        if not Attribute.are_merge_compatible(attribute_list_a=self._attributes, attribute_list_b=other._attributes, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Node[{self._type_name}].is_merge_compatible_with(...): "
                                            f"attributes are not compatible")
            return False
        if not Node.are_merge_compatible(node_list_a=self._child_nodes, node_list_b=other._child_nodes, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Node[{self._type_name}].is_merge_compatible_with(...): "
                                            f"child_nodes are not compatible")
            return False
        if not Permissions.are_merge_compatible(permissions_a=self._permissions, permissions_b=other._permissions):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Node[{self._type_name}].is_merge_compatible_with(...): "
                                            f"permissions are not compatible")
            return False
        return True

    def is_mergeable_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=set(), explanation=None):
        if not self.is_merge_compatible_with(other=other, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation, message=f"Node[{self._type_name}].is_mergeable_with(...): other is not compatible")
            return False
        if not Attribute.are_mergeable(attribute_list_a=self._attributes, attribute_list_b=other._attributes,
                                       overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation, message=f"Node[{self._type_name}].is_mergeable_with(...): attributes are not mergeable")
            return False
        merged_attributes = Attribute.merge_many(attribute_list_a=self._attributes, attribute_list_b=other._attributes,
                                                 overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids)
        if self._attributes != merged_attributes and not Permissions.is_allowed_with(permissions=self._permissions, action=Action.WRITE_ATTRIBUTES,
                                                                                     request_uuids=request_uuids):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Node[{self._type_name}].is_mergeable_with(...): "
                                            "writing attributes without write_attributes permission is not allowed")
            return False
        if not Node.are_mergeable(list_a=self._child_nodes, list_b=other._child_nodes,
                                  overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                  request_uuids=request_uuids, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Node[{self._type_name}].is_mergeable_with(...): child_nodes are not mergeable")
            return False
        merged_child_nodes = Node.merge_many(list_a=self._child_nodes, list_b=other._child_nodes,
                                             overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids)
        if self._child_nodes != merged_child_nodes and not Permissions.is_allowed_with(permissions=self._permissions, action=Action.WRITE_CHILD_NODES,
                                                                                       request_uuids=request_uuids):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Node[{self._type_name}].is_mergeable_with(...): "
                                            "writing child_nodes without write_child_nodes permission is not allowed")
            return False
        if not Permissions.are_mergeable(permissions_a=self._permissions, permissions_b=other._permissions, overwrite=overwrite_permissions,
                                         explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Node[{self._type_name}].is_mergeable_with(...): permissions are not mergeable")
            return False
        merged_permissions = Permissions.merge(permissions_a=self._permissions, permissions_b=other._permissions, overwrite=overwrite_permissions)
        if self._permissions != merged_permissions and not Permissions.is_allowed_with(permissions=self._permissions, action=Action.WRITE_PERMISSIONS,
                                                                                       request_uuids=request_uuids):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Node[{self._type_name}].is_mergeable_with(...): "
                                            "writing permissions without write_permissions permission is not allowed")
            return False
        return True

    def merge_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=set()):
        explanation = Explanation()
        if not self.is_mergeable_with(other=other, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                      request_uuids=request_uuids, explanation=explanation):
            raise MergeException(f"cannot merge nodes that are not mergeable; self: {self} other: {other} explanation: {explanation}")
        merged = self.copy()
        merged._attributes = Attribute.merge_many(attribute_list_a=self._attributes, attribute_list_b=other._attributes,
                                                  overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                                  request_uuids=request_uuids)
        merged._child_nodes = Node.merge_many(list_a=self._child_nodes, list_b=other._child_nodes,
                                              overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                              request_uuids=request_uuids)
        for index, tmp_child_node in enumerate(merged._child_nodes if merged._child_nodes is not None else []):
            tmp_child_node._list_index = index if 1 < len(merged._child_nodes) else -1
        merged._list_index = -1
        merged._permissions = Permissions.merge(permissions_a=self._permissions, permissions_b=other._permissions, overwrite=overwrite_permissions)
        return merged

    def get_attribute(self, index=-1, key=None, value=None, default=None):
        if index < 0 and key is None and value is None:
            return default
        for tmp_index, tmp_attribute in enumerate(self._attributes if self._attributes is not None else []):
            if (index < 0 or index == tmp_index) and (key is None or key == tmp_attribute.get_key()) and (value is None or value == tmp_attribute.get_value()):
                return tmp_attribute
        return default

    def add_attribute(self, attribute, index=-1):
        if attribute is None:
            raise Exception("attribute is none")
        if self.get_attribute(index=index, key=attribute.get_key(), value=attribute.get_value()) is not None:
            raise Exception("duplicate attributes not allowed")
        if self._attributes is None:
            self._attributes = []
        if Attribute.check_list(attribute_list=self._attributes, check_data=None):
            raise Exception("node may not have list of attributes with multiple null keys")
        if index < 0:
            index = len(self._attributes)
        self._attributes.insert(index, attribute)

    def remove_attribute(self, index=-1, key=None, value=None):
        if index < 0 and key is None and value is None:
            raise Exception("attribute not found")
        for tmp_index, tmp_attribute in enumerate(self._attributes if self._attributes is not None else []):
            if (index < 0 or index == tmp_index) and (key is None or key == tmp_attribute.get_key()) and (value is None or value == tmp_attribute.get_value()):
                del self._attributes[tmp_index]
                return
        raise Exception("attribute not found")

    def num_child_nodes(self):
        if self._child_nodes is None:
            return 0
        return len(self._child_nodes)

    def get_child_nodes(self, index=-1, attributes_map=None):
        if index < 0 and attributes_map is None:
            return [child_node for child_node in self._child_nodes] if self._child_nodes is not None else []
        child_nodes = []
        for tmp_index, tmp_child_node in enumerate(self._child_nodes if self._child_nodes is not None else []):
            if (index < 0 or index == tmp_index) and (attributes_map is None or Node.attributes_list_matches_map(
                    attributes_list=tmp_child_node.get_attributes(), attributes_map=attributes_map)):
                child_nodes.append(tmp_child_node)
        return child_nodes

    def get_child_node(self, index=-1, attributes_map=None):
        if index < 0 and attributes_map is None:
            return None
        child_nodes = self.get_child_nodes(index=index, attributes_map=attributes_map)
        return child_nodes[0] if len(child_nodes) != 0 else None

    def add_child_node(self, child_node, index=-1):
        if child_node is None:
            raise Exception("child_node is none")
        if self.get_child_node(index=index, attributes_map=child_node.get_attributes()) is not None:
            raise Exception("duplicate child_nodes not allowed")
        if self._child_nodes is None:
            self._child_nodes = []
        if index < 0:
            index = len(self._child_nodes)
        self._child_nodes.insert(index, child_node)
        for index, tmp_child_node in enumerate(self._child_nodes if self._child_nodes is not None else []):
            tmp_child_node._list_index = index if 1 < len(self._child_nodes) else -1

    def remove_child_nodes(self, index=-1, attributes_map=None):
        child_nodes = self._child_nodes if self._child_nodes is not None else []
        for tmp_index in range(len(child_nodes) - 1, -1, -1):
            tmp_child_node = child_nodes[tmp_index]
            if (index < 0 or index == tmp_index) and (attributes_map is None or Node.attributes_list_matches_map(
                    attributes_list=tmp_child_node.get_attributes(), attributes_map=attributes_map)):
                del child_nodes[tmp_index]
        for tmp_index, tmp_child_node in enumerate(self._child_nodes if self._child_nodes is not None else []):
            tmp_child_node._list_index = tmp_index if 1 < len(self._child_nodes) else -1

    def remove_child_node(self, index=-1, attributes_map=None):
        if index < 0 and attributes_map is None:
            raise Exception("child_node not found")
        for tmp_index, tmp_child_node in enumerate(self._child_nodes if self._child_nodes is not None else []):
            if (index < 0 or index == tmp_index) and (attributes_map is None or Node.attributes_list_matches_map(
                    attributes_list=tmp_child_node.get_attributes(), attributes_map=attributes_map)):
                del self._child_nodes[tmp_index]
                for tmp_index_2, tmp_child_node_2 in enumerate(self._child_nodes if self._child_nodes is not None else []):
                    tmp_child_node_2._list_index = tmp_index_2 if 1 < len(self._child_nodes) else -1
                return
        raise Exception("child_node not found")
