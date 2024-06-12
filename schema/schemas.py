def individual_schema(user) -> dict:
    return {
        "id": str(user['_id']),
        "name": user['name'],
        "email": user['email'],
        "password": user['password']
    }

def many_schema(users) -> list:
    return [individual_schema(user) for user in users]
