from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.interface.dataset.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class AttributesColumnPrivateSql(AttributesGroup):
    def __init__(self, column, data_type_name, attribute_list=None, role_uuids=None):
        super().__init__(key='private_sql',
                         permissions=DefaultPermissions.owner_attribute(role_uuids=role_uuids),
                         column=column,
                         attribute_list=attribute_list)
        if data_type_name not in ['boolean', 'datetime', 'float', 'int', 'string']:
            raise Exception(f"unknown data_type_name {data_type_name}")
        DefaultPermissions.check_role_uuids(role_uuids=role_uuids)
        self.data_type_name = data_type_name
        self.role_uuids = role_uuids

    # allowed_values
    @property
    def allowed_values(self):
        return self.get_attribute_value(key='allowed_values')

    @allowed_values.setter
    def allowed_values(self, new_allowed_values):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_LIST,
                                 key='allowed_values',
                                 value=new_allowed_values,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.role_uuids))

    @allowed_values.deleter
    def allowed_values(self):
        self.delete_attribute(key='allowed_values')
