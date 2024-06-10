from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.userRoutes import router as user_router

app = FastAPI()

# Serve static files from the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include user routes
app.include_router(user_router, prefix="/api/v1")

# Define main page route to serve index.html
@app.get("/", response_class=HTMLResponse)
async def read_main_page():
    with open("static/index.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
