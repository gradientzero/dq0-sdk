from dq0.sdk.data.metadata.filter.filter import Filter


class FilterMachineLearning(Filter):
    @staticmethod
    def filter(node):
        retain_attributes = {
            'dataset': {
                'name': None,
                'description': None,
                'tags': None,
            },
            'database': {
                'name': None,
                'description': None,
                'connector': None,
            },
            'schema': {
                'name': None,
                'description': None,
            },
            'table': {
                'name': None,
                'description': None,
                'connector': None,
                'budget_epsilon': None,
                'budget_delta': None,
            },
            'column': {
                'name': None,
                'description': None,
                'data_type_name': None,
                'is_feature': None,
                'is_target': None,
            }
        }
        return Filter.filter(node=node, retain_nodes=None, retain_attributes=retain_attributes)
