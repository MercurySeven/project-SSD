from src.model.algorithm.node import Type
from src.model.algorithm.tree_node import TreeNode
from src.model.widgets.file import File
from src.model.widgets.directory import Directory


class RemoteDirectory(Directory):
    def __init__(self, tree: TreeNode, override_name: str = None):
        super().__init__(tree, override_name)

    def update_list_of_content(self) -> None:
        self._files.clear()
        self._dirs.clear()
        #if self._node.get_children is None:
        #    return
        content = self._node.get_children()
        for entry in content:
            if entry.get_payload().type == Type.File:
                self._files.append(File(entry))
            else:
                self._dirs.append(RemoteDirectory(entry))
