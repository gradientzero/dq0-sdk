from dq0.sdk.data.metadata.structure.filter.filter import Filter


class FilterSmartNoise(Filter):
    @staticmethod
    def filter(node):
        retain_attributes = {
            'dataset': {
                'data': {
                    'name': None,
                },
                'differential_privacy': {
                    'privacy_level': None,
                }
            },
            'database': {
                'connector': None,
                'data': {
                    'name': None,
                },
                'differential_privacy': {
                    'privacy_level': None,
                }
            },
            'schema': {
                'data': {
                    'name': None,
                },
                'differential_privacy': {
                    'privacy_level': None,
                }
            },
            'table': {
                'data': {
                    'name': None,
                    'rows': None,
                },
                'differential_privacy': {
                    'privacy_level': None,
                },
                'private_sql': {
                    'censor_dims': None,
                    'clamp_columns': None,
                    'clamp_counts': None,
                    'max_ids': None,
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
                'private_sql': {
                    'private_id': None,
                },
                'private_sql_and_synthesis': {
                    'bounded': None,
                    'cardinality': None,
                    'lower': None,
                    'upper': None,
                },
            }
        }
        return Filter.filter(node=node, retain_nodes=None, retain_attributes=retain_attributes)
