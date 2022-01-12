from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.interface.dataset.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class AttributesColumnMachineLearning(AttributesGroup):
    def __init__(self, column, attribute_list=None):
        super().__init__(key='machine_learning',
                         permissions=DefaultPermissions.shared_attribute(role_uuids=column.get_role_uuids()),
                         entity=column,
                         attribute_list=attribute_list)

    # is_feature
    @property
    def is_feature(self):
        return self.get_attribute_value(key='is_feature')

    @is_feature.setter
    def is_feature(self, new_is_feature):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='is_feature',
                                 value=new_is_feature,
                                 permissions=DefaultPermissions.analyst_attribute(role_uuids=self.get_role_uuids()))

    @is_feature.deleter
    def is_feature(self):
        self.delete_attribute(key='is_feature')

    # is_target
    @property
    def is_target(self):
        return self.get_attribute_value(key='is_target')

    @is_target.setter
    def is_target(self, new_is_target):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='is_target',
                                 value=new_is_target,
                                 permissions=DefaultPermissions.analyst_attribute(role_uuids=self.get_role_uuids()))

    @is_target.deleter
    def is_target(self):
        self.delete_attribute(key='is_target')
