from functools import lru_cache
from logging import getLogger

from spotipy import Spotify, SpotifyOAuth


class SpotifyAPI:

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        scopes = [
            "user-read-email",
            "user-library-read",
            "user-top-read",
            "user-read-recently-played"
        ]

        self.auth_manager = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=scopes
        )

        self.sp = Spotify(auth_manager=self.auth_manager)
        self._logger = getLogger("spotify_advance.api")

    @property
    @lru_cache(maxsize=1)
    def current_user(self):
        return self.sp.current_user()

    def get_recently_played(self, limit: int = 20) -> dict:
        return self.sp.current_user_recently_played(limit=limit)
