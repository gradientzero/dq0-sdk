from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class Specification:
    @staticmethod
    def check(specification):
        if not isinstance(specification, Specification):
            raise Exception(f"specification is not of type Specification, is of type {type(specification)} instead")

    def __init__(self, node_type_name, version, apply_defaults_func, verify_func, role_uuids=None):
        DefaultPermissions.check_role_uuids(role_uuids=role_uuids)
        self.node_type_name = node_type_name
        self.version = version
        self.apply_defaults_func = apply_defaults_func
        self.verify_func = verify_func
        self.role_uuids = role_uuids

    def __str__(self):
        return f"{self.node_type_name}_{self.version}"

    def __repr__(self):
        return "Specification(" + \
            f"node_type_name={repr(self.node_type_name)}, " + \
            f"version={repr(self.version)}, " + \
            f"apply_defaults_func={repr(self.apply_defaults_func)}, " + \
            f"verify_func={repr(self.verify_func)}, " + \
            f"role_uuids={repr(self.role_uuids)})"

    def apply_defaults(self, node):
        if node is None:
            raise Exception("node is none")
        if self.node_type_name != node.type_name:
            raise Exception(f"node type names do not match: {self.node_type_name} != {node.type_name}")
        return self.apply_defaults_func(node=node, role_uuids=self.role_uuids)

    def verify(self, node):
        if node is None:
            raise Exception("node is none")
        if self.node_type_name != node.type_name:
            raise Exception(f"node type names do not match: {self.node_type_name} != {node.type_name}")
        self.verify_func(node=node, role_uuids=self.role_uuids)
