from dq0.sdk.data.metadata.interface.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class AttributesRunData(AttributesGroup):
    def __init__(self, run, attribute_list=None):
        super().__init__(key='data',
                         permissions=DefaultPermissions.analyst_attribute(role_uuids=run.get_role_uuids()),
                         entity=run,
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
                                 permissions=DefaultPermissions.analyst_attribute(role_uuids=self.get_role_uuids()))

    @description.deleter
    def description(self):
        self.delete_attribute(key='description')

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
                                 permissions=DefaultPermissions.analyst_attribute(role_uuids=self.get_role_uuids()))
        self.get_entity().set_name(old_name=old_name, new_name=new_name)

    @name.deleter
    def name(self):
        raise Exception("name may not be deleted")

    # type_name
    @property
    def type_name(self):
        return self.get_attribute_value(key='type_name')

    @type_name.setter
    def type_name(self, new_type_name):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='type_name',
                                 value=new_type_name,
                                 permissions=DefaultPermissions.analyst_attribute(role_uuids=self.get_role_uuids()),
                                 allow_modification=False)

    @type_name.deleter
    def type_name(self):
        raise Exception(f"type_name {self.type_name} may not be deleted")
