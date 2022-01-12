from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.interface.dataset.attribute_utils import AttributeUtils
from dq0.sdk.data.metadata.interface.dataset.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class AttributesColumnPrivateSql(AttributesGroup):
    def __init__(self, column, attribute_list=None):
        super().__init__(key='private_sql',
                         permissions=DefaultPermissions.owner_attribute(role_uuids=column.get_role_uuids()),
                         entity=column,
                         attribute_list=attribute_list)

    # allowed_values
    @property
    def allowed_values(self):
        return AttributeUtils.value_to_list(input_value=self.get_attribute_value(key='allowed_values'))

    @allowed_values.setter
    def allowed_values(self, new_allowed_values):
        if self.get_entity().get_data_type_name() in ['boolean']:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not allow allowed_values")
        if self.get_entity().get_data_type_name() not in [AttributeType.TYPE_NAME_DATETIME, AttributeType.TYPE_NAME_FLOAT,
                                                          AttributeType.TYPE_NAME_INT, AttributeType.TYPE_NAME_STRING]:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not match any allowed attribute type_name")
        owner_permissions = DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids())
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_LIST,
                                 key='allowed_values',
                                 value=AttributeUtils.list_to_value(input_list=new_allowed_values,
                                                                    type_name=self.get_entity().get_data_type_name(),
                                                                    permissions=owner_permissions),
                                 permissions=owner_permissions)

    @allowed_values.deleter
    def allowed_values(self):
        self.delete_attribute(key='allowed_values')

    # auto_bounds_prob
    @property
    def auto_bounds_prob(self):
        return self.get_attribute_value(key='auto_bounds_prob')

    @auto_bounds_prob.setter
    def auto_bounds_prob(self, new_auto_bounds_prob):
        if self.get_entity().get_data_type_name() in ['boolean', 'string']:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not allow auto_bounds_prob")
        if self.get_entity().get_data_type_name() not in [AttributeType.TYPE_NAME_DATETIME, AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT]:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not match any allowed attribute type_name")
        self.set_attribute_value(type_name=self.get_entity().get_data_type_name(),
                                 key='auto_bounds_prob',
                                 value=new_auto_bounds_prob,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @auto_bounds_prob.deleter
    def auto_bounds_prob(self):
        self.delete_attribute(key='auto_bounds_prob')

    # auto_lower
    @property
    def auto_lower(self):
        return self.get_attribute_value(key='auto_lower')

    @auto_lower.setter
    def auto_lower(self, new_auto_lower):
        if self.get_entity().get_data_type_name() in ['boolean', 'string']:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not allow auto_lower")
        if self.get_entity().get_data_type_name() not in [AttributeType.TYPE_NAME_DATETIME, AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT]:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not match any allowed attribute type_name")
        self.set_attribute_value(type_name=self.get_entity().get_data_type_name(),
                                 key='auto_lower',
                                 value=new_auto_lower,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @auto_lower.deleter
    def auto_lower(self):
        self.delete_attribute(key='auto_lower')

    # auto_upper
    @property
    def auto_upper(self):
        return self.get_attribute_value(key='auto_upper')

    @auto_upper.setter
    def auto_upper(self, new_auto_upper):
        if self.get_entity().get_data_type_name() in ['boolean', 'string']:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not allow auto_upper")
        if self.get_entity().get_data_type_name() not in [AttributeType.TYPE_NAME_DATETIME, AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT]:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not match any allowed attribute type_name")
        self.set_attribute_value(type_name=self.get_entity().get_data_type_name(),
                                 key='auto_upper',
                                 value=new_auto_upper,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @auto_upper.deleter
    def auto_upper(self):
        self.delete_attribute(key='auto_upper')

    # mask
    @property
    def mask(self):
        return self.get_attribute_value(key='mask')

    @mask.setter
    def mask(self, new_mask):
        if self.get_entity().get_data_type_name() in ['boolean', 'datetime', 'float', 'int']:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not allow mask")
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='mask',
                                 value=new_mask,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @mask.deleter
    def mask(self):
        self.delete_attribute(key='mask')

    # private_id
    @property
    def private_id(self):
        return self.get_attribute_value(key='private_id')

    @private_id.setter
    def private_id(self, new_private_id):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='private_id',
                                 value=new_private_id,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @private_id.deleter
    def private_id(self):
        self.delete_attribute(key='private_id')

    # use_auto_bounds
    @property
    def use_auto_bounds(self):
        return self.get_attribute_value(key='use_auto_bounds')

    @use_auto_bounds.setter
    def use_auto_bounds(self, new_use_auto_bounds):
        if self.get_entity().get_data_type_name() in ['boolean', 'string']:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not allow use_auto_bounds")
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='use_auto_bounds',
                                 value=new_use_auto_bounds,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @use_auto_bounds.deleter
    def use_auto_bounds(self):
        self.delete_attribute(key='use_auto_bounds')
