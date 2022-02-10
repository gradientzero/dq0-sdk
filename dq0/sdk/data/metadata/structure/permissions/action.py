class Action:
    READ = 'read'
    WRITE_ATTRIBUTES = 'write_attributes'
    WRITE_CHILD_NODES = 'write_child_nodes'
    WRITE_PERMISSIONS = 'write_permissions'
    WRITE_VALUE = 'write_value'

    @staticmethod
    def is_valid_action(action):
        if action is None:
            return False
        if not isinstance(action, str):
            raise Exception(f"action is not of type str, is of type {type(action)} instead")
        return \
            action == Action.READ or \
            action == Action.WRITE_ATTRIBUTES or \
            action == Action.WRITE_CHILD_NODES or \
            action == Action.WRITE_PERMISSIONS or \
            action == Action.WRITE_VALUE
