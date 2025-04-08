from datetime import datetime

import requests
from pydantic import BaseModel


class TrackRecord(BaseModel):
    user_id: str
    track_id: str
    played_at: datetime


class MongoDBAPI:

    def __init__(self) -> None:
        self.url = "http://localhost:8000/"

    def get_recently_played(self, user_id: str, limit: int = 20) -> list[TrackRecord]:
        response = requests.get(
            f"{self.url}/recently_played/{user_id}?limit={limit}")
        return [TrackRecord(**item) for item in response.json()]

    def store_recently_played(self, user_id: str, track_id: str, played_at: datetime) -> None:
        response = requests.post(f"{self.url}/recently_played", json={
                                 "user_id": user_id, "track_id": track_id, "played_at": played_at})
        return response.json()

    def delete_user_recently_played(self, user_id: str) -> None:
        response = requests.delete(f"{self.url}/recently_played/{user_id}")
        return response.json()
