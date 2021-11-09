from os import stat
import uuid


class Utils:
    @staticmethod
    def str_from(object, quoted=False):
        if object is None:
            return 'null'
        string = str(object)
        return "'" + string + "'" if quoted else string
        
    @staticmethod
    def restricted_str_from(object, quoted=False, user_uuids=None, role_uuids=None):
        if object is None:
            return 'null'
        string = object.__str__(user_uuids=user_uuids, role_uuids=role_uuids)
        return "'" + string + "'" if quoted else string

    @staticmethod
    def str_from_list(list, sort=False):
        if list is None:
            return " null"
        if len(list) == 0:
            return " []"
        return_string = ''
        tmp_list = [Utils.str_from(tmp_elem, quoted=False).replace('\n', "\n   ") for tmp_elem in list]
        if sort:
            tmp_list.sort()
        for tmp_elem in tmp_list:
            return_string += "\n   " + tmp_elem
        return return_string
    
    @staticmethod
    def restricted_str_from_list(list, sort=False, user_uuids=None, role_uuids=None):
        if list is None:
            return " null"
        if len(list) == 0:
            return " []"
        return_string = ''
        tmp_list = [Utils.restricted_str_from(tmp_elem, quoted=False, user_uuids=user_uuids, role_uuids=role_uuids) for tmp_elem in list]
        tmp_list = [tmp_elem.replace('\n', "\n   ") for tmp_elem in tmp_list if tmp_elem is not None]
        if sort:
            tmp_list.sort()
        for tmp_elem in tmp_list:
            return_string += "\n   " + tmp_elem
        return return_string

    @staticmethod
    def repr_from(object):
        if object is None:
            return 'None'
        else:
            return repr(object)

    @staticmethod
    def repr_from_dict(dict):
        if dict is None:
            return 'None'
        return_string = '{'
        for element_key, element_value in dict.items():
            return_string += Utils.repr_from(element_key) + ':' + Utils.repr_from(element_value) + ','
        return_string += '}'
        return return_string

    def repr_from_list(list):
        if list is None:
            return 'None'
        return_string = '['
        for index, element in enumerate(list):
            return_string += Utils.repr_from(element)
            if index < len(list) - 1:
                return_string += ', '
        return_string += ']'
        return return_string

    @staticmethod
    def get_feature_target_cols_from_meta(metadata):
        feature_columns = []
        target_columns = []
        for node_table in metadata.root_node.child_nodes[0].child_nodes[0].child_nodes:
            for node_column in node_table.child_nodes:
                attribute_column_name = node_column.get_attribute(key='name')
                if attribute_column_name is not None:
                    attribute_column_is_feature = node_column.get_attribute(key='is_feature')
                    if attribute_column_is_feature is not None and attribute_column_is_feature.value:
                        feature_columns.append(attribute_column_name.value)
                    attribute_column_is_target = node_column.get_attribute(key='is_target')
                    if attribute_column_is_target is not None and attribute_column_is_target.value:
                        target_columns.append(attribute_column_name.value)
        return feature_columns, target_columns

    @staticmethod
    def get_header_rows_from_meta(metadata):
        header_rows = []
        for node_table in metadata.root_node.child_nodes[0].child_nodes[0].child_nodes:
            attribute_table_connector = node_table.get_attribute(key='connector')
            if attribute_table_connector is not None:
                attribute_connector_type_name = attribute_table_connector.get_attribute(key='type_name')
                if attribute_connector_type_name is not None and attribute_connector_type_name.value == 'csv':
                    attribute_connector_header_row = attribute_table_connector.get_attribute(key='header_row')
                    if attribute_connector_header_row is not None:
                        for tmp_attribute_header in attribute_connector_header_row.value:
                            header_rows.append(tmp_attribute_header.value)
        return header_rows

    @staticmethod
    def get_col_types(metadata):
        col_types = {}
        for node_table in metadata.root_node.child_nodes[0].child_nodes[0].child_nodes:
            for node_column in node_table.child_nodes:
                attribute_column_name = node_column.get_attribute(key='name')
                if attribute_column_name is not None:
                    attribute_column_data_type_name = node_column.get_attribute(key='data_type_name')
                    if attribute_column_data_type_name is not None:
                        col_types[attribute_column_name.value] = attribute_column_data_type_name.value
        return col_types if len(col_types) != 0 else None

    @staticmethod
    def is_valid_uuid(val):
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False

    @staticmethod
    def check_uuids(uuid_list):
        if uuid_list is None:
            raise Exception("uuid_list is none")
        if not isinstance(uuid_list, list):
            raise Exception(f"uuid_list is not of type list, is of type {type(uuid_list)} instead")
        uuid_set = set()
        for tmp_uuid in uuid_list:
            if not Utils.is_valid_uuid(tmp_uuid):
                raise Exception(f"uuid {tmp_uuid} is not a valid uuid")
            if tmp_uuid in uuid_set:
                raise Exception(f"duplicate uuids are not allowed, found {tmp_uuid} at least twice")
            uuid_set.add(tmp_uuid)

    @staticmethod
    def merge_uuids(uuid_list_a, uuid_list_b, overwrite=False):
        if overwrite or uuid_list_a is None:
            return uuid_list_b
        if uuid_list_b is None:
            return uuid_list_a
        uuid_list = []
        for tmp_uuid in uuid_list_a:
            if tmp_uuid in uuid_list_b:
                uuid_list.append(tmp_uuid)
        return uuid_list

    @staticmethod
    def do_intersect(list_a, list_b):
        if list_a is None or list_b is None:
            return True
        return 0 < len(list(set(list_a) & set(list_b)))

    @staticmethod
    def is_allowed(requested_a, allowed_a, requested_b, allowed_b):
        is_allowed_a = requested_a is None or allowed_a is None or Utils.do_intersect(list_a=requested_a, list_b=allowed_a)
        is_allowed_b = requested_b is None or allowed_b is None or Utils.do_intersect(list_a=requested_b, list_b=allowed_b)
        return is_allowed_a and is_allowed_b

    @staticmethod
    def list_map_to_dict(list, user_uuids=None, role_uuids=None):
        mapped_list = None
        if list is not None:
            tmp_list = [tmp_elem.to_dict(user_uuids=user_uuids, role_uuids=role_uuids) for tmp_elem in list]
            tmp_list = [tmp_elem for tmp_elem in tmp_list if tmp_elem is not None]
            if len(tmp_list) != 0:
                mapped_list = tmp_list
        return mapped_list
