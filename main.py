from fastapi import FastAPI
from config.mongo_db import app as mongo_app  # Updated import statement

app = FastAPI()

# Mount the MongoDB related app to handle database operations
app.mount("/mongo", mongo_app)

@app.get("/")
async def read_root():
    return {"Hello": "World"}
