from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from spotify_advance.apis import client_data, mongodb_data
from spotify_advance.apis.spotify import SpotifyAPI
from spotify_advance.datamodels.track_record import RecentlyPlayedTrackRecord
from spotify_advance.handlers.mongodb import MongoDBHandler


class TrackRecord(BaseModel):
    user_id: str
    track_id: str
    played_at: datetime


class SavedTrack(BaseModel):
    user_id: str
    track_id: str
    added_at: datetime


app = FastAPI()
handler = MongoDBHandler(mongodb_data['uri'])
spotify_api = SpotifyAPI(**client_data)


@app.get("/me",
         name="get_me",
         description="get user from spotify",
         tags=["me"])
async def get_me() -> dict:
    return spotify_api.current_user


@app.get("/recently_played/{user_id}",
         name="get_recently_played",
         description="get user recently played tracks from mongodb",
         tags=["recently_played"],
         response_model=list[RecentlyPlayedTrackRecord])
async def get_recently_played(user_id: str) -> list[RecentlyPlayedTrackRecord]:
    tracks, message = handler.get_recently_played(user_id)
    if not tracks:
        raise HTTPException(
            status_code=500, detail=message)
    return tracks


@app.post("/recently_played",
          name="store_recently_played",
          description="store recently played track in mongodb",
          tags=["recently_played"],
          response_model=dict)
async def store_recently_played(user_id: str, track_id: str, played_at: datetime) -> dict:
    success, message = handler.store_recently_played(
        user_id, track_id, played_at)
    if not success:
        raise HTTPException(
            status_code=500, detail=message)
    return {"message": message}


@app.delete("/recently_played/{user_id}",
            description="delete all recently played tracks for a user from mongodb",
            tags=["recently_played"],
            response_model=bool)
async def delete_user_recently_played(user_id: str) -> bool:
    success, message = handler.delete_user_recently_played(user_id)
    if not success:
        raise HTTPException(
            status_code=500, detail=message)
    return success


@app.post("/saved_tracks",
          name="store_saved_track",
          description="store saved track in mongodb",
          tags=["saved_tracks"],
          response_model=SavedTrack)
async def store_saved_track(request: SavedTrack) -> SavedTrack:
    success, message = handler.store_saved_track(
        request.user_id, request.track_id, request.added_at)
    if not success:
        raise HTTPException(
            status_code=500, detail=message)
    return request


@app.get("/saved_tracks/{user_id}",
         name="get_saved_tracks",
         description="get user saved tracks from mongodb",
         tags=["saved_tracks"],
         response_model=list[SavedTrack])
async def get_saved_tracks(user_id: str) -> list[SavedTrack]:
    tracks, message = handler.get_saved_tracks(user_id)
    if not tracks:
        raise HTTPException(
            status_code=500, detail=message)
    return tracks


@app.delete("/saved_tracks",
            name="delete_user_saved_tracks",
            description="delete all saved tracks for a user from mongodb",
            tags=["saved_tracks"],
            response_model=dict)
async def delete_user_saved_tracks(user_id: str, track_id: str) -> dict:
    success, message = handler.delete_user_saved_tracks(user_id, track_id)
    if not success:
        raise HTTPException(
            status_code=500, detail=message)
    return {"message": message}


@app.post("/tracks",
          name="store_track",
          description="store track in mongodb",
          tags=["tracks"],
          response_model=bool)
async def store_track(request: dict) -> None:
    print(f"request: {request}")
    track = request['track']
    name = track['name']
    track_id = track['id']
    popularity = track['popularity']
    uri = track['uri']
    album = track['album']
    artists = track['artists']
    success, message = handler.store_track(
        name, track_id, popularity, uri, album, artists)
    if not success:
        raise HTTPException(
            status_code=500, detail=message)
    return success


@app.get("/tracks/all",
         name="get_all_tracks",
         description="get all tracks from mongodb",
         tags=["tracks"],
         response_model=list[dict])
async def get_all_tracks() -> list[dict]:
    tracks, message = handler.get_all_tracks()
    if not tracks:
        raise HTTPException(
            status_code=500, detail=message)
    return tracks


@app.get("/tracks/{track_id}",
         name="get_track",
         description="get track from mongodb",
         tags=["tracks"],
         response_model=dict)
async def get_track(track_id: str) -> dict:
    track, message = handler.get_track(track_id)
    if not track:
        raise HTTPException(
            status_code=500, detail=message)
    return track


@app.delete("/tracks/{track_id}",
            name="delete_track",
            description="delete track from mongodb",
            tags=["tracks"],
            response_model=bool)
async def delete_track(track_id: str) -> bool:
    success, message = handler.delete_track(track_id)
    if not success:
        raise HTTPException(
            status_code=500, detail=message)
    return success
