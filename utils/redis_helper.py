import json
from bson import ObjectId
from datetime import timedelta

from config.redis_config import redis_conn as redis_client

# Utility function to serialize ObjectId to JSON
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

def check_redis_cache(key: str, type: str):
    return redis_client.exists(f'{type}:{key}')

def store_token(email, token):
    redis_client.setex(f"token:{email}", timedelta(hours=1), token)

def get_token(email):
    return redis_client.get(f"token:{email}")

def store_user_data(email, user_data):
    key = f"user:{email}"
    redis_client.hmset(key, user_data)
    redis_client.expire(key, timedelta(hours=1))

def get_user_data(email):
    return redis_client.hgetall(f"user:{email}")

def store_appointment(appointment_id, appointment_data):
    key = f"appointment:{appointment_id}"
    redis_client.hmset(key, appointment_data)
    redis_client.expire(key, timedelta(hours=1))

def get_appointment(appointment_id):
    return redis_client.hgetall(f"appointment:{appointment_id}")

def delete_appointment(appointment_id):
    return redis_client.delete(f"appointment:{appointment_id}")

def store_album(album_id, album_data):
    key = f"album:{album_id}"
    redis_client.hmset(key, album_data)
    redis_client.expire(key, timedelta(hours=1))

def get_album(album_id):
    return redis_client.hgetall(f"album:{album_id}")

def delete_album(album_id):
    return redis_client.delete(f"album:{album_id}")


