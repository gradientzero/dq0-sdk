from data.metadata.meta_verifier import MetaVerifier


class Metadata:
    def __init__(self, root_node, verify=None):
        if verify is None:
            verify = MetaVerifier.verify
        verify(root_node)
        self.root_node = root_node
