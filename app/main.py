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

# Run with: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
