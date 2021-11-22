from dq0.sdk.data.metadata.permissions.permissions import Permissions


class PermissionsFactory:
    @staticmethod
    def from_yaml_dict(yaml_dict):
        return Permissions(permissions=yaml_dict)