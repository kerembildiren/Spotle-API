import os
import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from app.routes import router

# Create FastAPI instance
app = FastAPI(title="Spotle API")

# Include routes from routes.py
app.include_router(router)

@app.get("/")
def home():
    return {"message": "Welcome to Spotle API!"}

# Initialize caching when app starts
@app.on_event("startup")
def startup():
    FastAPICache.init(InMemoryBackend())

# Get the PORT from Render's environment (default to 8000 if not set)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use Render's PORT variable
    uvicorn.run(app, host="0.0.0.0", port=port)

