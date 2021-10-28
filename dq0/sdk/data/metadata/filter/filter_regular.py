from dq0.sdk.data.metadata.filter.filter import Filter


class FilterRegular(Filter):
    @staticmethod
    def filter(node):
        retain_attributes = {
            'dataset': {
                'name': None,
                'description': None,
                'tags': None,
                'metadata_is_public': None,
                'connector': None,
            },
            'database': {
                'name': None,
                'description': None,
                'metadata_is_public': None,
                'connector': None,
            },
            'schema': {
                'name': None,
                'description': None,
                'metadata_is_public': None,
                'connector': None,
                'privacy_level': None,
            },
            'table': {
                'name': None,
                'description': None,
                'metadata_is_public': None,
                'connector': None,
                'privacy_level': None,
                'tau': None,
                'synth_allowed': None,
                'budget_epsilon': None,
                'budget_delta': None,
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
                'description': None,
                'metadata_is_public': None,
                'data_type_name': None,
                'bounded': None,
                'lower': None,
                'upper': None,
                'private_id': None,
                'cardinality': None,
                'use_auto_bounds': None,
                'auto_bounds_prob': None,
                'auto_lower': None,
                'auto_upper': None,
                'allowed_values': None,
                'selectable': None,
                'mask': None,
                'synthesizable': None,
                'discrete': None,
                'min_step': None,
                'is_feature': None,
                'is_target': None,
            }
        }
        return Filter.filter(node=node, retain_nodes=None, retain_attributes=retain_attributes)
