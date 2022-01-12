from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.interface.dataset.attribute_utils import AttributeUtils
from dq0.sdk.data.metadata.interface.dataset.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class AttributesDatabaseConnector(AttributesGroup):
    def __init__(self, database, attribute_list=None):
        super().__init__(key='connector',
                         permissions=DefaultPermissions.shared_attribute(role_uuids=database.get_role_uuids()),
                         entity=database,
                         attribute_list=attribute_list)

    def type_name_check(self, type_name):
        if self.type_name != type_name:
            raise Exception(f"access forbidden, typename mismatch: {self.type_name} != {type_name}")

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
                                 permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()))

    @type_name.deleter
    def type_name(self):
        raise Exception(f"type_name {self.type_name} may not be deleted")

    # ==========================================================================================================================================================
    # csv
    # ==========================================================================================================================================================

    # decimal
    @property
    def decimal(self):
        self.type_name_check(type_name='csv')
        return self.get_attribute_value(key='decimal')

    @decimal.setter
    def decimal(self, new_decimal):
        self.type_name_check(type_name='csv')
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='decimal',
                                 value=new_decimal,
                                 permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()))

    @decimal.deleter
    def decimal(self):
        self.type_name_check(type_name='csv')
        self.delete_attribute(key='decimal')

    # header_columns
    @property
    def header_columns(self):
        self.type_name_check(type_name='csv')
        return AttributeUtils.value_to_list(input_value=self.get_attribute_value(key='header_columns'))

    @header_columns.setter
    def header_columns(self, new_header_columns):
        self.type_name_check(type_name='csv')
        shared_permissions = DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids())
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_LIST,
                                 key='header_columns',
                                 value=AttributeUtils.list_to_value(input_list=new_header_columns,
                                                                    type_name=AttributeType.TYPE_NAME_STRING,
                                                                    permissions=shared_permissions),
                                 permissions=shared_permissions)

    @header_columns.deleter
    def header_columns(self):
        self.type_name_check(type_name='csv')
        self.delete_attribute(key='header_columns')

    # header_row
    @property
    def header_row(self):
        self.type_name_check(type_name='csv')
        value = self.get_attribute_value(key='header_row')
        return AttributeUtils.value_to_list(input_value=value) if isinstance(value, list) else value

    @header_row.setter
    def header_row(self, new_header_row):
        self.type_name_check(type_name='csv')
        shared_permissions = DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids())
        value = AttributeUtils.list_to_value(input_list=new_header_row,
                                             type_name=AttributeType.TYPE_NAME_INT,
                                             permissions=shared_permissions) \
            if isinstance(new_header_row, list) else new_header_row
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_LIST if isinstance(new_header_row, list) else AttributeType.TYPE_NAME_INT,
                                 key='header_row',
                                 value=value,
                                 permissions=shared_permissions)

    @header_row.deleter
    def header_row(self):
        self.type_name_check(type_name='csv')
        self.delete_attribute(key='header_row')

    # index_col
    @property
    def index_col(self):
        self.type_name_check(type_name='csv')
        value = self.get_attribute_value(key='index_col')
        return AttributeUtils.value_to_list(input_value=value) if isinstance(value, list) else value

    @index_col.setter
    def index_col(self, new_index_col):
        self.type_name_check(type_name='csv')
        shared_permissions = DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids())
        type_name = None
        value = None
        if isinstance(new_index_col, str):
            type_name = AttributeType.TYPE_NAME_STRING
            value = new_index_col
        elif isinstance(new_index_col, int):
            type_name = AttributeType.TYPE_NAME_INT
            value = new_index_col
        elif isinstance(new_index_col, list):
            type_name = AttributeType.TYPE_NAME_LIST
            list_type_name = AttributeType.TYPE_NAME_STRING
            if len(new_index_col) != 0:
                if isinstance(new_index_col[0], int):
                    list_type_name = AttributeType.TYPE_NAME_INT
                elif not isinstance(new_index_col[0], str):
                    raise Exception(f"first list element {new_index_col[0]} is neither of type int nor of type str, "
                                    f"is of type {type(new_index_col[0])} instead")
            value = AttributeUtils.list_to_value(input_list=new_index_col,
                                                 type_name=list_type_name,
                                                 permissions=shared_permissions)
        else:
            raise Exception(f"new_index_col {new_index_col} is neither of type list nor of type int or str, is of type {type(new_index_col)} instead")
        self.set_attribute_value(type_name=type_name,
                                 key='index_col',
                                 value=value,
                                 permissions=shared_permissions)

    @index_col.deleter
    def index_col(self):
        self.type_name_check(type_name='csv')
        self.delete_attribute(key='index_col')

    # na_values
    @property
    def na_values(self):
        self.type_name_check(type_name='csv')
        return AttributeUtils.value_to_dict(input_value=self.get_attribute_value(key='na_values'))

    @na_values.setter
    def na_values(self, new_na_values):
        self.type_name_check(type_name='csv')
        shared_permissions = DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids())
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_LIST,
                                 key='na_values',
                                 value=AttributeUtils.dict_to_value(input_dict=new_na_values,
                                                                    type_name=None,
                                                                    permissions=shared_permissions),
                                 permissions=shared_permissions)

    @na_values.deleter
    def na_values(self):
        self.type_name_check(type_name='csv')
        self.delete_attribute(key='na_values')

    # sep
    @property
    def sep(self):
        self.type_name_check(type_name='csv')
        return self.get_attribute_value(key='sep')

    @sep.setter
    def sep(self, new_sep):
        self.type_name_check(type_name='csv')
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='sep',
                                 value=new_sep,
                                 permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()))

    @sep.deleter
    def sep(self):
        self.type_name_check(type_name='csv')
        self.delete_attribute(key='sep')

    # skipinitialspace
    @property
    def skipinitialspace(self):
        self.type_name_check(type_name='csv')
        return self.get_attribute_value(key='skipinitialspace')

    @skipinitialspace.setter
    def skipinitialspace(self, new_skipinitialspace):
        self.type_name_check(type_name='csv')
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='skipinitialspace',
                                 value=new_skipinitialspace,
                                 permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()))

    @skipinitialspace.deleter
    def skipinitialspace(self):
        self.type_name_check(type_name='csv')
        self.delete_attribute(key='skipinitialspace')

    # uri
    @property
    def uri(self):
        self.type_name_check(type_name='csv')
        return self.get_attribute_value(key='uri')

    @uri.setter
    def uri(self, new_uri):
        self.type_name_check(type_name='csv')
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='uri',
                                 value=new_uri,
                                 permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()))

    @uri.deleter
    def uri(self):
        self.type_name_check(type_name='csv')
        self.delete_attribute(key='uri')

    # use_original_header
    @property
    def use_original_header(self):
        self.type_name_check(type_name='csv')
        return self.get_attribute_value(key='use_original_header')

    @use_original_header.setter
    def use_original_header(self, new_use_original_header):
        self.type_name_check(type_name='csv')
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_BOOLEAN,
                                 key='use_original_header',
                                 value=new_use_original_header,
                                 permissions=DefaultPermissions.shared_attribute(role_uuids=self.get_role_uuids()))

    @use_original_header.deleter
    def use_original_header(self):
        self.type_name_check(type_name='csv')
        self.delete_attribute(key='use_original_header')

    # ==========================================================================================================================================================
    # postgresql
    # ==========================================================================================================================================================

    # host
    @property
    def host(self):
        self.type_name_check(type_name='postgresql')
        return self.get_attribute_value(key='host')

    @host.setter
    def host(self, new_host):
        self.type_name_check(type_name='postgresql')
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='host',
                                 value=new_host,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @host.deleter
    def host(self):
        self.type_name_check(type_name='postgresql')
        self.delete_attribute(key='host')

    # password
    @property
    def password(self):
        self.type_name_check(type_name='postgresql')
        return self.get_attribute_value(key='password')

    @password.setter
    def password(self, new_password):
        self.type_name_check(type_name='postgresql')
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='password',
                                 value=new_password,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @password.deleter
    def password(self):
        self.type_name_check(type_name='postgresql')
        self.delete_attribute(key='password')

    # port
    @property
    def port(self):
        self.type_name_check(type_name='postgresql')
        return self.get_attribute_value(key='port')

    @port.setter
    def port(self, new_port):
        self.type_name_check(type_name='postgresql')
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_INT,
                                 key='port',
                                 value=new_port,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @port.deleter
    def port(self):
        self.type_name_check(type_name='postgresql')
        self.delete_attribute(key='port')

    # username
    @property
    def username(self):
        self.type_name_check(type_name='postgresql')
        return self.get_attribute_value(key='username')

    @username.setter
    def username(self, new_username):
        self.type_name_check(type_name='postgresql')
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='username',
                                 value=new_username,
                                 permissions=DefaultPermissions.owner_attribute(role_uuids=self.get_role_uuids()))

    @username.deleter
    def username(self):
        self.type_name_check(type_name='postgresql')
        self.delete_attribute(key='username')
