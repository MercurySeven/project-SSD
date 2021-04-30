
class Query:

    @staticmethod
    def get_info_from_email(email: str) -> tuple[str, dict[str, str]]:
        query = """
        query GetUserByEmail($email: String!) {
            getUserByEmail(email: $email) {
                id
                full_name
            }
        }
        """

        params = {
            "email": email
        }

        return (query, params)

    @staticmethod
    def get_all_files(node_id: str) -> tuple[str, dict[str, str]]:
        query = """
        query GetNode ($id: ID!) {
            getNode(id: $id) {
                ... node
                ... on Folder {
                    children(limit:50) {
                        ...node
                    }
                }
            }
        }

        fragment node on Node {
            id
            name
            created_at
            updated_at
            type
            ... on File {
                size
            }
            last_editor {
                email
            }
        }
        """

        params = {
            "id": node_id
        }

        return (query, params)

    @staticmethod
    def create_folder(parent_folder_id: str, folder_name: str) -> tuple[str, dict[str, str]]:
        query = """
        mutation CreateFolder ($parent_id: String!, $name: String!) {
            createFolder(parent_id: $parent_id, name: $name) {
                id
            }
        }
        """

        params = {
            "parent_id": parent_folder_id,
            "name": folder_name
        }

        return (query, params)

    @staticmethod
    def delete_node(node_id: str) -> tuple[str, dict[str, str]]:
        query = """
        mutation DeleteNodes($node_id: ID!) {
            deleteNodes(nodes: {
                node_id: $node_id
            })
        }
        """

        params = {
            "node_id": node_id
        }

        return (query, params)
