from fastapi import APIRouter, Body
from models.user import UserModel, UserLoginModel

from config.mongo import db
from schema.schemas import individual_schema, many_schema
from bson import ObjectId

from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer

users=[]

router = APIRouter()
user_collection = db.users

def check_user(data: UserLoginModel):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

@router.get("/users", tags=["users"])
async def get_users():
    users = user_collection.users.find()
    return many_schema(users)

@router.post("/user/signup", tags=["users"])
def create_user(user: UserModel = Body(...)):
    users.append(user) # replace with db call, making sure to hash the password first
    return signJWT(user.email)


@router.post("/user/login", tags=["users"])
def user_login(user: UserLoginModel = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }