from dq0.sdk.data.metadata.interface.dataset.entity import Entity
from dq0.sdk.data.metadata.interface.dataset.v1.database.database import Database
from dq0.sdk.data.metadata.interface.dataset.v1.dataset.attributes_dataset_data import AttributesDatasetData
from dq0.sdk.data.metadata.interface.dataset.v1.dataset.attributes_dataset_differential_privacy import AttributesDatasetDifferentialPrivacy
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.structure.node.node_type import NodeType


class Dataset(Entity):
    def __init__(self, name, parent, permissions=None, data_permissions=None, name_permissions=None, role_uuids=None, node=None):
        super().__init__(name=name, type_name=NodeType.TYPE_NAME_DATASET, parent=parent,
                         permissions=permissions, data_permissions=data_permissions, name_permissions=name_permissions,
                         create_child_entity_func=self.create_child_entity, create_attributes_group_func=self.create_attributes_group,
                         role_uuids=role_uuids, node=node)

    def create_attributes_group(self, key, attribute_list=None):
        if key == 'data':
            return AttributesDatasetData(dataset=self, attribute_list=attribute_list)
        elif key == 'differential_privacy':
            return AttributesDatasetDifferentialPrivacy(dataset=self, attribute_list=attribute_list)
        else:
            raise Exception(f"key {key} is invalid")

    def create_child_entity(self, name, child_node):
        return Database(name=name, parent=self,
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

    # database
    def database_names(self):
        return super().get_child_names()

    def database(self, name=None, index=-1):
        return super().get_child_entity(name=name, index=index)

    def drop_database(self, name=None, index=-1):
        return super().remove_child_node(name=name, index=index)

    def drop_databases(self, attributes_map=None):
        return super().remove_child_nodes(attributes_map=attributes_map)
