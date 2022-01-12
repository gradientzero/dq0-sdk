from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.attribute.attribute_string import AttributeString
from dq0.sdk.data.metadata.node.node import Node
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.permissions.permissions import Permissions
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class Entity:
    @staticmethod
    def check_and_get(type_name, node=None, permissions=None, data_permissions=None, name_permissions=None):
        if node is not None:
            if not isinstance(node, Node):
                raise Exception(f"node is not of type Node, is of type {type(node)} instead")
            if node.get_type_name() != type_name:
                raise Exception(f"node must have type_name {type_name}, has {node.get_type_name()} instead")
            permissions = node.get_permissions()
            data_attribute = node.get_attribute(key='data')
            if data_attribute is not None:
                if not isinstance(data_attribute, AttributeList):
                    raise Exception(f"data_attribute is not of type AttributeList, is of type {type(data_attribute)} instead")
                data_permissions = data_attribute.get_permissions()
                name_attribute = data_attribute.get_attribute(key='name')
                if name_attribute is not None:
                    if not isinstance(name_attribute, AttributeString):
                        raise Exception(f"name_attribute is not of type AttributeString, is of type {type(name_attribute)} instead")
                    name_permissions = name_attribute.get_permissions()
        Permissions.check(permissions=permissions)
        Permissions.check(permissions=data_permissions)
        Permissions.check(permissions=name_permissions)
        return permissions, data_permissions, name_permissions

    @staticmethod
    def name_of(node):
        if not isinstance(node, Node):
            raise Exception(f"node is not of type Node, is of type {type(node)} instead")
        data_attribute = node.get_attribute(key='data')
        if not isinstance(data_attribute, AttributeList):
            raise Exception(f"data_attribute is not of type AttributeList, is of type {type(data_attribute)} instead")
        name_attribute = data_attribute.get_attribute(key='name')
        if not isinstance(name_attribute, AttributeString):
            raise Exception(f"name_attribute is not of type AttributeString, is of type {type(name_attribute)} instead")
        name = name_attribute.get_value()
        if not isinstance(name, str):
            raise Exception(f"name is not of type str, is of type {type(name)} instead")
        return name

    def __init__(self, name, type_name, parent, permissions=None, data_permissions=None, name_permissions=None,
                 create_child_entity_func=None, create_attributes_group_func=None, role_uuids=None, node=None):
        if not isinstance(name, str):
            raise Exception(f"name is not of type str, is of type {type(name)} instead")
        if node is not None and not NodeType.is_valid_type_name(type_name=type_name):
            raise Exception(f"type_name {type_name} is invalid")
        if not isinstance(parent, Entity):
            raise Exception(f"parent is not of type Entity, is of type {type(parent)} instead")
        DefaultPermissions.check_role_uuids(role_uuids=role_uuids)
        self._permissions, self._data_permissions, self._name_permissions = Entity.check_and_get(
            type_name=type_name, node=node, permissions=permissions, data_permissions=data_permissions, name_permissions=name_permissions)
        self._name = name
        self._type_name = type_name
        self._parent = parent
        self._create_child_entity_func = create_child_entity_func
        self._create_attributes_group_func = create_attributes_group_func
        self._role_uuids = role_uuids
        self._node = node
        self._attribute_groups = {}
        self._child_entities = {}

    def __len__(self):
        return self.get_node().num_child_nodes() if self.get_node() is not None else 0

    def get_role_uuids(self):
        return self._role_uuids

    def get_node(self):
        return self._node

    def create(self):
        if self.get_node() is not None:
            return
        self._node = Node(type_name=self._type_name, attributes=[
            AttributeList(key='data', value=[
                AttributeString(key='name', value=self._name, permissions=self._name_permissions)
            ], permissions=self._data_permissions)
        ], child_nodes=None, permissions=self._permissions)
        self._parent.add_child_node(node=self._node)

    def delete(self):
        if self.get_node() is None:
            return
        self._parent.remove_child_node(name=self._name)
        self.wipe()

    def wipe(self):
        self._node = None
        for attribute_group in self._attribute_groups.values():
            attribute_group.wipe()
        for child_entity in self._child_entities.values():
            child_entity.wipe()

    def get_child_entity(self, name=None, index=-1):
        if name is None and index < 0:
            index = 0
        if name is None:
            child_node = self.get_node().get_child_node(index=index) if self.get_node() is not None else None
            if child_node is None:
                raise Exception("index based get may only work for existing child nodes")
            name = Entity.name_of(node=child_node)
        else:
            child_node = self.get_node().get_child_node(attributes_map={'data': {'name': name}}) if self.get_node() is not None else None
        if name not in self._child_entities:
            if self._create_child_entity_func is None:
                raise Exception("create_child_entity_func is None")
            self._child_entities[name] = self._create_child_entity_func(name=name, child_node=child_node)
        return self._child_entities[name]

    def add_child_node(self, child_node):
        self.create()
        self.get_node().add_child_node(child_node=child_node)

    def remove_child_node(self, name=None, index=-1):
        if self.get_node() is None:
            return
        if name is None:
            if index < 0:
                index = 0
            child_node = self.get_node().get_child_node(index=index)
            if child_node is None:
                return
            name = Entity.name_of(node=child_node)
        self.get_node().remove_child_node(index=index, attributes_map={'data': {'name': name}})
        if name in self._child_entities:
            self._child_entities[name].wipe()

    def remove_child_nodes(self, attributes_map=None):
        if self.get_node() is None:
            return
        child_nodes = self.get_node().get_child_nodes(attributes_map=attributes_map)
        for child_node in child_nodes:
            self.remove_child_node(name=Entity.name_of(child_node))

    def get_attribute_group(self, key):
        if key not in self._attribute_groups:
            attribute_list = self.get_node().get_attribute(key=key) if self.get_node() is not None else None
            if self._create_attributes_group_func is None:
                raise Exception("create_attributes_group_func is None")
            self._attribute_groups[key] = self._create_attributes_group_func(key=key, attribute_list=attribute_list)
        return self._attribute_groups[key]

    def get_name(self):
        return self._name

    def set_name(self, old_name, new_name):
        if not isinstance(old_name, str):
            raise Exception(f"old_name {old_name} is not of type str, is of type {type(old_name)} instead")
        if not isinstance(new_name, str):
            raise Exception(f"new_name {new_name} is not of type str, is of type {type(new_name)} instead")
        if self.get_name() != old_name:
            raise Exception(f"name mismatch: {self.get_name()} != {old_name}")
        self._name = new_name
        self._parent.set_child_name(old_name=old_name, new_name=new_name)

    def set_child_name(self, old_name, new_name):
        if not isinstance(old_name, str):
            raise Exception(f"old_name {old_name} is not of type str, is of type {type(old_name)} instead")
        if not isinstance(new_name, str):
            raise Exception(f"new_name {new_name} is not of type str, is of type {type(new_name)} instead")
        if old_name not in self._child_entities:
            raise Exception(f"old_name {old_name} of child entity does not exist")
        if old_name == new_name:
            return
        if new_name in self._child_entities:
            raise Exception(f"new_name {new_name} of child entity already exists")
        self._child_entities[new_name] = self._child_entities[old_name]
        del self._child_entities[old_name]

    def get_child_names(self):
        child_names = set()
        for child_node in self.get_node().get_child_nodes() if self.get_node() is not None else []:
            child_names.add(Entity.name_of(node=child_node))
        if len(child_names) != self.get_node().num_child_nodes():
            raise Exception(f"length mismatch; child_names are not unique: {len(child_names)} != {len(self.get_node().num_child_nodes())}")
        return child_names

    def add_attribute(self, attribute):
        self.create()
        self.get_node().add_attribute(attribute=attribute)

    def remove_attribute(self, key):
        if self.get_node() is None:
            return
        self.get_node().remove_attribute(key=key)
        if key in self._attribute_groups:
            self._attribute_groups[key].wipe()
