from dq0.sdk.data.metadata.interface.dataset.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class AttributesTablePrivateSynthesis(AttributesGroup):
    def __init__(self, table, attribute_list=None):
        super().__init__(key='private_synthesis',
                         permissions=DefaultPermissions.owner_attribute(role_uuids=table.get_role_uuids()),
                         entity=table,
                         attribute_list=attribute_list)

    # synth_allowed
    @property
    def synth_allowed(self):
        return self.get_attribute_value(key='synth_allowed')

    @synth_allowed.setter
    def synth_allowed(self, new_synth_allowed):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='synth_allowed',
                                 value=new_synth_allowed,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @synth_allowed.deleter
    def synth_allowed(self):
        self.delete_attribute(key='synth_allowed')
