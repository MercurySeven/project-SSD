from src.model.algorithm.tree_node import TreeNode


class RemoteDirectory:
    def __init__(self, tree: TreeNode, override_name: str = None):
        self._name = tree.get_name() if override_name is None else override_name
        self.id = tree.get_payload().id
        self._node = tree.get_payload()

    def get_name(self):
        return self._name
