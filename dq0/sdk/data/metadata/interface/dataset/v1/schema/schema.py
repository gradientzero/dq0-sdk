from dq0.sdk.data.metadata.interface.dataset.entity import Entity
from dq0.sdk.data.metadata.interface.dataset.v1.schema.attributes_schema_data import AttributesSchemaData
from dq0.sdk.data.metadata.interface.dataset.v1.schema.attributes_schema_differential_privacy import AttributesSchemaDifferentialPrivacy
from dq0.sdk.data.metadata.interface.dataset.v1.table.table import Table
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class Schema(Entity):
    def __init__(self, name, parent, permissions=None, data_permissions=None, name_permissions=None, role_uuids=None, node=None):
        super().__init__(name=name, type_name=NodeType.TYPE_NAME_SCHEMA, parent=parent,
                         permissions=permissions, data_permissions=data_permissions, name_permissions=name_permissions,
                         create_child_entity_func=self.create_child_entity, create_attributes_group_func=self.create_attributes_group,
                         role_uuids=role_uuids, node=node)

    def create_attributes_group(self, key, attribute_list=None):
        if key == 'data':
            return AttributesSchemaData(schema=self, attribute_list=attribute_list)
        elif key == 'differential_privacy':
            return AttributesSchemaDifferentialPrivacy(schema=self, attribute_list=attribute_list)
        else:
            raise Exception(f"key {key} is invalid")

    def create_child_entity(self, name, child_node):
        return Table(name=name, parent=self,
                     permissions=DefaultPermissions.shared_node(role_uuids=self.get_role_uuids()),
                     data_permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()),
                     name_permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()),
                     role_uuids=self.get_role_uuids(), node=child_node)

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

    # table
    def table_names(self):
        return super().get_child_names()

    def table(self, name=None, index=-1):
        return super().get_child_entity(name=name, index=index)

    def drop_table(self, name=None, index=-1):
        return super().remove_child_node(name=name, index=index)

    def drop_tables(self, attributes_map=None):
        return super().remove_child_nodes(attributes_map=attributes_map)
