from dq0.sdk.data.metadata.structure.filter.filter import Filter


class FilterMachineLearning(Filter):
    @staticmethod
    def filter(node):
        retain_attributes = {
            'dataset': {
                'data': {
                    'description': None,
                    'name': None,
                    'tags': None,
                },
            },
            'database': {
                'connector': None,
                'data': {
                    'description': None,
                    'name': None,
                },
            },
            'schema': {
                'data': {
                    'description': None,
                    'name': None,
                },
            },
            'table': {
                'data': {
                    'description': None,
                    'name': None,
                },
                'differential_privacy': {
                    'budget_delta': None,
                    'budget_epsilon': None,
                },
            },
            'column': {
                'data': {
                    'data_type_name': None,
                    'description': None,
                    'name': None,
                },
                'machine_learning': {
                    'is_feature': None,
                    'is_target': None,
                },
            }
        }
        return Filter.filter(node=node, retain_nodes=None, retain_attributes=retain_attributes)
