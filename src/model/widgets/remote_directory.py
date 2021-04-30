from src.model.algorithm.tree_node import TreeNode


class RemoteDirectory:
    def __init__(self, tree: TreeNode, override_name: str = None):
        self._name = tree.get_name() if override_name is None else override_name
        self.node = tree.get_payload()

    def get_name(self) -> str:
        return self._name

    def get_id(self) -> str:
        return self.node.id
