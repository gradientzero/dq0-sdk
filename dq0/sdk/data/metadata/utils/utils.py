class Utils:
    @staticmethod
    def get_feature_target_cols(meta_table):
        feature_columns = []
        target_columns = []
        column_names = meta_table.column_names()
        for column_name in column_names:
            meta_column_ml = meta_table.column(name=column_name).machine_learning
            if meta_column_ml.is_feature:
                feature_columns.append(column_name)
            if meta_column_ml.is_target:
                target_columns.append(column_name)
        return feature_columns, target_columns

    @staticmethod
    def get_col_types(meta_table):
        col_types = {}
        column_names = meta_table.column_names()
        for column_name in column_names:
            data_type_name = meta_table.column(name=column_name).data.data_type_name
            if isinstance(data_type_name, str):
                col_types[column_name] = data_type_name
        return col_types if len(col_types) != 0 else None
