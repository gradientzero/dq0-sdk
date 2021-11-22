from dq0.sdk.data.metadata.filter.filter import Filter


class FilterRegular(Filter):
    @staticmethod
    def filter(node):
        retain_attributes = {
            'dataset': {
                'description': None,
                'metadata_is_public': None,
                'name': None,
                'privacy_level': None,
                'tags': None,
            },
            'database': {
                'connector': None,
                'description': None,
                'metadata_is_public': None,
                'name': None,
                'privacy_level': None,
            },
            'schema': {
                'description': None,
                'metadata_is_public': None,
                'name': None,
                'privacy_level': None,
            },
            'table': {
                'budget_delta': None,
                'budget_epsilon': None,
                'max_ids': None,
                'privacy_column': None,
                'tau': None,
                'censor_dims': None,
                'clamp_columns': None,
                'clamp_counts': None,
                'connector': None,
                'description': None,
                'metadata_is_public': None,
                'name': None,
                'privacy_level': None,
                'rows': None,
                'row_privacy': None,
                'sample_max_ids': None,
                'synth_allowed': None,
                'use_dpsu': None,
            },
            'column': {
                'auto_bounds_prob': None,
                'auto_lower': None,
                'auto_upper': None,
                'cardinality': None,
                'lower': None,
                'mask': None,
                'upper': None,
                'allowed_values': None,
                'bounded': None,
                'bonding': None,
                'data_type_name': None,
                'data': None,
                'description': None,
                'discrete': None,
                'is_feature': None,
                'is_target': None,
                'machine_learning': None,
                'metadata_is_public': None,
                'min_step': None,
                'name': None,
                'private_id': None,
                'selectable': None,
                'synthesizable': None,
                'use_auto_bounds': None,
            }
        }
        return Filter.filter(node=node, retain_nodes=None, retain_attributes=retain_attributes)
