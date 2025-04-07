from fastapi import FastAPI

from spotify_advance.apis.mongodb import router as mongodb_router

app = FastAPI(
    title="Spotify Advance API",
    description="API for Spotify Advance application",
    version="1.0.0"
)

app.include_router(mongodb_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
