from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.interface.dataset.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class AttributesTableDifferentialPrivacy(AttributesGroup):
    def __init__(self, table, attribute_list=None):
        super().__init__(key='differential_privacy',
                         permissions=DefaultPermissions.owner_attribute(role_uuids=table.get_role_uuids()),
                         entity=table,
                         attribute_list=attribute_list)

    # budget_delta
    @property
    def budget_delta(self):
        return self.get_attribute_value(key='budget_delta')

    @budget_delta.setter
    def budget_delta(self, new_budget_delta):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_FLOAT,
                                 key='budget_delta',
                                 value=new_budget_delta,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @budget_delta.deleter
    def budget_delta(self):
        self.delete_attribute(key='budget_delta')

    # budget_epsilon
    @property
    def budget_epsilon(self):
        return self.get_attribute_value(key='budget_epsilon')

    @budget_epsilon.setter
    def budget_epsilon(self, new_budget_epsilon):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_FLOAT,
                                 key='budget_epsilon',
                                 value=new_budget_epsilon,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @budget_epsilon.deleter
    def budget_epsilon(self):
        self.delete_attribute(key='budget_epsilon')

    # privacy_column
    @property
    def privacy_column(self):
        return self.get_attribute_value(key='privacy_column')

    @privacy_column.setter
    def privacy_column(self, new_privacy_column):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='privacy_column',
                                 value=new_privacy_column,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @privacy_column.deleter
    def privacy_column(self):
        self.delete_attribute(key='privacy_column')

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
