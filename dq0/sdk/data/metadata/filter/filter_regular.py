from dq0.sdk.data.metadata.filter.filter import Filter


class FilterRegular(Filter):
    @staticmethod
    def filter(node):
        retain_attributes = {
            'dataset': {
                'data': {
                    'description': None,
                    'metadata_is_public': None,
                    'name': None,
                    'tags': None,
                },
                'differential_privacy': {
                    'privacy_level': None,
                },
            },
            'database': {
                'connector': {
                    'type_name': None,
                },
                'data': {
                    'description': None,
                    'metadata_is_public': None,
                    'name': None,
                },
                'differential_privacy': {
                    'privacy_level': None,
                },
            },
            'schema': {
                'data': {
                    'description': None,
                    'metadata_is_public': None,
                    'name': None,
                },
                'differential_privacy': {
                    'privacy_level': None,
                },
            },
            'table': {
                'connector': {
                    'decimal': None,
                    'header_columns': None,
                    'header_row': None,
                    'na_values': None,
                    'sep': None,
                    'skipinitialspace': None,
                    'type_name': None,
                    'uri': None,
                    'use_original_header': None,
                },
                'data': {
                    'description': None,
                    'metadata_is_public': None,
                    'name': None,
                },
                'data_synthesis': {
                    'synth_allowed': None,
                    'tau': None,
                },
                'differential_privacy': {
                    'budget_delta': None,
                    'budget_epsilon': None,
                    'privacy_column': None,
                    'privacy_level': None,
                },
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
                'privacy_attacks': {
                    'calibration_fact': None,
                    'confidence_threshold_list': None,
                    'model_performance_metric': None,
                    'model_privacy_balanced': None,
                    'model_privacy_metric': None,
                    'model_privacy_metric_threshold': None,
                    'model_task': None,
                    'num_attack_runs': None,
                    'num_CV_folds_gen_gap': None,
                    'privacy_leakage_metrics': None,
                    'risk_env': None,
                    'sm_attacks': None,
                    'sm_attacks_topk_proba': None,
                    'stop_at_first_privacy_breach': None,
                    'test_size': None,
                },
            },
            'column': {
                'data': {
                    'data_type_name': None,
                    'description': None,
                    'discrete': None,
                    'metadata_is_public': None,
                    'name': None,
                    'selectable': None,
                },
                'data_synthesis': {
                    'synthesizable': None,
                },
                'differential_privacy': {
                    'bounded': None,
                    'cardinality': None,
                    'lower': None,
                    'upper': None,
                },
                'differential_privacy_sql': {
                    'allowed_values': None,
                    'auto_bounds_prob': None,
                    'auto_lower': None,
                    'auto_upper': None,
                    'mask': None,
                    'min_step': None,
                    'private_id': None,
                    'use_auto_bounds': None,
                },
                'machine_learning': {
                    'is_feature': None,
                    'is_target': None,
                },
                'privacy_attacks': {
                    'enabled': None,
                    'alias': None,
                    'weight': None,
                },
            }
        }
        return Filter.filter(node=node, retain_nodes=None, retain_attributes=retain_attributes)
