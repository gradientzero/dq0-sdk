from uuid import UUID

from dq0.sdk.data.metadata.structure.explanation import Explanation
from dq0.sdk.data.metadata.structure.merge_exception import MergeException
from dq0.sdk.data.metadata.structure.permissions.action import Action
from dq0.sdk.data.metadata.structure.utils.str_utils import StrUtils


class Permissions:
    def is_valid_uuid(uuid, version=4):
        try:
            tmp_uuid = UUID(uuid, version=version)
        except ValueError:
            return False
        return str(tmp_uuid) == uuid

    @staticmethod
    def check(permissions):
        if permissions is None:
            return
        if not isinstance(permissions, Permissions):
            raise Exception(f"permissions is not of type Permissions, is of type {type(permissions)} instead")
        Permissions.check_internal_permissions(internal_permissions=permissions._permissions)

    @staticmethod
    def check_internal_permissions(internal_permissions):
        if internal_permissions is None:
            return
        if not isinstance(internal_permissions, dict):
            raise Exception(f"internal_permissions is not of type dict, is of type {type(internal_permissions)} instead")
        for action, allowed_uuids in internal_permissions.items():
            if not Action.is_valid_action(action=action):
                raise Exception(f"action {action} is invalid")
            Permissions.check_internal_uuids(internal_uuids=allowed_uuids)

    @staticmethod
    def check_internal_uuids(internal_uuids):
        if internal_uuids is None:
            return
        if not isinstance(internal_uuids, set):
            raise Exception(f"internal_uuids is not of type set, is of type {type(internal_uuids)} instead")
        for uuid in internal_uuids:
            if uuid is None:
                raise Exception("uuid is none")
            if not Permissions.is_valid_uuid(uuid=uuid):
                raise Exception(f"uuid {uuid} is invalid")

    @staticmethod
    def are_merge_compatible(permissions_a, permissions_b, explanation=None):
        Permissions.check(permissions=permissions_a)
        Permissions.check(permissions=permissions_b)
        if permissions_a is None or permissions_b is None:
            return True
        return permissions_a.is_merge_compatible_with(other=permissions_b, explanation=explanation)

    @staticmethod
    def are_mergeable(permissions_a, permissions_b, overwrite=False, explanation=None):
        return Permissions.are_merge_compatible(permissions_a=permissions_a, permissions_b=permissions_b, explanation=explanation)

    @staticmethod
    def merge(permissions_a, permissions_b, overwrite=False):
        if not Permissions.are_mergeable(permissions_a=permissions_a, permissions_b=permissions_b, overwrite=overwrite):
            raise MergeException(f"cannot merge permissions that are not mergeable; permissions_a: {permissions_a} permissions_b: {permissions_b}")
        if permissions_a is None and permissions_b is None:
            return None
        if permissions_a is None:
            return permissions_b.copy()
        if permissions_b is None:
            return permissions_a.copy()
        return permissions_a.merge_with(other=permissions_b, overwrite=overwrite)

    @staticmethod
    def merge_internal_uuids(internal_uuids_a, internal_uuids_b, overwrite=False, sum=False):
        Permissions.check_internal_uuids(internal_uuids=internal_uuids_a)
        Permissions.check_internal_uuids(internal_uuids=internal_uuids_b)
        if internal_uuids_a is None and internal_uuids_b is None:
            return None
        if overwrite or internal_uuids_a is None:
            return internal_uuids_b.copy() if internal_uuids_b is not None else None
        if internal_uuids_b is None:
            return internal_uuids_a.copy() if internal_uuids_a is not None else None
        if sum:
            return internal_uuids_a.union(internal_uuids_b)
        return internal_uuids_a & internal_uuids_b

    @staticmethod
    def str_from_internal_uuids(internal_uuids, sort=False):
        if internal_uuids is None:
            return " null"
        if len(internal_uuids) == 0:
            return " {}"
        return_string = ' {'
        tmp_list = list(internal_uuids)
        if sort:
            tmp_list.sort()
        for index, tmp_elem in enumerate(tmp_list):
            return_string += tmp_elem
            if index < len(tmp_list) - 1:
                return_string += ", "
        return_string += '}'
        return return_string

    @staticmethod
    def is_allowed_with(permissions, action, request_uuids=set(), explanation=None):
        Permissions.check_internal_uuids(internal_uuids=request_uuids)
        if action is not None and not Action.is_valid_action(action=action):
            raise Exception(f"action {action} is invalid")
        Permissions.check(permissions=permissions)
        if permissions is None or action is None or request_uuids is None:
            return True
        return permissions.is_allowed(action=action, request_uuids=request_uuids, explanation=explanation)

    @staticmethod
    def is_subset_of(permissions_a, permissions_b):
        Permissions.check(permissions=permissions_a)
        Permissions.check(permissions=permissions_b)
        if permissions_b is None:
            return True
        if permissions_a is None:
            return False
        return permissions_a.is_subset(other=permissions_b)

    def __init__(self, permissions):
        Permissions.check_internal_permissions(internal_permissions=permissions)
        self._permissions = permissions

    def __str__(self):
        if self.get_permissions() is None:
            return " null"
        if len(self.get_permissions()) == 0:
            return " {}"
        return_string = ''
        for action, allowed_uuids in self.get_permissions().items():
            return_string += "\n  " + StrUtils.str_from(action, quoted=True) + ':' + \
                Permissions.str_from_internal_uuids(internal_uuids=allowed_uuids, sort=True).replace('\n', "\n  ")
        return return_string

    def __repr__(self):
        repr_permissions = 'None'
        if self.get_permissions() is not None:
            repr_permissions = '{'
            sorted_actions = sorted(self.get_permissions().keys())
            for action_index, action in enumerate(sorted_actions):
                repr_permissions += repr(action) + ": {"
                sorted_uuids = sorted(list(self.get_permissions()[action]))
                for uuid_index, uuid in enumerate(sorted_uuids):
                    repr_permissions += repr(uuid)
                    if uuid_index < len(sorted_uuids) - 1:
                        repr_permissions += ", "
                repr_permissions += '}'
                if action_index < len(sorted_actions) - 1:
                    repr_permissions += ", "
            repr_permissions += '}'
        return f"Permissions(permissions={repr_permissions})"

    def __eq__(self, other):
        if other is None or not isinstance(other, Permissions):
            return False
        return self.get_permissions() == other.get_permissions()

    def get_permissions(self):
        return self._permissions

    def copy(self):
        if self.get_permissions() is None:
            return Permissions(permissions=None)
        copied_permissions = {}
        for action, allowed_uuids in self.get_permissions().items():
            copied_permissions[action] = allowed_uuids.copy() if allowed_uuids is not None else None
        return Permissions(permissions=copied_permissions)

    def to_dict(self):
        if self.get_permissions() is None:
            return None
        permissions_dict = {}
        for action, allowed_uuids in self.get_permissions().items():
            permissions_dict[action] = allowed_uuids
        return permissions_dict

    def is_merge_compatible_with(self, other, explanation=None):
        Permissions.check(other)
        return True

    def is_mergeable_with(self, other, overwrite=False, explanation=None):
        return self.is_merge_compatible_with(other=other, explanation=explanation)

    def merge_with(self, other, overwrite=False, sum=False):
        if not self.is_mergeable_with(other=other, overwrite=overwrite):
            raise MergeException(f"cannot merge permissions that are not mergeable; self: {self} other: {other}")
        if other is None:
            return self.copy()
        if other.get_permissions() is None:
            return self.copy()
        if self.get_permissions() is None:
            return other.copy()
        merged_permissions = {}
        for action, allowed_uuids in self.get_permissions().items():
            if action in other.get_permissions():
                merged_permissions[action] = Permissions.merge_internal_uuids(internal_uuids_a=allowed_uuids, internal_uuids_b=other.get_permissions()[action],
                                                                              overwrite=overwrite, sum=sum)
            else:
                merged_permissions[action] = allowed_uuids.copy() if allowed_uuids is not None else None
        for action, allowed_uuids in other.get_permissions().items():
            if action not in self.get_permissions():
                merged_permissions[action] = allowed_uuids.copy() if allowed_uuids is not None else None
        return Permissions(permissions=merged_permissions)

    def is_allowed(self, action, request_uuids=set(), explanation=None):
        Permissions.check_internal_uuids(internal_uuids=request_uuids)
        if action is not None and not Action.is_valid_action(action=action):
            raise Exception(f"action {action} is invalid")
        if self.get_permissions() is None or action is None or request_uuids is None:
            return True
        if action not in self.get_permissions():
            Explanation.dynamic_add_message(explanation=explanation, message=f"Permissions.is_allowed(...): action {action} not contained")
            return False
        if self.get_permissions()[action] is None:
            return True
        if len(self.get_permissions()[action] & request_uuids) == 0:
            Explanation.dynamic_add_message(explanation=explanation,
                                            message="Permissions.is_allowed(...): "
                                            f"none of requested uuids {request_uuids} in allowed uuids {self.get_permissions()[action]}")
            return False
        return True

    def is_subset(self, other):
        Permissions.check(permissions=other)
        if other is None or other.get_permissions() is None:
            return True
        if self.get_permissions() is None:
            return False
        for action, allowed_uuids in self.get_permissions().items():
            if action not in other.get_permissions():
                return False
            if other.get_permissions()[action] is not None:
                if allowed_uuids is None:
                    return False
                if not allowed_uuids.issubset(other.get_permissions()[action]):
                    return False
        return True
