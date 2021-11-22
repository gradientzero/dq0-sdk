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
    def restricted_str_from(object, quoted=False, request_uuids=None):
        if object is None:
            return 'null'
        string = object.__str__(request_uuids=request_uuids)
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
    def restricted_str_from_list(list, sort=False, request_uuids=None):
        if list is None:
            return " null"
        if len(list) == 0:
            return " []"
        return_string = ''
        tmp_list = [Utils.restricted_str_from(tmp_elem, quoted=False, request_uuids=request_uuids) for tmp_elem in list]
        tmp_list = [tmp_elem.replace('\n', "\n   ") for tmp_elem in tmp_list if tmp_elem is not None]
        if sort:
            tmp_list.sort()
        for tmp_elem in tmp_list:
            return_string += "\n   " + tmp_elem
        return return_string

    @staticmethod
    def list_map_to_dict(list, request_uuids=None):
        mapped_list = None
        if list is not None:
            tmp_list = [tmp_elem.to_dict(request_uuids=request_uuids) for tmp_elem in list]
            tmp_list = [tmp_elem for tmp_elem in tmp_list if tmp_elem is not None]
            if len(tmp_list) != 0:
                mapped_list = tmp_list
        return mapped_list

    @staticmethod
    def list_equals_unordered(list_a, list_b):
        if list_a is None and list_b is None:
            return True
        if list_a is None or list_b is None:
            return False
        tmp_list = list_b.copy()
        for elem in list_a:
            found_match = False
            for tmp_elem in tmp_list:
                if elem == tmp_elem:
                    found_match = True
                    tmp_list.remove(tmp_elem)
                    break
            if not found_match:
                return False
        return len(tmp_list) == 0

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
