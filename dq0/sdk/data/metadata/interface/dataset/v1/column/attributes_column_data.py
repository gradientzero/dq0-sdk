from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.interface.dataset.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class AttributesColumnData(AttributesGroup):
    def __init__(self, column, attribute_list=None):
        super().__init__(key='data',
                         permissions=DefaultPermissions.shared_attribute(role_uuids=column.get_role_uuids()),
                         entity=column,
                         attribute_list=attribute_list)

    # data_type_name
    @property
    def data_type_name(self):
        return self.get_attribute_value(key='data_type_name')

    @data_type_name.setter
    def data_type_name(self, _):
        raise Exception(f"data_type_name {self.data_type_name} may not be modified")

    @data_type_name.deleter
    def data_type_name(self):
        raise Exception(f"data_type_name {self.data_type_name} may not be deleted")

    # description
    @property
    def description(self):
        return self.get_attribute_value(key='description')

    @description.setter
    def description(self, new_description):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='description',
                                 value=new_description,
                                 permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()))

    @description.deleter
    def description(self):
        self.delete_attribute(key='description')

    # metadata_is_public
    @property
    def metadata_is_public(self):
        return self.get_attribute_value(key='metadata_is_public')

    @metadata_is_public.setter
    def metadata_is_public(self, new_metadata_is_public):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='metadata_is_public',
                                 value=new_metadata_is_public,
                                 permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()))

    @metadata_is_public.deleter
    def metadata_is_public(self):
        self.delete_attribute(key='metadata_is_public')

    # name
    @property
    def name(self):
        return self.get_attribute_value(key='name')

    @name.setter
    def name(self, new_name):
        old_name = self.get_attribute_value(key='name')
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='name',
                                 value=new_name,
                                 permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()))
        self.get_entity().set_name(old_name=old_name, new_name=new_name)

    @name.deleter
    def name(self):
        raise Exception(f"name {self.name} may not be deleted")

    # selectable
    @property
    def selectable(self):
        return self.get_attribute_value(key='selectable')

    @selectable.setter
    def selectable(self, new_selectable):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='selectable',
                                 value=new_selectable,
                                 permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()))

    @selectable.deleter
    def selectable(self):
        self.delete_attribute(key='selectable')
