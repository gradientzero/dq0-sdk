from dq0.sdk.data.metadata.filter.filter import Filter


class FilterSmartNoise(Filter):
    @staticmethod
    def filter(node):
        retain_attributes = {
            'dataset': {},
            'database': {},
            'schema': {},
            'table': {
                'differential_privacy_sql': {
                    'censor_dims': None,
                    'clamp_columns': None,
                    'clamp_counts': None,
                    'max_ids': None,
                    'rows': None,
                    'row_privacy': None,
                    'sample_max_ids': None,
                    'use_dpsu': None,
                },
            },
            'column': {
                'data': {
                    'data_type_name': None,
                    'name': None,
                },
                'differential_privacy': {
                    'bounded': None,
                    'cardinality': None,
                    'lower': None,
                    'upper': None,
                },
                'differential_privacy_sql': {
                    'private_id': None,
                },
            }
        }
        return Filter.filter(node=node, retain_nodes=None, retain_attributes=retain_attributes)
