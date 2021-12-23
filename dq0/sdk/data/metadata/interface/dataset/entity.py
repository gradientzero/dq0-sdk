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
            if node.type_name != type_name:
                raise Exception(f"node must have type_name {type_name}, has {node.type_name} instead")
            permissions = node.permissions
            data_attribute = node.get_attribute(key='data')
            if data_attribute is not None:
                if not isinstance(data_attribute, AttributeList):
                    raise Exception(f"data_attribute is not of type AttributeList, is of type {type(data_attribute)} instead")
                data_permissions = data_attribute.permissions
                name_attribute = data_attribute.get_attribute(key='name')
                if name_attribute is not None:
                    if not name_attribute(data_attribute, AttributeString):
                        raise Exception(f"data_attribute is not of type AttributeList, is of type {type(data_attribute)} instead")
                    name_permissions = name_attribute.permissions
        Permissions.check(permissions=permissions)
        Permissions.check(permissions=data_permissions)
        Permissions.check(permissions=name_permissions)
        return permissions, data_permissions, name_permissions

    def __init__(self, name, type_name, parent, permissions=None, data_permissions=None, name_permissions=None,
                 create_child_entity_func=None, create_attributes_group_func=None, role_uuids=None, node=None):
        if not isinstance(name, str):
            raise Exception(f"name is not of type str, is of type {type(name)} instead")
        if not NodeType.is_valid_type_name(type_name=type_name):
            raise Exception(f"type_name {type_name} is invalid")
        if not isinstance(parent, Entity):
            raise Exception(f"parent is not of type Entity, is of type {type(parent)} instead")
        DefaultPermissions.check_role_uuids(role_uuids=role_uuids)
        self.permissions, self.data_permissions, self.name_permissions = Entity.check_and_get(
            type_name=type_name, node=node, permissions=permissions, data_permissions=data_permissions, name_permissions=name_permissions)
        self.name = name
        self.type_name = type_name
        self.parent = parent
        self.create_child_entity_func = create_child_entity_func
        self.create_attributes_group_func = create_attributes_group_func
        self.role_uuids = role_uuids
        self.node = node
        self.attribute_groups = {}
        self.child_entities = {}

    def create(self):
        if self.node is not None:
            return
        self.node = Node(type_name=self.type_name, attributes=[
            AttributeList(key='data', value=[
                AttributeString(key='name', value=self.name, permissions=self.name_permissions)
            ], permissions=self.data_permissions)
        ], child_nodes=None, permissions=self.permissions)
        self.parent.add_child_node(node=self.node)

    def delete(self):
        if self.node is None:
            return
        self.parent.remove_child_node(name=self.name)
        self.wipe()

    def wipe(self):
        self.node = None
        for attribute_group in self.attribute_groups.values():
            attribute_group.wipe()
        for child_entity in self.child_entities.values():
            child_entity.wipe()

    def get_child_entity(self, name):
        if name not in self.child_entities:
            child_node = self.node.get_child_node(attributes_map={'data': {'name': name}}) if self.node is not None else None
            if self.create_child_entity_func is None:
                raise Exception("create_child_entity_func is None")
            self.child_entities[name] = self.create_child_entity_func(name=name, child_node=child_node)
        return self.child_entities[name]

    def add_child_node(self, child_node):
        self.create()
        self.node.add_child_node(child_node=child_node)

    def remove_child_node(self, name):
        if self.node is None:
            return
        self.node.remove_child_node(attributes_map={'data': {'name': name}})
        if name in self.child_entities:
            self.child_entities[name].wipe()

    def get_attribute_group(self, key):
        if key not in self.attribute_groups:
            attribute_list = self.node.get_attribute(key=key) if self.node is not None else None
            if self.create_attributes_group_func is None:
                raise Exception("create_attributes_group_func is None")
            self.attribute_groups[key] = self.create_attributes_group_func(key=key, attribute_list=attribute_list)
        return self.attribute_groups[key]

    def set_name(self, old_name, new_name):
        if not isinstance(old_name, str):
            raise Exception(f"old_name {old_name} is not of type str, is of type {type(old_name)} instead")
        if not isinstance(new_name, str):
            raise Exception(f"new_name {new_name} is not of type str, is of type {type(new_name)} instead")
        if self.name != old_name:
            raise Exception(f"name mismatch: {self.name} != {old_name}")
        self.name = new_name
        self.parent.set_child_name(old_name=old_name, new_name=new_name)

    def set_child_name(self, old_name, new_name):
        if not isinstance(old_name, str):
            raise Exception(f"old_name {old_name} is not of type str, is of type {type(old_name)} instead")
        if not isinstance(new_name, str):
            raise Exception(f"new_name {new_name} is not of type str, is of type {type(new_name)} instead")
        if old_name not in self.child_entities:
            raise Exception(f"old_name {old_name} of child entity does not exist")
        if old_name == new_name:
            return
        if new_name in self.child_entities:
            raise Exception(f"new_name {new_name} of child entity already exists")
        self.child_entities[new_name] = self.child_entities[old_name]
        del self.child_entities[old_name]

    def add_attribute(self, attribute):
        self.create()
        self.node.add_attribute(attribute=attribute)

    def remove_attribute(self, key):
        if self.node is None:
            return
        self.node.remove_attribute(key=key)
        if key in self.attribute_groups:
            self.attribute_groups[key].wipe()
