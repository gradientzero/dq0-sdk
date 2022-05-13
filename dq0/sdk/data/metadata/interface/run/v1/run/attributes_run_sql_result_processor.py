from dq0.sdk.data.metadata.interface.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class AttributesRunSQLResultProcessor(AttributesGroup):
    def __init__(self, attributes_run_sql, attribute_list=None):
        super().__init__(key='result_processor',
                         permissions=DefaultPermissions.analyst_attribute(role_uuids=attributes_run_sql.get_role_uuids()),
                         entity=attributes_run_sql,
                         attribute_list=attribute_list)

    def type_names_check(self, type_names):
        if self.type_name not in type_names:
            raise Exception(f"access forbidden, typename mismatch: {self.type_name} not in {type_names}")

    # type_name
    @property
    def type_name(self):
        return self.get_attribute_value(key='type_name')

    @type_name.setter
    def type_name(self, new_type_name):
        if self.type_name is not None:
            raise Exception(f"type_name {self.type_name} may not be modified")
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='type_name',
                                 value=new_type_name,
                                 permissions=DefaultPermissions.analyst_attribute(role_uuids=self.get_role_uuids()),
                                 allow_modification=False)

    @type_name.deleter
    def type_name(self):
        raise Exception(f"type_name {self.type_name} may not be deleted")

    # ==========================================================================================================================================================
    # modular properties
    # ==========================================================================================================================================================

    # epsilon
    @property
    def epsilon(self):
        self.type_names_check(type_names={'opendp', 'classic_dp'})
        return self.get_attribute_value(key='epsilon')

    @epsilon.setter
    def epsilon(self, new_epsilon):
        self.type_names_check(type_names={'opendp', 'classic_dp'})
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_FLOAT,
                                 key='epsilon',
                                 value=new_epsilon,
                                 permissions=DefaultPermissions.analyst_attribute(role_uuids=self.get_role_uuids()))

    @epsilon.deleter
    def epsilon(self):
        self.type_names_check(type_names={'opendp', 'classic_dp'})
        self.delete_attribute(key='epsilon')

    # delta
    @property
    def delta(self):
        self.type_names_check(type_names={'opendp'})
        return self.get_attribute_value(key='delta')

    @delta.setter
    def delta(self, new_delta):
        self.type_names_check(type_names={'opendp'})
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_FLOAT,
                                 key='delta',
                                 value=new_delta,
                                 permissions=DefaultPermissions.analyst_attribute(role_uuids=self.get_role_uuids()))

    @delta.deleter
    def delta(self):
        self.type_names_check(type_names={'opendp'})
        self.delete_attribute(key='delta')
