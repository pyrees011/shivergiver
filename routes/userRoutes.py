from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models.user import UserModel, UserLoginModel
from config.mongo_config import db
from schema.schemas import individual_schema, many_schema
from auth.auth_handler import signJWT, get_password_hash, verify_password
from auth.auth_bearer import JWTBearer

from config.redis_config import redis_conn
from utils.redis_helper import get_user_data, store_user_data, check_redis_cache

router = APIRouter()
user_collection = db.users

def check_user(data: UserLoginModel):
    db_user = user_collection.find_one({"email": data.email})
    if db_user and verify_password(data.password, db_user['password']):
        return True
    return False

@router.post("/user/signup", tags=["users"])
async def create_user(user: UserModel = Body(...)):
    if user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")
    
    user.password = get_password_hash(user.password)
    user_collection.insert_one({"name": user.name, "email": user.email, "password": user.password})
    return signJWT(user.email)

@router.post("/user/login", tags=["users"])
async def user_login(user: UserLoginModel = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    raise HTTPException(status_code=401, detail="Wrong login details!")

@router.get("/user/profile", dependencies=[Depends(JWTBearer())], tags=["users"])
async def get_user_profile(user: str ):
    if check_redis_cache(user, "user"):
        return get_user_data(user)
    user_data = user_collection.find_one({"email": user})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    store_user_data(user, user_data)
    return individual_schema(user_data)

@router.get('/user/getAlluser', dependencies=[Depends(JWTBearer())], tags=['users'])
async def get_all_user():
    user_data = user_collection.find()
    if not user_data:
        raise HTTPException(status_code=404, detail="No user found")
    return many_schema(user_data)
