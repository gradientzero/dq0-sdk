from dq0.sdk.data.metadata.interface.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class AttributesColumnPrivateSynthesis(AttributesGroup):
    def __init__(self, column, attribute_list=None):
        super().__init__(key='private_synthesis',
                         permissions=DefaultPermissions.owner_attribute(role_uuids=column.get_role_uuids()),
                         entity=column,
                         attribute_list=attribute_list)

    # discrete
    @property
    def discrete(self):
        return self.get_attribute_value(key='discrete')

    @discrete.setter
    def discrete(self, new_discrete):
        if self.get_entity().get_data_type_name() in ['boolean', 'datetime', 'int', 'string']:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not allow discrete")
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='discrete',
                                 value=new_discrete,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @discrete.deleter
    def discrete(self):
        self.delete_attribute(key='discrete')

    # min_step
    @property
    def min_step(self):
        return self.get_attribute_value(key='min_step')

    @min_step.setter
    def min_step(self, new_min_step):
        if self.get_entity().get_data_type_name() in ['boolean', 'datetime', 'string']:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not allow min_step")
        if self.get_entity().get_data_type_name() not in [AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT]:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not match any allowed attribute type_name")
        self.set_attribute_value(type_name=self.get_entity().get_data_type_name(),
                                 key='min_step',
                                 value=new_min_step,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @min_step.deleter
    def min_step(self):
        self.delete_attribute(key='min_step')

    # synthesizable
    @property
    def synthesizable(self):
        return self.get_attribute_value(key='synthesizable')

    @synthesizable.setter
    def synthesizable(self, new_synthesizable):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='synthesizable',
                                 value=new_synthesizable,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @synthesizable.deleter
    def synthesizable(self):
        self.delete_attribute(key='synthesizable')
