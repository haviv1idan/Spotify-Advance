from enum import Enum
from typing import Any, Dict, List

from spotipy import Spotify
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOAuth

from src import logger

from .album import Album
from .artist import Artist
from .track import Track


class TimeRange(Enum):
    """Time ranges for Spotify API queries."""
    SHORT_TERM = 'short_term'  # Last 4 weeks
    MEDIUM_TERM = 'medium_term'  # Last 6 months
    LONG_TERM = 'long_term'  # All time

    def __str__(self) -> str:
        return self.value


class SpotifyAPIError(Exception):
    """Custom exception for Spotify API related errors."""
    pass


class API:
    """
    A wrapper class for the Spotify Web API that provides simplified access
    to common Spotify functionality.
    """

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        """
        Initialize the Spotify API wrapper.

        Args:
            client_id: Spotify API client ID
            client_secret: Spotify API client secret
            redirect_uri: OAuth redirect URI

        Raises:
            SpotifyAPIError: If authentication fails
        """
        try:
            self.client_id = client_id
            self.client_secret = client_secret
            self.redirect_uri = redirect_uri

            scopes = [
                "user-read-email",
                "user-library-read",
                "user-top-read",
                "user-read-recently-played",
                "playlist-read-private",
                "playlist-modify-public",
                "playlist-modify-private",
                "user-follow-read",
                "user-follow-modify",
                "user-library-modify"
            ]

            self.auth_manager = SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope=",".join(scopes)
            )
            self.sp = Spotify(auth_manager=self.auth_manager)
            logger.info("Successfully initialized Spotify API client")
        except Exception as e:
            logger.error(f"Failed to initialize Spotify API: {str(e)}")
            raise SpotifyAPIError(f"Failed to initialize Spotify API: {str(e)}")

    def _handle_api_error(self, operation: str) -> None:
        """
        Handle Spotify API errors and provide meaningful error messages.

        Args:
            operation: Description of the operation that failed

        Raises:
            SpotifyAPIError: With detailed error message
        """
        logger.error(f"Error during {operation}")
        raise SpotifyAPIError(f"Failed to {operation}")

    @property
    def current_user(self) -> Dict[str, Any]:
        """
        Get the current user's Spotify profile.

        Returns:
            Dict containing user profile information

        Raises:
            SpotifyAPIError: If unable to fetch user profile
        """
        try:
            return self.sp.current_user()
        except SpotifyException as e:
            self._handle_api_error(f"fetch user profile: {str(e)}")

    def get_top_tracks(self, time_range: TimeRange = TimeRange.MEDIUM_TERM, limit: int = 20) -> List[Track]:
        """
        Get the user's top tracks for a given time range.

        Args:
            time_range: Time range for the query (default: MEDIUM_TERM)
            limit: Number of tracks to return (default: 20, max: 50)

        Returns:
            List of Track objects representing the user's top tracks

        Raises:
            SpotifyAPIError: If unable to fetch top tracks
        """
        try:
            response = self.sp.current_user_top_tracks(
                time_range=time_range.value,
                limit=min(limit, 50)
            )
            return [Track.from_spotify_dict(item) for item in response['items']]
        except SpotifyException as e:
            self._handle_api_error(f"fetch top tracks: {str(e)}")

    def get_top_artists(self, time_range: TimeRange = TimeRange.MEDIUM_TERM, limit: int = 20) -> List[Artist]:
        """
        Get the user's top artists for a given time range.

        Args:
            time_range: Time range for the query (default: MEDIUM_TERM)
            limit: Number of artists to return (default: 20, max: 50)

        Returns:
            List of Artist objects representing the user's top artists

        Raises:
            SpotifyAPIError: If unable to fetch top artists
        """
        try:
            response = self.sp.current_user_top_artists(
                time_range=time_range.value,
                limit=min(limit, 50)
            )
            return [Artist(**item) for item in response['items']]
        except SpotifyException as e:
            self._handle_api_error(f"fetch top artists: {str(e)}")

    def create_playlist(self, name: str, description: str = "", public: bool = False) -> Dict[str, Any]:
        """
        Create a new playlist for the current user.

        Args:
            name: Name of the playlist
            description: Optional description of the playlist
            public: Whether the playlist should be public (default: False)

        Returns:
            Dict containing the created playlist information

        Raises:
            SpotifyAPIError: If unable to create playlist
        """
        try:
            user_id = self.current_user['id']
            return self.sp.user_playlist_create(
                user=user_id,
                name=name,
                public=public,
                description=description
            )
        except SpotifyException as e:
            self._handle_api_error(f"create playlist: {str(e)}")

    def add_tracks_to_playlist(self, playlist_id: str, track_ids: List[str]) -> bool:
        """
        Add tracks to an existing playlist.

        Args:
            playlist_id: Spotify ID of the playlist
            track_ids: List of Spotify track IDs to add

        Returns:
            True if successful, raises exception otherwise

        Raises:
            SpotifyAPIError: If unable to add tracks to playlist
        """
        try:
            self.sp.playlist_add_items(playlist_id, track_ids)
            logger.info(f"Successfully added {len(track_ids)} tracks to playlist {playlist_id}")
            return True
        except SpotifyException as e:
            self._handle_api_error(f"add tracks to playlist: {str(e)}")

    def get_recently_played(self, limit: int = 20) -> List[Track]:
        """
        Get the user's recently played tracks.

        Args:
            limit: Number of tracks to return (default: 20, max: 50)

        Returns:
            List of Track objects representing recently played tracks

        Raises:
            SpotifyAPIError: If unable to fetch recently played tracks
        """
        try:
            response = self.sp.current_user_recently_played(limit=min(limit, 50))
            return [Track.from_spotify_dict(item['track']) for item in response['items']]
        except SpotifyException as e:
            self._handle_api_error(f"fetch recently played tracks: {str(e)}")

    def search(self, query: str, types: List[str] = ['track', 'artist', 'album'], limit: int = 10) -> Dict[str, List]:
        """
        Search for tracks, artists, albums, or playlists.

        Args:
            query: Search query string
            types: List of item types to search for (default: ['track', 'artist', 'album'])
            limit: Maximum number of items to return per type (default: 10)

        Returns:
            Dictionary containing search results for each type

        Raises:
            SpotifyAPIError: If unable to perform search
        """
        try:
            response = self.sp.search(q=query, limit=limit, type=','.join(types))
            results = {}

            if 'tracks' in response:
                results['tracks'] = [Track.from_spotify_dict(item) for item in response['tracks']['items']]
            if 'artists' in response:
                results['artists'] = [Artist(**item) for item in response['artists']['items']]
            if 'albums' in response:
                results['albums'] = [Album.from_spotify_dict(item) for item in response['albums']['items']]

            return results
        except SpotifyException as e:
            self._handle_api_error(f"perform search: {str(e)}")

    def get_artist(self, artist_id: str) -> Artist:
        """
        Get detailed information about a specific artist.

        Args:
            artist_id: Spotify ID of the artist

        Returns:
            Artist object containing detailed information

        Raises:
            SpotifyAPIError: If unable to fetch artist information
        """
        try:
            response = self.sp.artist(artist_id)
            return Artist(**response)
        except SpotifyException as e:
            self._handle_api_error(f"fetch artist information: {str(e)}")

    def get_album(self, album_id: str) -> Album:
        """
        Get detailed information about a specific album.

        Args:
            album_id: Spotify ID of the album

        Returns:
            Album object containing detailed information

        Raises:
            SpotifyAPIError: If unable to fetch album information
        """
        try:
            response = self.sp.album(album_id)
            return Album.from_spotify_dict(response)
        except SpotifyException as e:
            self._handle_api_error(f"fetch album information: {str(e)}")

    def get_track(self, track_id: str) -> Track:
        """
        Get detailed information about a specific track.

        Args:
            track_id: Spotify ID of the track

        Returns:
            Track object containing detailed information

        Raises:
            SpotifyAPIError: If unable to fetch track information
        """
        try:
            response = self.sp.track(track_id)
            return Track.from_spotify_dict(response)
        except SpotifyException as e:
            self._handle_api_error(f"fetch track information: {str(e)}")

    def get_user_playlists(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get the current user's playlists.

        Args:
            limit: Maximum number of playlists to return (default: 50)

        Returns:
            List of dictionaries containing playlist information

        Raises:
            SpotifyAPIError: If unable to fetch user playlists
        """
        try:
            response = self.sp.current_user_playlists(limit=limit)
            return response['items']
        except SpotifyException as e:
            self._handle_api_error(f"fetch user playlists: {str(e)}")

    def follow_artist(self, artist_id: str) -> bool:
        """
        Follow a Spotify artist.

        Args:
            artist_id: Spotify ID of the artist to follow

        Returns:
            True if successful

        Raises:
            SpotifyAPIError: If unable to follow artist
        """
        try:
            self.sp.user_follow_artists([artist_id])
            return True
        except SpotifyException as e:
            self._handle_api_error(f"follow artist: {str(e)}")

    def unfollow_artist(self, artist_id: str) -> bool:
        """
        Unfollow a Spotify artist.

        Args:
            artist_id: Spotify ID of the artist to unfollow

        Returns:
            True if successful

        Raises:
            SpotifyAPIError: If unable to unfollow artist
        """
        try:
            self.sp.user_unfollow_artists([artist_id])
            return True
        except SpotifyException as e:
            self._handle_api_error(f"unfollow artist: {str(e)}")

    def save_tracks(self, track_ids: List[str]) -> bool:
        """
        Save tracks to the user's library.

        Args:
            track_ids: List of Spotify track IDs to save

        Returns:
            True if successful

        Raises:
            SpotifyAPIError: If unable to save tracks
        """
        try:
            self.sp.current_user_saved_tracks_add(track_ids)
            return True
        except SpotifyException as e:
            self._handle_api_error(f"save tracks: {str(e)}")

    def remove_saved_tracks(self, track_ids: List[str]) -> bool:
        """
        Remove tracks from the user's library.

        Args:
            track_ids: List of Spotify track IDs to remove

        Returns:
            True if successful

        Raises:
            SpotifyAPIError: If unable to remove tracks
        """
        try:
            self.sp.current_user_saved_tracks_delete(track_ids)
            return True
        except SpotifyException as e:
            self._handle_api_error(f"remove saved tracks: {str(e)}")
