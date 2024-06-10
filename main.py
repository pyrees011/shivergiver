from fastapi import FastAPI
from routes.userRoutes import router as user_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(user_router, prefix="/api/v1")