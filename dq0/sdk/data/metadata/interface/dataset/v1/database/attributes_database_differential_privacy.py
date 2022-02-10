from dq0.sdk.data.metadata.interface.dataset.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class AttributesDatabaseDifferentialPrivacy(AttributesGroup):
    def __init__(self, database, attribute_list=None):
        super().__init__(key='differential_privacy',
                         permissions=DefaultPermissions.owner_attribute(role_uuids=database.get_role_uuids()),
                         entity=database,
                         attribute_list=attribute_list)

    # privacy_level
    @property
    def privacy_level(self):
        return self.get_attribute_value(key='privacy_level')

    @privacy_level.setter
    def privacy_level(self, new_privacy_level):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_INT,
                                 key='privacy_level',
                                 value=new_privacy_level,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @privacy_level.deleter
    def privacy_level(self):
        self.delete_attribute(key='privacy_level')
