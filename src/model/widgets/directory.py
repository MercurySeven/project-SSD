from src.model.algorithm.tree_node import TreeNode


class Directory:

    def __init__(self, tree: TreeNode, override_name: str = None):
        self._name = tree.get_name() if override_name is None else override_name
        self._files = []
        self._dirs = []
        self._node = tree

    def update_list_of_content(self) -> None:
        pass

    def get_name(self) -> str:
        return self._name
