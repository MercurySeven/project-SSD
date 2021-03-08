def get_info_from_email():
    return """
    query GetUserByEmail($email: String!) {
        getUserByEmail(email: $email) {
            id
            full_name
        }
    }
    """


def get_all_files():
    return """
    query GetNode ($id: ID!) {
        getNode(id: $id) {
            id
            created_at
            name
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
        ...file
    }

    fragment file on File {
        size
    }
    """
