from dq0.sdk.data.metadata.interface.dataset.attribute_utils import AttributeUtils
from dq0.sdk.data.metadata.interface.dataset.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class AttributesDatasetData(AttributesGroup):
    def __init__(self, dataset, attribute_list=None):
        super().__init__(key='data',
                         permissions=DefaultPermissions.shared_attribute(role_uuids=dataset.get_role_uuids()),
                         entity=dataset,
                         attribute_list=attribute_list)

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
        raise Exception("name may not be deleted")

    # tags
    @property
    def tags(self):
        return AttributeUtils.value_to_list(input_value=self.get_attribute_value(key='tags'))

    @tags.setter
    def tags(self, new_tags):
        shared_permissions = DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids())
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_LIST,
                                 key='tags',
                                 value=AttributeUtils.list_to_value(input_list=new_tags,
                                                                    type_name=AttributeType.TYPE_NAME_STRING,
                                                                    permissions=shared_permissions),
                                 permissions=shared_permissions)

    @tags.deleter
    def tags(self):
        self.delete_attribute(key='tags')
