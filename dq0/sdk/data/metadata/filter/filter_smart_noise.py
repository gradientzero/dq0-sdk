from dq0.sdk.data.metadata.filter.filter import Filter


class FilterSmartNoise(Filter):
    @staticmethod
    def filter(node):
        retain_attributes = {
            'dataset': None,
            'database': None,
            'schema': None,
            'table': {
                'max_ids': None,
                'censor_dims': None,
                'clamp_columns': None,
                'clamp_counts': None,
                'rows': None,
                'row_privacy': None,
                'sample_max_ids': None,
                'use_dpsu': None,
            },
            'column': {
                'cardinality': None,
                'lower': None,
                'upper': None,
                'bounded': None,
                'data_type_name': None,
                'name': None,
                'private_id': None,
            }
        }
        return Filter.filter(node=node, retain_nodes=None, retain_attributes=retain_attributes)
