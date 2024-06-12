from fastapi import FastAPI
from routes.userRoutes import router as user_router
from routes.appointments import router as appointment_router

from routes.relationRoutes import router as relation_router
from routes.album_routes import router as album_router


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(user_router, prefix="/api/v1")
app.include_router(appointment_router, prefix="/api/v2")
app.include_router(relation_router, prefix="/api/v3")
app.include_router(album_router)
