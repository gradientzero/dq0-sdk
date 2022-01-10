from dq0.sdk.data.metadata.interface.dataset.entity import Entity
from dq0.sdk.data.metadata.interface.dataset.v1.database.database import Database
from dq0.sdk.data.metadata.interface.dataset.v1.dataset.attributes_dataset_data import AttributesDatasetData
from dq0.sdk.data.metadata.interface.dataset.v1.dataset.attributes_dataset_differential_privacy import AttributesDatasetDifferentialPrivacy
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class Dataset(Entity):
    def __init__(self, name, parent, permissions=None, data_permissions=None, name_permissions=None, role_uuids=None, node=None):
        super().__init__(name=name, type_name=NodeType.TYPE_NAME_SCHEMA, parent=parent,
                         permissions=permissions, data_permissions=data_permissions, name_permissions=name_permissions,
                         create_child_entity_func=self.create_child_entity, create_attributes_group_func=self.create_attributes_group,
                         role_uuids=role_uuids, node=node)

    def create_attributes_group(self, key, attribute_list=None):
        if key == 'data':
            return AttributesDatasetData(schema=self, attribute_list=attribute_list)
        elif key == 'differential_privacy':
            return AttributesDatasetDifferentialPrivacy(schema=self, attribute_list=attribute_list)
        else:
            raise Exception(f"key {key} is invalid")

    def create_child_entity(self, name, child_node):
        return Database(name=name, parent=self,
                        permissions=DefaultPermissions.shared_node(role_uuids=self.role_uuids),
                        data_permissions=DefaultPermissions.shared_attribute(role_uuids=self.role_uuids),
                        name_permissions=DefaultPermissions.shared_attribute(role_uuids=self.role_uuids),
                        role_uuids=self.role_uuids, node=child_node)

    def data(self):
        return super().get_attribute_group(key='data')

    def differential_privacy(self):
        return super().get_attribute_group(key='differential_privacy')

    def databases(self):
        return super().get_child_names()

    def database(self, name=None, index=-1):
        return super().get_child_entity(name=name, index=index)
