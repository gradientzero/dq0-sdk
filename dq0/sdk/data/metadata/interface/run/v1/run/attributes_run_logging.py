from dq0.sdk.data.metadata.interface.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class AttributesRunLogging(AttributesGroup):
    def __init__(self, run, attribute_list=None):
        super().__init__(key='logging',
                         permissions=DefaultPermissions.analyst_attribute(role_uuids=run.get_role_uuids()),
                         entity=run,
                         attribute_list=attribute_list)

    # log_key_string
    @property
    def log_key_string(self):
        return self.get_attribute_value(key='log_key_string')

    @log_key_string.setter
    def log_key_string(self, new_log_key_string):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='log_key_string',
                                 value=new_log_key_string,
                                 permissions=DefaultPermissions.analyst_attribute(role_uuids=self.get_role_uuids()))

    @log_key_string.deleter
    def log_key_string(self):
        self.delete_attribute(key='log_key_string')

    # tracker_output_path
    @property
    def tracker_output_path(self):
        return self.get_attribute_value(key='tracker_output_path')

    @tracker_output_path.setter
    def tracker_output_path(self, new_tracker_output_path):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='tracker_output_path',
                                 value=new_tracker_output_path,
                                 permissions=DefaultPermissions.analyst_attribute(role_uuids=self.get_role_uuids()))

    @tracker_output_path.deleter
    def tracker_output_path(self):
        self.delete_attribute(key='tracker_output_path')

    # tracker_type
    @property
    def tracker_type(self):
        return self.get_attribute_value(key='tracker_type')

    @tracker_type.setter
    def tracker_type(self, new_tracker_type):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='tracker_type',
                                 value=new_tracker_type,
                                 permissions=DefaultPermissions.analyst_attribute(role_uuids=self.get_role_uuids()))

    @tracker_type.deleter
    def tracker_type(self):
        self.delete_attribute(key='tracker_type')

    # tracker_group_uuid
    @property
    def tracker_group_uuid(self):
        return self.get_attribute_value(key='tracker_group_uuid')

    @tracker_group_uuid.setter
    def tracker_group_uuid(self, new_tracker_group_uuid):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='tracker_group_uuid',
                                 value=new_tracker_group_uuid,
                                 permissions=DefaultPermissions.analyst_attribute(role_uuids=self.get_role_uuids()))

    @tracker_group_uuid.deleter
    def tracker_group_uuid(self):
        self.delete_attribute(key='tracker_group_uuid')

    # tracker_run_uuid
    @property
    def tracker_run_uuid(self):
        return self.get_attribute_value(key='tracker_run_uuid')

    @tracker_run_uuid.setter
    def tracker_run_uuid(self, new_tracker_run_uuid):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='tracker_run_uuid',
                                 value=new_tracker_run_uuid,
                                 permissions=DefaultPermissions.analyst_attribute(role_uuids=self.get_role_uuids()))

    @tracker_run_uuid.deleter
    def tracker_run_uuid(self):
        self.delete_attribute(key='tracker_run_uuid')
