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

    ### TRACKS ###

    def store_track(self, name: str, track_id: str, popularity: int, uri: str, album: dict, artists: list[dict]) -> tuple[bool, str]:
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
            return False, "Track already exists"

        track_data = {
            "name": name,
            "track_id": track_id,
            "popularity": popularity,
            "uri": uri,
            "album": album['name'],
            "artists": [artist['name'] for artist in artists]
        }

        try:
            self.tracks.insert_one(track_data)
            return True, "Track stored successfully"
        except Exception as e:
            self._logger.error(
                f"Failed to store track: {str(e)}")
            return False, "Failed to store track"

    def get_track(self, track_id: str) -> tuple[dict, str]:
        """
        Get a track from MongoDB.

        Args:
            track_id: Spotify track ID

        Returns:
            Track: Track object
        """
        try:
            track = self.tracks.find_one({"track_id": track_id})
            track['_id'] = str(track['_id'])
            return track, "Track retrieved successfully"
        except Exception as e:
            self._logger.error(
                f"Failed to get track: {str(e)}")
            return None, "Failed to get track"

    def get_all_tracks(self) -> tuple[list[dict], str]:
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
            return [], "Failed to get all tracks"

    def delete_track(self, track_id: str) -> tuple[bool, str]:
        """
        Delete a track from MongoDB.

        Args:
            track_id: Spotify track ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.tracks.delete_one({"id": track_id})
            return True, "Track deleted successfully"
        except Exception as e:
            self._logger.error(
                f"Failed to delete track: {str(e)}")
            return False, "Failed to delete track"

    ### RECENTLY PLAYED ###

    def store_recently_played(self, user_id: str, track_id: str, played_at: datetime) -> tuple[bool, str]:
        """
        Store a recently played track in MongoDB.

        Args:
            user_id: Spotify user ID
            track_id: Spotify track ID
            played_at: Timestamp when the track was played

        Returns:
            bool: True if successful, False otherwise
        """
        track_data = {
            "user_id": user_id,
            "track_id": track_id,
            "played_at": played_at,
        }

        try:
            if self.recently_played.find_one({"user_id": user_id, "track_id": track_id}):
                self._logger.info(
                    f"Recently played track already exists: {track_id} for user: {user_id}")
                return False, "Recently played track already exists"

            self.recently_played.insert_one(track_data)
            self._logger.info(
                f"Stored recently played track: {track_id} for user: {user_id}")
            return True, "Recently played track stored successfully"
        except Exception as e:
            self._logger.error(
                f"Failed to store recently played track: {str(e)}")
            return False, "Failed to store recently played track"

    def get_recently_played(self, user_id: str, limit: int = 10) -> tuple[list[TrackRecord], str]:
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
            return [TrackRecord(**doc) for doc in cursor], "Recently played tracks retrieved successfully"
        except Exception as e:
            self._logger.error(
                f"Failed to get recently played tracks: {str(e)}")
            return [], "Failed to get recently played tracks"

    def delete_user_recently_played(self, user_id: str) -> tuple[bool, str]:
        """
        Delete all recently played tracks for a user.

        Args:
            user_id: Spotify user ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.recently_played.delete_many({"user_id": user_id})
            return True, "Recently played tracks deleted successfully"
        except Exception as e:
            self._logger.error(
                f"Failed to delete recently played tracks: {str(e)}")
            return False, "Failed to delete recently played tracks"

    ### SAVED TRACKS ###

    def store_saved_track(self, user_id: str, track_id: str, added_at: datetime) -> tuple[bool, str]:
        """
        Store a saved track in MongoDB.

        Args:
            user_id: Spotify user ID
            track_id: Spotify track ID
            added_at: Timestamp when the track was added

        Returns:
            bool: True if successful, False otherwise
        """
        track_data = {
            "user_id": user_id,
            "track_id": track_id,
            "added_at": added_at,
        }

        try:
            if self.saved_tracks.find_one({"user_id": user_id, "track_id": track_id}):
                self._logger.info(
                    f"Saved track already exists: {track_id} for user: {user_id}")
                return False, "Saved track already exists"

            self.saved_tracks.insert_one(track_data)
            self._logger.info(
                f"Stored saved track: {track_id} for user: {user_id}")
            return True, "Saved track stored successfully"
        except Exception as e:
            self._logger.error(
                f"Failed to store saved track: {str(e)}")
            return False, "Failed to store saved track"

    def get_saved_tracks(self, user_id: str) -> tuple[list[SavedTrack], str]:
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
            return [SavedTrack(**doc) for doc in cursor], "Saved tracks retrieved successfully"
        except Exception as e:
            self._logger.error(
                f"Failed to get saved tracks: {str(e)}")
            return [], "Failed to get saved tracks"

    def delete_user_saved_tracks(self, user_id: str, track_id: str) -> tuple[bool, str]:
        """
        Delete a saved track for a user.

        Args:
            user_id: Spotify user ID
            track_id: Spotify track ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.saved_tracks.delete_one(
                {"user_id": user_id, "track_id": track_id})
            return True, "Saved track deleted successfully"
        except Exception as e:
            self._logger.error(
                f"Failed to delete saved track: {str(e)}")
            return False, "Failed to delete saved track"
