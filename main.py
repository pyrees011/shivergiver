from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr
from pymongo import MongoClient
from typing import Optional

from auth.auth_handler import get_password_hash, verify_password, create_access_token, verify_token

# Initialize FastAPI app
app = FastAPI()

# Database connection setup
uri = "mongodb+srv://test2:test@nosql.qmuetpj.mongodb.net/?retryWrites=true&w=majority&appName=noSQL"
client = MongoClient(uri)
db = client.users  # Database name
collection = db.accounts  # Collection name

# OAuth2 setup for FastAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic models for user data
class UserRegistrationModel(BaseModel):
    username: str
    email: EmailStr
    password: str
    age: Optional[int] = None
    sex: Optional[str] = None
    genre: Optional[str] = None

class UserLoginModel(BaseModel):
    username: str
    password: str

# Startup and Shutdown events
@app.on_event("startup")
async def startup_db_client():
    try:
        db.list_collection_names()
        print("MongoDB connected successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MongoDB connection failed: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    print("MongoDB connection closed.")

# User registration endpoint
@app.post("/register")
async def register(user: UserRegistrationModel):
    if collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict['password'] = hashed_password  # Replace plain password with hashed one
    result = collection.insert_one(user_dict)
    return {"username": user.username, "id": str(result.inserted_id)}

# User login endpoint
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# User profile retrieval endpoint
@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    username = verify_token(token, credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ))
    user = collection.find_one({"username": username})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user["username"], "email": user.get("email"), "age": user.get("age")}
