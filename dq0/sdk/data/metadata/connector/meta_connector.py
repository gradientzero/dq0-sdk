from dq0.sdk.data.metadata.connector.meta_connector_type import MetaConnectorType


class MetaConnector:
    def __init__(self, type_name):
        if not MetaConnectorType.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        self.type_name = type_name

    def copy(self):
        return MetaConnector(self.type_name)

    def to_dict(self):
        return {k: v for k, v in [('type_name', self.type_name)] if v is not None}

    def merge_precheck_with(self, other):
        if other is None:
            raise Exception("other cannot be None for merge")
        if self.type_name != other.type_name:
            raise Exception(f"type_names must match for merge but {self.type_name} <--> {other.type_name}")
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge connectors that fail the precheck")
        return self.copy()
  
