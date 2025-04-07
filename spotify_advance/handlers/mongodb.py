from datetime import datetime
from logging import getLogger

from pymongo import DESCENDING, MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from spotify_advance.datamodels.track_record import TrackRecord


class MongoDBHandler:

    def __init__(self, uri: str):
        self.client = MongoClient(uri)
        self.db: Database = self.client.spotify_advance
        self.recently_played: Collection = self.db.recently_played
        self._logger = getLogger("spotify_advance.mongodb")

    def store_recently_played(self, user_id: str, track_id: str, played_at: datetime) -> bool:
        """
        Store a recently played track in MongoDB.

        Args:
            user_id: Spotify user ID
            track_id: Spotify track ID
            played_at: Timestamp when the track was played

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            track_data = {
                "user_id": user_id,
                "track_id": track_id,
                "played_at": played_at,
            }

            self.recently_played.insert_one(track_data)
            self._logger.info(
                f"Stored recently played track: {track_id} for user: {user_id}")
            return True
        except Exception as e:
            self._logger.error(
                f"Failed to store recently played track: {str(e)}")
            return False

    def get_recently_played(self, user_id: str, limit: int = 10) -> list[TrackRecord]:
        """
        Get recently played tracks for a user.

        Args:
            user_id: Spotify user ID
            limit: Number of tracks to retrieve

        Returns:
            list[TrackRecord]: List of recently played tracks
        """
        try:
            cursor = self.recently_played.find({"user_id": user_id}).sort(
                "played_at", DESCENDING).limit(limit)
            return [TrackRecord(**doc) for doc in cursor]
        except Exception as e:
            self._logger.error(
                f"Failed to get recently played tracks: {str(e)}")
            return []

    def delete_user_recently_played(self, user_id: str) -> bool:
        """
        Delete all recently played tracks for a user.

        Args:
            user_id: Spotify user ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.recently_played.delete_many({"user_id": user_id})
            return True
        except Exception as e:
            self._logger.error(
                f"Failed to delete recently played tracks: {str(e)}")
            return False
