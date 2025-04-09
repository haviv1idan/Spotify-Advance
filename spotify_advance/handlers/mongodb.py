from datetime import datetime
from logging import getLogger

from pymongo import DESCENDING, MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from spotify_advance.datamodels.saved_track import SavedTrack
from spotify_advance.datamodels.track_record import TrackRecord


class MongoDBHandler:

    def __init__(self, uri: str):
        self.client = MongoClient(uri)
        self.db: Database = self.client.spotify_advance
        self.tracks: Collection = self.db.tracks
        self.recently_played: Collection = self.db.recently_played
        self.saved_tracks: Collection = self.db.saved_tracks
        self._logger = getLogger("spotify_advance.mongodb")

    def store_track(self, name: str, track_id: str, popularity: int, uri: str, album: dict, artists: list[dict]) -> bool:
        """
        Store a track in MongoDB.

        Args:
            name: Track name
            id: Track ID
            popularity: Track popularity
            uri: Track URI
            album: Track album
            artists: Track artists

        Returns:
            bool: True if successful, False otherwise
        """
        if self.tracks.find_one({"track_id": track_id}):
            self._logger.info(
                f"Track already exists: {track_id}")
            return False

        try:
            self.tracks.insert_one({
                "name": name,
                "track_id": track_id,
                "popularity": popularity,
                "uri": uri,
                "album": album['name'],
                "artists": [artist['name'] for artist in artists]
            })
            return True
        except Exception as e:
            self._logger.error(
                f"Failed to store track: {str(e)}")
            return False

    # def get_track(self, track_id: str) -> Track:
    #    """
    #    Get a track from MongoDB.

    #    Args:
    #        track_id: Spotify track ID

    #    Returns:
    #        Track: Track object
    #    """
    #    try:
    #        return Track(**self.tracks.find_one({"track_id": track_id}))
    #    except Exception as e:
    #        self._logger.error(
    #            f"Failed to get track: {str(e)}")
    #        return None

    def get_all_tracks(self):
        """
        Get all tracks from MongoDB.

        Returns:
            list[Track]: List of all tracks
        """
        try:
            cursor = self.tracks.find()
            return [TrackRecord(**doc).__dict__ for doc in cursor]
        except Exception as e:
            self._logger.error(
                f"Failed to get all tracks: {str(e)}")
            return []

    def delete_track(self, track_id: str) -> bool:
        """
        Delete a track from MongoDB.

        Args:
            track_id: Spotify track ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.tracks.delete_one({"id": track_id})
            return True
        except Exception as e:
            self._logger.error(
                f"Failed to delete track: {str(e)}")
            return False

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

    def store_saved_track(self, user_id: str, track_id: str, added_at: datetime) -> bool:
        """
        Store a saved track in MongoDB.

        Args:
            user_id: Spotify user ID
            track_id: Spotify track ID
            added_at: Timestamp when the track was added

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            track_data = {
                "user_id": user_id,
                "track_id": track_id,
                "added_at": added_at,
            }
            self.saved_tracks.insert_one(track_data)
            self._logger.info(
                f"Stored saved track: {track_id} for user: {user_id}")
            return True
        except Exception as e:
            self._logger.error(
                f"Failed to store saved track: {str(e)}")
            return False

    def get_saved_tracks(self, user_id: str) -> list[SavedTrack]:
        """
        Get saved tracks for a user.

        Args:
            user_id: Spotify user ID
            limit: Number of tracks to retrieve

        Returns:
            list[SavedTrack]: List of saved tracks
        """
        try:
            cursor = self.saved_tracks.find({"user_id": user_id}).sort(
                "added_at", DESCENDING)
            return [SavedTrack(**doc) for doc in cursor]
        except Exception as e:
            self._logger.error(
                f"Failed to get saved tracks: {str(e)}")
            return []
