from dq0.sdk.data.metadata.default.default_dataset import DefaultDataset
from dq0.sdk.data.metadata.default.default_permissions import DefaultPermissions


class Default:
    VERSION = 2021112301

    @staticmethod
    def check(default):
        if not isinstance(default, Default):
            raise Exception(f"default is not of type Default, is of type {type(default)} instead")

    @staticmethod
    def check_version(version):
        if version is None:
            return
        if not isinstance(version, int):
            raise Exception(f"version {version} is not of type int, is of type {type(version)} instead")
        if Default.VERSION < version:
            raise Exception(f"version {version} is too new for highest provided version {Default.VERSION}")

    @staticmethod
    def obtain_with(version, role_uuids=None):
        Default.check_version(version=version)
        return Default(role_uuids=role_uuids)

    def __init__(self, role_uuids=None):
        DefaultPermissions.check_role_uuids(role_uuids=role_uuids)
        self.role_uuids = role_uuids

    def version(self, requested_version=0):
        Default.check_version(version=requested_version)
        return Default.VERSION

    def apply_defaults(self, node):
        return DefaultDataset.apply_defaults(node=node, role_uuids=self.role_uuids)

    def verify(self, node):
        DefaultDataset.verify(node=node, role_uuids=self.role_uuids)
