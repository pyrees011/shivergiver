from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user import UserModel, UserLoginModel
from auth.auth_handler import get_password_hash, verify_password, signJWT, decodeJWT
from config.mongo_db import get_database
from fastapi.encoders import jsonable_encoder
from pymongo.collection import Collection

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get the database collection
def get_user_collection(db=Depends(get_database)):
    return db["users"]

@router.post("/register", response_model=UserModel, tags=["users"])
async def register_user(user: UserModel, users: Collection = Depends(get_user_collection)):
    # Check if the user already exists
    if await users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user.password)  # Hash the password
    await users.insert_one(user_dict)
    return user_dict

@router.post("/login", tags=["users"])
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), users: Collection = Depends(get_user_collection)):
    user = await users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return signJWT(user['email'])

@router.get("/users", tags=["users"], dependencies=[Depends(oauth2_scheme)])
async def get_users(users: Collection = Depends(get_user_collection)):
    user_list = await users.find().to_list(100)
    return user_list

@router.post("/token", tags=["users"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), users: Collection = Depends(get_user_collection)):
    user = await users.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, user['password']):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": signJWT(user['email']), "token_type": "bearer"}

@router.get("/logout", tags=["users"])
async def logout_user(token: str = Depends(oauth2_scheme)):
    # Here, you would handle token invalidation if using a server-side session store or a blacklist mechanism
    return {"msg": "Logged out successfully"}

