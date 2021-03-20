
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
                id
                name
                created_at
                updated_at
                type
                ... on Folder {
                    children(limit:50) {
                        ...nodo
                    }
                }
            }
        }

        fragment nodo on Node {
            id
            name
            created_at
            updated_at
            type
            ... on File {
                size
            }
        }
        """

        params = {
            "id": node_id
        }

        return (query, params)
