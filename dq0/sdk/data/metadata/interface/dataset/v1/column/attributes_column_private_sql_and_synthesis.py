from dq0.sdk.data.metadata.interface.dataset.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class AttributesColumnPrivateSqlAndSynthesis(AttributesGroup):
    def __init__(self, column, attribute_list=None):
        super().__init__(key='private_sql_and_synthesis',
                         permissions=DefaultPermissions.owner_attribute(role_uuids=column.get_role_uuids()),
                         entity=column,
                         attribute_list=attribute_list)

    # bounded
    @property
    def bounded(self):
        return self.get_attribute_value(key='bounded')

    @bounded.setter
    def bounded(self, new_bounded):
        if self.get_entity().get_data_type_name() in ['boolean', 'string']:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not allow bounded")
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='bounded',
                                 value=new_bounded,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @bounded.deleter
    def bounded(self):
        self.delete_attribute(key='bounded')

    # cardinality
    @property
    def cardinality(self):
        return self.get_attribute_value(key='cardinality')

    @cardinality.setter
    def cardinality(self, new_cardinality):
        if self.get_entity().get_data_type_name() in ['boolean']:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not allow cardinality")
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_INT,
                                 key='cardinality',
                                 value=new_cardinality,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @cardinality.deleter
    def cardinality(self):
        self.delete_attribute(key='cardinality')

    # lower
    @property
    def lower(self):
        return self.get_attribute_value(key='lower')

    @lower.setter
    def lower(self, new_lower):
        if self.get_entity().get_data_type_name() in ['boolean', 'string']:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not allow lower")
        if self.get_entity().get_data_type_name() not in [AttributeType.TYPE_NAME_DATETIME, AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT]:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not match any allowed attribute type_name")
        self.set_attribute_value(type_name=self.get_entity().get_data_type_name(),
                                 key='lower',
                                 value=new_lower,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @lower.deleter
    def lower(self):
        self.delete_attribute(key='lower')

    # upper
    @property
    def upper(self):
        return self.get_attribute_value(key='upper')

    @upper.setter
    def upper(self, new_upper):
        if self.get_entity().get_data_type_name() in ['boolean', 'string']:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not allow upper")
        if self.get_entity().get_data_type_name() not in [AttributeType.TYPE_NAME_DATETIME, AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT]:
            raise Exception(f"data_type_name {self.get_entity().get_data_type_name()} does not match any allowed attribute type_name")
        self.set_attribute_value(type_name=self.get_entity().get_data_type_name(),
                                 key='upper',
                                 value=new_upper,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @upper.deleter
    def upper(self):
        self.delete_attribute(key='upper')
