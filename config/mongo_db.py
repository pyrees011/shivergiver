from pymongo import MongoClient, errors
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Database URI and Client Setup
uri = "mongodb+srv://test2:test@nosql.qmuetpj.mongodb.net/?retryWrites=true&w=majority&appName=noSQL"
client = MongoClient(uri)
db = client.testgenre  # This should match your actual database name

@app.on_event("startup")
async def startup_db_client():
    try:
        # Ensure the database connection is working
        db.list_collection_names()
        app.state.db = db  # Setting the state here
        print("MongoDB connected successfully")
    except Exception as e:
        print(f"Failed to connect to MongoDB during startup: {e}")
        raise HTTPException(status_code=500, detail=f"MongoDB connection failed: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    # Cleanly close the database connection
    client.close()
    print("MongoDB connection closed.")

@app.get("/test_db")
async def test_db():
    # Directly test the database connection to bypass potential state issues
    try:
        db.list_collection_names()  # Direct access to the db object
        return {"message": "Connected to MongoDB"}
    except Exception as e:
        return {"message": "Failed to connect to MongoDB", "error": str(e)}
