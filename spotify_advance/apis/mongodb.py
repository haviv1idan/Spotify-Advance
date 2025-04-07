from datetime import datetime

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from spotify_advance.apis import client_data, mongodb_data
from spotify_advance.apis.spotify import SpotifyAPI
from spotify_advance.handlers.mongodb import MongoDBHandler


class TrackRecord(BaseModel):
    user_id: str
    track_id: str
    played_at: datetime


app = FastAPI()
handler = MongoDBHandler(mongodb_data['uri'])
spotify_api = SpotifyAPI(**client_data)


@app.get("/me")
async def get_me() -> dict:
    return spotify_api.current_user


@app.get("/recently_played/{user_id}",
         description="get user recently played tracks from mongodb",
         response_model=list[TrackRecord])
async def get_recently_played(user_id: str, limit: int = Query(10, ge=1, le=50)) -> list[TrackRecord]:
    tracks = handler.get_recently_played(user_id, limit)
    return tracks


@app.post("/recently_played",
          description="store recently played track in mongodb",
          response_model=TrackRecord)
async def store_recently_played(request: TrackRecord) -> TrackRecord:
    success = handler.store_recently_played(
        request.user_id, request.track_id, request.played_at)
    if not success:
        raise HTTPException(
            status_code=500, detail="Failed to store recently played track")
    return request


@app.delete("/recently_played/{user_id}",
            description="delete all recently played tracks for a user from mongodb")
async def delete_user_recently_played(user_id: str) -> bool:
    success = handler.delete_user_recently_played(user_id)
    return success
