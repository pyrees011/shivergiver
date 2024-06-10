def individual_schema(user) -> dict:
    return {
        "id": str(user['_id']),
        "username": user['username'],
        "email": user['email'],
        "full_name": user['full_name'],
        "password": user['password']
    }

def many_schema(users) -> list:
    return [individual_schema(user) for user in users]
