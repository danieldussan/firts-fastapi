def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": str(user["username"]),
        "email": str(user["email"]),
    }


def user_list_schema(user_list) -> list:
    return [user_schema(user) for user in user_list]
