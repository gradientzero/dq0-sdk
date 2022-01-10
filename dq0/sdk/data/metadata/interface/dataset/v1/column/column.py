from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.attribute.attribute_string import AttributeString
from dq0.sdk.data.metadata.interface.dataset.entity import Entity
from dq0.sdk.data.metadata.interface.dataset.v1.column.attributes_column_data import AttributesColumnData
from dq0.sdk.data.metadata.interface.dataset.v1.column.attributes_column_machine_learning import AttributesColumnMachineLearning
from dq0.sdk.data.metadata.interface.dataset.v1.column.attributes_column_private_sql import AttributesColumnPrivateSql
from dq0.sdk.data.metadata.interface.dataset.v1.column.attributes_column_private_sql_and_synthesis import AttributesColumnPrivateSqlAndSynthesis
from dq0.sdk.data.metadata.node.node import Node
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.permissions.permissions import Permissions
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class Column(Entity):
    @staticmethod
    def check_data_type_name(data_type_name):
        if data_type_name not in ['boolean', 'datetime', 'float', 'int', 'string']:
            raise Exception(f"unknown data_type_name {data_type_name}")

    def __init__(self, name, parent, permissions=None, data_permissions=None, name_permissions=None, role_uuids=None, node=None):
        super().__init__(name=name, type_name=NodeType.TYPE_NAME_COLUMN, parent=parent,
                         permissions=permissions, data_permissions=data_permissions, name_permissions=name_permissions,
                         create_child_entity_func=None, create_attributes_group_func=self.create_attributes_group, role_uuids=role_uuids, node=node)
        data_attribute = node.get_attribute(key='data') if isinstance(node, Node) else None
        data_type_name_attribute = data_attribute.get_attribute(key='data_type_name') if isinstance(data_attribute, AttributeList) else None
        data_type_name = data_type_name_attribute.value if data_type_name_attribute is not None else None
        data_type_name_permissions = data_type_name_attribute.permissions if data_type_name_attribute is not None else None
        if data_type_name is not None:
            Column.check_data_type_name(data_type_name=data_type_name)
        elif node is not None:
            raise Exception("if node is not none, data_type_name cannot be none")
        self.data_type_name = data_type_name
        self.data_type_name_permissions = data_type_name_permissions

    def set_data_type_name(self, data_type_name, data_type_name_permissions=None):
        Column.check_data_type_name(data_type_name=data_type_name)
        Permissions.check(permissions=data_type_name_permissions)
        self.data_type_name = data_type_name
        self.data_type_name_permissions = data_type_name_permissions

    def create(self):
        if self.node is not None:
            return
        Column.check_data_type_name(data_type_name=self.data_type_name)
        if self.data_type_name_permissions is None:
            self.data_type_name_permissions = DefaultPermissions.shared_attribute(role_uuids=self.role_uuids)
        super().create()
        if not isinstance(self.node, Node):
            raise Exception(f"self.node is not of type Node, is of type {type(self.node)} instead")
        data_attribute = self.node.get_attribute(key='data')
        if not isinstance(data_attribute, AttributeList):
            raise Exception(f"data_attribute is not of type AttributeList, is of type {type(data_attribute)} instead")
        data_type_name_attribute = data_attribute.get_attribute(key='data_type_name')
        if data_type_name_attribute is not None:
            raise Exception("data_type_name_attribute must be none at this point")
        data_type_name_attribute = AttributeString(key='data_type_name', value=self.data_type_name, permissions=self.data_type_name_permissions)
        data_attribute.add_attribute(attribute=data_type_name_attribute)

    def create_attributes_group(self, key, attribute_list=None):
        if key == 'data':
            return AttributesColumnData(column=self, attribute_list=attribute_list)
        elif key == 'machine_learning':
            return AttributesColumnMachineLearning(column=self, attribute_list=attribute_list)
        elif key == 'private_sql':
            if self.data_type_name is None:
                raise Exception("cannot access private_sql without data_type_name being set")
            return AttributesColumnPrivateSql(column=self, attribute_list=attribute_list)
        elif key == 'private_sql_and_synthesis':
            if self.data_type_name is None:
                raise Exception("cannot access private_sql_and_synthesis without data_type_name being set")
            if self.data_type_name == 'boolean':
                raise Exception("attribute group private_sql_and_synthesis not allowed for boolean column")
            return AttributesColumnPrivateSqlAndSynthesis(column=self, attribute_list=attribute_list)
        elif key == 'private_synthesis':
            if self.data_type_name is None:
                raise Exception("cannot access private_synthesis without data_type_name being set")
            return AttributesColumnPrivateSql(column=self, attribute_list=attribute_list)
        else:
            raise Exception(f"key {key} is invalid")

    def data(self):
        return super().get_attribute_group(key='data')

    def machine_learning(self):
        return super().get_attribute_group(key='machine_learning')

    def private_sql(self):
        return super().get_attribute_group(key='private_sql')

    def private_sql_and_synthesis(self):
        return super().get_attribute_group(key='private_sql_and_synthesis')

    def private_synthesis(self):
        return super().get_attribute_group(key='private_synthesis')
