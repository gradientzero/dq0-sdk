from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.merge_exception import MergeException
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.utils import Utils as MetaUtils


class Node:
    @staticmethod
    def init_check_many(list):
        tmp_list = [tmp_elem for tmp_elem in list] if list is not None else []
        while 0 < len(tmp_list):
            elem_a = tmp_list.pop()
            if elem_a is None:
                raise Exception("node cannot be None")
            for elem_b in tmp_list:
                if elem_b is None:
                    raise Exception("node cannot be None")
                try:
                    if elem_a.merge_check_with(other=elem_b):
                        raise Exception("mergeable nodes:\n" + str(elem_a) + "\nand:\n" + str(elem_b) + "\ndetected in:\n" + str(list))
                except: MergeException

    @staticmethod
    def are_merge_compatible(list_a, list_b):
        if list_a is None or len(list_a) == 0:
            return True
        if list_b is None or len(list_b) == 0:
            return True
        for elem_a in list_a:
            for elem_b in list_b:
                if not elem_a.is_merge_compatible_with(other=elem_b):
                    return False
        return True

    @staticmethod
    def are_mergeable(list_a, list_b, overwrite=False):
        if not Node.are_merge_compatible(list_a=list_a, list_b=list_b):
            return False
        if list_a is None or len(list_a) == 0:
            return True
        if list_b is None or len(list_b) == 0:
            return True
        for elem_a in list_a:
            found_match = False
            for elem_b in list_b:
                if elem_a.is_mergeable_with(other=elem_b, overwrite=overwrite):
                    if found_match:
                        return False
                    found_match = True
        return True

    @staticmethod
    def merge_many(list_a, list_b, overwrite=False):
        if not Node.are_mergeable(list_a=list_a, list_b=list_b, overwrite=overwrite):
            raise MergeException(f"cannot merge nodes that are not mergeable; list_a: {list_a} list_b: {list_b}")
        if list_a is None or len(list_a) == 0:
            return None if list_b is None or len(list_b) == 0 else list_b
        if list_b is None or len(list_b) == 0:
            return None if list_a is None or len(list_a) == 0 else list_a
        merged = []
        tmp_list_b = [tmp_elem for tmp_elem in list_b]
        for elem_a in list_a:
            elem_merged = elem_a.copy()
            for elem_b in tmp_list_b:
                if elem_a.is_mergeable_with(other=elem_b, overwrite=overwrite):
                    tmp_list_b.remove(elem_b)
                    elem_merged = elem_a.merge_with(other=elem_b, overwrite=overwrite)
                    break
            merged.append(elem_merged)
        for elem_b in tmp_list_b:
            for elem_a in list_a:
                if elem_a.is_mergeable_with(other=elem_b, overwrite=overwrite):
                    raise Exception("this can never happen")
            merged.append(elem_b.copy())
        return merged

    def __init__(self, type_name, attributes=None, child_nodes=None):
        if not NodeType.isValidTypeName(type_name=type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        Attribute.init_check_many(list=attributes)
        Node.init_check_many(list=child_nodes)
        self.type_name = type_name
        self.attributes = attributes
        self.child_nodes = child_nodes

    def __str__(self):
        return_string = MetaUtils.str_from(object=self.type_name) + ":\n"
        return_string += "   attributes:" + MetaUtils.str_from_list(list=self.attributes).replace('\n', "\n   ") + '\n'
        return_string += "   child_nodes:" + MetaUtils.str_from_list(list=self.child_nodes).replace('\n', "\n   ")
        return return_string

    def __repr__(self):
        return_string = "Node(type_name=" + MetaUtils.repr_from(object=self.type_name) + ", "
        return_string += "attributes=" + MetaUtils.repr_from_list(list=self.attributes) + ", "
        return_string += "child_nodes=" + MetaUtils.repr_from_list(list=self.child_nodes) + ')'
        return return_string

    def copy(self):
        return Node(
            type_name=self.type_name,
            attributes=[tmp_attribute.copy() for tmp_attribute in self.attributes] if self.attributes is not None else None,
            child_nodes=[tmp_child_node.copy() for tmp_child_node in self.child_nodes] if self.child_nodes is not None else None,
            )

    def to_dict(self):
        return {tmp_key: tmp_value for tmp_key, tmp_value in [
            ('type_name', self.type_name),
            ('attributes', [tmp_attribute.to_dict() for tmp_attribute in self.attributes] if self.attributes is not None else None),
            ('child_nodes', [tmp_child_node.to_dict() for tmp_child_node in self.child_nodes] if self.child_nodes is not None else None),
            ] if tmp_value is not None}

    def is_merge_compatible_with(self, other):
        if other is None:
            print(f"other is None <-- Node.is_merge_compatible_with:(self={self} other=None)")
            return False
        if self.type_name != other.type_name:
            print(f"type_names mismatch <-- Node.is_merge_compatible_with:(self={self} other={other})")
            return False
        if not Attribute.are_merge_compatible(list_a=self.attributes, list_b=other.attributes):
            print(f"attributes are not merge compatible <-- Node.is_merge_compatible_with:(self={self} other={other})")
            return False
        if not Node.are_merge_compatible(list_a=self.child_nodes, list_b=other.child_nodes):
            print(f"child_nodes are not merge compatible <-- Node.is_merge_compatible_with:(self={self} other={other})")
            return False
        return True

    def is_mergeable_with(self, other, overwrite=False):
        if not self.is_merge_compatible_with(other=other):
            print(f"self is not merge compatible <-- Node.is_mergeable_with:(self={self} other={other} overwrite={overwrite})")
            return False
        if not Attribute.are_mergeable(list_a=self.attributes, list_b=other.attributes, overwrite=overwrite):
            print(f"attributes are not mergeable <-- Node.is_mergeable_with:(self={self} other={other} overwrite={overwrite})")
            return False
        if not Node.are_mergeable(list_a=self.child_nodes, list_b=other.child_nodes, overwrite=overwrite):
            print(f"child_nodes are not mergeable <-- Node.is_mergeable_with:(self={self} other={other} overwrite={overwrite})")
            return False
        return True

    def merge_with(self, other, overwrite=False):
        if not self.is_mergeable_with(other=other, overwrite=overwrite):
            raise MergeException(f"cannot merge nodes that are not mergeable; self: {self} other: {other}")
        merged = self.copy()
        merged.attributes = Attribute.merge_many(list_a=self.attributes, list_b=other.attributes, overwrite=overwrite)
        merged.child_nodes = Node.merge_many(list_a=self.child_nodes, list_b=other.child_nodes, overwrite=overwrite)
        return merged

    def get_attribute(self, index=-1, key=None, value=None):
        if index < 0 and key is None and value is None:
            return None
        for tmp_index, tmp_attribute in enumerate(self.attributes if self.attributes is not None else []):
            if (index < 0 or index == tmp_index) and (key is None or key == tmp_attribute.key) and (value is None or value == tmp_attribute.value):
                return tmp_attribute
        return None

    def add_attribute(self, attribute, index=-1):
        if attribute is None:
            raise Exception("attribute is none")
        if self.get_attribute(index=index, key=attribute.key, value=attribute.value) is not None:
            raise Exception("duplicate attributes not allowed")
        if self.attributes is None:
            self.attributes = []
        if index < 0:
            index = len(self.attributes)
        self.attributes.insert(index, attribute)

    def remove_attribute(self, index=-1, key=None, value=None):
        if index < 0 and key is None and value is None:
            raise Exception("attribute not found")
        for tmp_index, tmp_attribute in enumerate(self.attributes if self.attributes is not None else []):
            if (index < 0 or index == tmp_index) and (key is None or key == tmp_attribute.key) and (value is None or value == tmp_attribute.value):
                del self.attributes[tmp_index]
                return
        raise Exception("attribute not found")

    def matches_attribute_map(self, attributes_map):
        for tmp_key, tmp_value in attributes_map.items() if attributes_map is not None else {}:
            if self.get_attribute(index=-1, key=tmp_key, value=tmp_value) is None:
                return False
        return True

    def get_child_node(self, index=-1, attributes_map=None):
        if index < 0 and attributes_map is None:
            return None
        for tmp_index, tmp_child_node in enumerate(self.child_nodes if self.child_nodes is not None else []):
            if (index < 0 or index == tmp_index) and (attributes_map is None or tmp_child_node.matches_attribute_map(attributes_map=attributes_map)):
                return tmp_child_node
        return None

    def add_child_node(self, child_node, index=-1):
        if child_node is None:
            raise Exception("child_node is none")
        if self.get_child_node(index=index, attributes_map=child_node.attributes) is not None:
            raise Exception("duplicate child_nodes not allowed")
        if self.child_nodes is None:
            self.child_nodes = []
        if index < 0:
            index = len(self.child_nodes)
        self.child_nodes.insert(index, child_node)

    def remove_child_node(self, index=-1, attributes_map=None):
        if index < 0 and attributes_map is None:
            raise Exception("child_node not found")
        for tmp_index, tmp_child_node in enumerate(self.child_nodes if self.child_nodes is not None else []):
            if (index < 0 or index == tmp_index) and (attributes_map is None or tmp_child_node.matches_attribute_map(attributes_map=attributes_map)):
                del self.child_nodes[tmp_index]
                return
        raise Exception("child_node not found")
