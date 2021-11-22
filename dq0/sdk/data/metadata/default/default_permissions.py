from dq0.sdk.data.metadata.permissions.action import Action
from dq0.sdk.data.metadata.permissions.permissions import Permissions


class DefaultPermissions:
    OWNER_NAME = 'owner'
    USER_NAME = 'user'

    @staticmethod
    def select_uuids(role_uuids, role_names):
        if role_uuids is None:
            return None
        selected_role_uuids = set()
        for role_name in role_names if role_names is not None else []:
            if role_name in role_uuids:
                selected_role_uuids = selected_role_uuids.union(role_uuids[role_name])
        return selected_role_uuids

    @staticmethod
    def shared_node(role_uuids=None):
        return Permissions(permissions={
            Action.READ: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names=[DefaultPermissions.OWNER_NAME, DefaultPermissions.USER_NAME]),
            Action.WRITE_ATTRIBUTES: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names=[DefaultPermissions.OWNER_NAME]),
            Action.WRITE_CHILD_NODES: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names=[DefaultPermissions.OWNER_NAME]),
            Action.WRITE_PERMISSIONS: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names=[DefaultPermissions.OWNER_NAME]),
        })

    @staticmethod
    def shared_attribute(role_uuids=None):
        return Permissions(permissions={
            Action.READ: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names=[DefaultPermissions.OWNER_NAME, DefaultPermissions.USER_NAME]),
            Action.WRITE_PERMISSIONS: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names=[DefaultPermissions.OWNER_NAME]),
            Action.WRITE_VALUE: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names=[DefaultPermissions.OWNER_NAME]),
        })

    @staticmethod
    def owner_attribute(role_uuids=None):
        return Permissions(permissions={
            Action.READ: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names=[DefaultPermissions.OWNER_NAME]),
            Action.WRITE_PERMISSIONS: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names=[DefaultPermissions.OWNER_NAME]),
            Action.WRITE_VALUE: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names=[DefaultPermissions.OWNER_NAME]),
        })

    @staticmethod
    def user_attribute(role_uuids=None):
        return Permissions(permissions={
            Action.READ: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names=[DefaultPermissions.OWNER_NAME, DefaultPermissions.USER_NAME]),
            Action.WRITE_PERMISSIONS: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names=[DefaultPermissions.OWNER_NAME]),
            Action.WRITE_VALUE: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names=[DefaultPermissions.OWNER_NAME, DefaultPermissions.USER_NAME]),
        })
