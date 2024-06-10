# auth_handler.py
from passlib.context import CryptContext
import jwt
from decouple import config
import time

# Configuration for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Environment variables
JWT_SECRET = config('secret')
JWT_ALGORITHM = config('ALGORITHM', default='HS256')

# Function to hash passwords
def get_password_hash(password):
    return pwd_context.hash(password)

# Function to verify passwords
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to sign JWTs
def signJWT(user_id: str):
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600  # 10 minutes from now
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

# Function to decode JWTs
def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token['expires'] >= time.time() else None
    except:
        return None