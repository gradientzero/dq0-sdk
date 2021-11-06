from dq0.sdk.data.metadata.filter.filter import Filter


class FilterSmartNoise(Filter):
    @staticmethod
    def filter(node):
        retain_attributes = {
            'dataset': None,
            'database': None,
            'schema': None,
            'table': {
                'row_privacy': None,
                'rows': None,
                'max_ids': None,
                'sample_max_ids': None,
                'use_dpsu': None,
                'clamp_counts': None,
                'clamp_columns': None,
                'censor_dims': None,
            },
            'column': {
                'name': None,
                'data_type_name': None,
                'bounded': None,
                'lower': None,
                'upper': None,
                'private_id': None,
                'cardinality': None,
            }
        }
        return Filter.filter(node=node, retain_nodes=None, retain_attributes=retain_attributes)
