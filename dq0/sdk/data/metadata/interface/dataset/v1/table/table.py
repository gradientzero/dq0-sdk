from dq0.sdk.data.metadata.interface.dataset.entity import Entity
from dq0.sdk.data.metadata.interface.dataset.v1.column.column import Column
from dq0.sdk.data.metadata.interface.dataset.v1.table.attributes_table_data import AttributesTableData
from dq0.sdk.data.metadata.interface.dataset.v1.table.attributes_table_differential_privacy import AttributesTableDifferentialPrivacy
from dq0.sdk.data.metadata.interface.dataset.v1.table.attributes_table_private_sql import AttributesTablePrivateSql
from dq0.sdk.data.metadata.interface.dataset.v1.table.attributes_table_private_synthesis import AttributesTablePrivateSynthesis
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class Table(Entity):
    def __init__(self, name, parent, permissions=None, data_permissions=None, name_permissions=None, role_uuids=None, node=None):
        super().__init__(name=name, type_name=NodeType.TYPE_NAME_TABLE, parent=parent,
                         permissions=permissions, data_permissions=data_permissions, name_permissions=name_permissions,
                         create_child_entity_func=self.create_child_entity, create_attributes_group_func=self.create_attributes_group,
                         role_uuids=role_uuids, node=node)

    def create_attributes_group(self, key, attribute_list=None):
        if key == 'data':
            return AttributesTableData(table=self, attribute_list=attribute_list)
        elif key == 'differential_privacy':
            return AttributesTableDifferentialPrivacy(table=self, attribute_list=attribute_list)
        elif key == 'private_sql':
            return AttributesTablePrivateSql(table=self, attribute_list=attribute_list)
        elif key == 'private_synthesis':
            return AttributesTablePrivateSynthesis(table=self, attribute_list=attribute_list)
        else:
            raise Exception(f"key {key} is invalid")

    def create_child_entity(self, name, child_node):
        return Column(name=name, parent=self,
                      permissions=DefaultPermissions.shared_node(role_uuids=self.role_uuids),
                      data_permissions=DefaultPermissions.shared_attribute(role_uuids=self.role_uuids),
                      name_permissions=DefaultPermissions.shared_attribute(role_uuids=self.role_uuids),
                      role_uuids=self.role_uuids, node=child_node)

    # data
    @property
    def data(self):
        return super().get_attribute_group(key='data')

    @data.setter
    def data(self, _):
        raise Exception("data attribute group may not be set")

    @data.deleter
    def data(self):
        super().get_attribute_group(key='data').delete()

    # differential_privacy
    @property
    def differential_privacy(self):
        return super().get_attribute_group(key='differential_privacy')

    @differential_privacy.setter
    def differential_privacy(self, _):
        raise Exception("differential_privacy attribute group may not be set")

    @differential_privacy.deleter
    def differential_privacy(self):
        super().get_attribute_group(key='differential_privacy').delete()

    # private_sql
    @property
    def private_sql(self):
        return super().get_attribute_group(key='private_sql')

    @private_sql.setter
    def private_sql(self, _):
        raise Exception("private_sql attribute group may not be set")

    @private_sql.deleter
    def private_sql(self):
        super().get_attribute_group(key='private_sql').delete()

    # private_synthesis
    @property
    def private_synthesis(self):
        return super().get_attribute_group(key='private_synthesis')

    @private_synthesis.setter
    def private_synthesis(self, _):
        raise Exception("private_synthesis attribute group may not be set")

    @private_synthesis.deleter
    def private_synthesis(self):
        super().get_attribute_group(key='private_synthesis').delete()

    # column
    def column_names(self):
        return super().get_child_names()

    def column(self, name=None, index=-1):
        return super().get_child_entity(name=name, index=index)

    def drop_column(self, name=None, index=-1):
        return super().remove_child_node(name=name, index=index)

    def drop_columns(self, attributes_map=None):
        return super().remove_child_nodes(attributes_map=attributes_map)
