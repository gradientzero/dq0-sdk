from dq0.sdk.data.metadata.default.default_dataset import DefaultDataset


class Default:
    @staticmethod
    def check(default):
        if not isinstance(default, Default):
            raise Exception(f"default is not of type Default, is of type {type(default)} instead")

    def __init__(self, role_uuids=None):
        self.role_uuids = role_uuids

    def apply_defaults(self, node):
        return DefaultDataset.apply_defaults(node=node, role_uuids=self.role_uuids)

    def verify(self, node):
        DefaultDataset.verify(node=node, role_uuids=self.role_uuids)
