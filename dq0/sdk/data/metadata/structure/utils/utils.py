class Utils:
    @staticmethod
    def get_feature_target_cols(meta_table):
        feature_columns = []
        target_columns = []
        for meta_column in meta_table:
            if meta_column.machine_learning.is_feature:
                feature_columns.append(meta_column.data.name)
            if meta_column.machine_learning.is_target:
                target_columns.append(meta_column.data.name)
        return feature_columns, target_columns

    @staticmethod
    def get_col_types(meta_table):
        col_types = {}
        for meta_column in meta_table:
            data_type_name = meta_column.data.data_type_name
            if isinstance(data_type_name, str):
                col_types[meta_column.data.name] = data_type_name
        return col_types if len(col_types) != 0 else None
