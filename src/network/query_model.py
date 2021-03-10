
class Query:

    @staticmethod
    def GET_INFO_FROM_EMAIL(email: str) -> tuple[str, dict[str, str]]:
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
    def GET_ALL_FILES(ID: str) -> tuple[str, dict[str, str]]:
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
            "id": ID
        }

        return (query, params)
