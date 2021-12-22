from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.interface.dataset.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class AttributesTablePrivateSql(AttributesGroup):
    def __init__(self, table, attribute_list=None):
        super().__init__(key='private_sql',
                         permissions=DefaultPermissions.owner_attribute(role_uuids=table.role_uuids),
                         entity=table,
                         attribute_list=attribute_list)

    # censor_dims
    @property
    def censor_dims(self):
        return self.get_attribute_value(key='censor_dims')

    @censor_dims.setter
    def censor_dims(self, new_censor_dims):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='censor_dims',
                                 value=new_censor_dims,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.entity.role_uuids))

    @censor_dims.deleter
    def censor_dims(self):
        self.delete_attribute(key='censor_dims')

    # clamp_columns
    @property
    def clamp_columns(self):
        return self.get_attribute_value(key='clamp_columns')

    @clamp_columns.setter
    def clamp_columns(self, new_clamp_columns):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='clamp_columns',
                                 value=new_clamp_columns,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.entity.role_uuids))

    @clamp_columns.deleter
    def clamp_columns(self):
        self.delete_attribute(key='clamp_columns')

    # clamp_counts
    @property
    def clamp_counts(self):
        return self.get_attribute_value(key='clamp_counts')

    @clamp_counts.setter
    def clamp_counts(self, new_clamp_counts):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='clamp_counts',
                                 value=new_clamp_counts,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.entity.role_uuids))

    @clamp_counts.deleter
    def clamp_counts(self):
        self.delete_attribute(key='clamp_counts')

    # max_ids
    @property
    def max_ids(self):
        return self.get_attribute_value(key='max_ids')

    @max_ids.setter
    def max_ids(self, new_max_ids):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_INT,
                                 key='max_ids',
                                 value=new_max_ids,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.entity.role_uuids))

    @max_ids.deleter
    def max_ids(self):
        self.delete_attribute(key='max_ids')

    # row_privacy
    @property
    def row_privacy(self):
        return self.get_attribute_value(key='row_privacy')

    @row_privacy.setter
    def row_privacy(self, new_row_privacy):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='row_privacy',
                                 value=new_row_privacy,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.entity.role_uuids))

    @row_privacy.deleter
    def row_privacy(self):
        self.delete_attribute(key='row_privacy')

    # sample_max_ids
    @property
    def sample_max_ids(self):
        return self.get_attribute_value(key='sample_max_ids')

    @sample_max_ids.setter
    def sample_max_ids(self, new_sample_max_ids):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='sample_max_ids',
                                 value=new_sample_max_ids,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.entity.role_uuids))

    @sample_max_ids.deleter
    def sample_max_ids(self):
        self.delete_attribute(key='sample_max_ids')

    # tau
    @property
    def tau(self):
        return self.get_attribute_value(key='tau')

    @tau.setter
    def tau(self, new_tau):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_FLOAT,
                                 key='tau',
                                 value=new_tau,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.entity.role_uuids))

    @tau.deleter
    def tau(self):
        self.delete_attribute(key='tau')

    # use_dpsu
    @property
    def use_dpsu(self):
        return self.get_attribute_value(key='use_dpsu')

    @use_dpsu.setter
    def use_dpsu(self, new_use_dpsu):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='use_dpsu',
                                 value=new_use_dpsu,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.entity.role_uuids))

    @use_dpsu.deleter
    def use_dpsu(self):
        self.delete_attribute(key='use_dpsu')
