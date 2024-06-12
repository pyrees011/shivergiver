# This file is responsible for signing , encoding , decoding and returning JWTS
import time
from datetime import datetime, timedelta
from typing import Dict
from fastapi import HTTPException

import jwt
from decouple import config
from passlib.context import CryptContext

# redis
from config.redis_config import redis_conn

from utils.redis_helper import check_redis_cache, store_token, get_token

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def token_response(token: str):
    return {
        "access_token": token,
        "token_type": "bearer"
    }

def signJWT(user_email: str):
    if check_redis_cache(user_email, "token"):
        token = get_token(user_email)
        return token_response(token)
    payload = {
        "user_id": user_email,
        "expires": time.time() + 3600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    store_token(user_email, token)
    return token_response(token)

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token['expires'] >= time.time() else None
    except:
        return {}


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
