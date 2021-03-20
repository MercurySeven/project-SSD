from .tree_node import TreeNode


def get_only_files(children: list[TreeNode]) -> list[TreeNode]:
    return [node for node in children if not node.is_directory()]


def get_only_folders(children: list[TreeNode]) -> list[TreeNode]:
    return [node for node in children if node.is_directory()]


def compareFiles(client: list[TreeNode], server: list[TreeNode]) -> list:
    update_files: list = []

    for cl_file in client:
        trovato = False
        for sr_file in server:
            if cl_file._name == sr_file._name:
                if cl_file._updated_at > sr_file._updated_at:
                    update_files.append({
                        "name": cl_file._name,
                        "action": "client aggiornato"
                    })
                elif sr_file._updated_at > cl_file._updated_at:
                    update_files.append({
                        "name": cl_file._name,
                        "action": "server aggiornato"
                    })
                trovato = True
                break
        if not trovato:
            # Il client ha un file che nel server non c'è
            update_files.append({
                "name": cl_file._name,
                "action": "client upload"
            })

    for sr_file in server:
        trovato = False
        for cl_file in client:
            if sr_file._name == cl_file._name:
                trovato = True
        if not trovato:
            # Il server ha un file che nel client non c'è
            update_files.append({
                "name": sr_file._name,
                "action": "server download"
            })

    return update_files


def compareFolders(client: TreeNode, server: TreeNode) -> list:
    update_files: list = []

    # Controllo prima SOLO i file
    client_files = get_only_files(client._children)
    server_files = get_only_files(server._children)
    update_files.extend(compareFiles(client_files, server_files))

    client_folders = get_only_folders(client._children)
    server_folders = get_only_folders(server._children)

    for cl_folder in client_folders:
        trovato = False
        for sr_folder in server_folders:
            if cl_folder._name == sr_folder._name:
                trovato = True
                update_files.extend(compareFolders(cl_folder, sr_folder))
        if not trovato:
            # Il client ha un cartella che nel server non c'è
            update_files.append({
                "name": cl_folder._name,
                "action": "client folder upload"
            })

    for sr_folder in server_folders:
        trovato = False
        for cl_folder in client_folders:
            if sr_folder._name == cl_folder._name:
                trovato = True
        if not trovato:
            # Il server ha una cartella che nel client non c'è
            update_files.append({
                "name": sr_folder._name,
                "action": "server folder download"
            })
    return update_files
