from dq0.sdk.data.metadata.permissions.action import Action
from dq0.sdk.data.metadata.permissions.permissions import Permissions


class DefaultPermissions:
    OWNER_NAME = 'owner'
    USER_NAME = 'user'

    @staticmethod
    def is_valid_role_name(role_name):
        if not isinstance(role_name, str):
            raise Exception(f"role_name {role_name} is not of type str, is of type {type(role_name)} instead")
        return \
            role_name == DefaultPermissions.OWNER_NAME or \
            role_name == DefaultPermissions.USER_NAME

    @staticmethod
    def check_role_names(role_names):
        if role_names is None:
            return
        if not isinstance(role_names, set):
            raise Exception(f"role_names {role_names} is not of type set, is of type {type(role_names)} instead")
        for role_name in role_names:
            if not DefaultPermissions.is_valid_role_name(role_name=role_name):
                raise Exception(f"role_name {role_name} is invalid")

    @staticmethod
    def check_role_uuids(role_uuids):
        if role_uuids is None:
            return
        if not isinstance(role_uuids, dict):
            raise Exception(f"role_uuids is not of type dict, is of type {type(role_uuids)} instead")
        for role_name, allowed_uuids in role_uuids.items():
            DefaultPermissions.check_role_names(role_names={role_name})
            Permissions.check_internal_uuids(internal_uuids=allowed_uuids)

    @staticmethod
    def select_uuids(role_uuids, role_names):
        DefaultPermissions.check_role_uuids(role_uuids=role_uuids)
        DefaultPermissions.check_role_names(role_names=role_names)
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
            Action.READ: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names={DefaultPermissions.OWNER_NAME, DefaultPermissions.USER_NAME}),
            Action.WRITE_ATTRIBUTES: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names={DefaultPermissions.OWNER_NAME}),
            Action.WRITE_CHILD_NODES: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names={DefaultPermissions.OWNER_NAME}),
            Action.WRITE_PERMISSIONS: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names={DefaultPermissions.OWNER_NAME}),
        })

    @staticmethod
    def shared_attribute(role_uuids=None):
        return Permissions(permissions={
            Action.READ: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names={DefaultPermissions.OWNER_NAME, DefaultPermissions.USER_NAME}),
            Action.WRITE_PERMISSIONS: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names={DefaultPermissions.OWNER_NAME}),
            Action.WRITE_VALUE: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names={DefaultPermissions.OWNER_NAME}),
        })

    @staticmethod
    def owner_attribute(role_uuids=None):
        return Permissions(permissions={
            Action.READ: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names={DefaultPermissions.OWNER_NAME}),
            Action.WRITE_PERMISSIONS: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names={DefaultPermissions.OWNER_NAME}),
            Action.WRITE_VALUE: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names={DefaultPermissions.OWNER_NAME}),
        })

    @staticmethod
    def analyst_attribute(role_uuids=None):
        return Permissions(permissions={
            Action.READ: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names={DefaultPermissions.OWNER_NAME, DefaultPermissions.USER_NAME}),
            Action.WRITE_PERMISSIONS: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names={DefaultPermissions.OWNER_NAME}),
            Action.WRITE_VALUE: DefaultPermissions.select_uuids(role_uuids=role_uuids, role_names={DefaultPermissions.OWNER_NAME,
                                                                                                   DefaultPermissions.USER_NAME}),
        })
