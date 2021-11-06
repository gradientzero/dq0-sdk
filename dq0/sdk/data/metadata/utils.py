class Utils:
    @staticmethod
    def str_from(object):
        if object is None:
            return 'None'
        else:
            return str(object)

    @staticmethod
    def str_from_list(list):
        if list is None:
            return " None"
        if len(list) == 0:
            return " []"
        return_string = ''
        for element in list:
            return_string += "\n   " + Utils.str_from(element).replace('\n', "\n   ")
        return return_string

    @staticmethod
    def str_from_dict(dict):
        if dict is None:
            return " None"
        if len(dict) == 0:
            return " {}"
        return_string = ''
        for element_key, element_value in list:
            return_string += "\n   " + Utils.str_from(element_key) + ':' + Utils.str_from(element_value).replace('\n', "\n   ")
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
        for element in list:
            return_string += Utils.repr_from(element) + ','
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
