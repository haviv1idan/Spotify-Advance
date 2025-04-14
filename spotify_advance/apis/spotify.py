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

    @lru_cache(maxsize=1)
    def get_recently_played(self, limit: int = 20, before: str = None, after: str = None):
        recently_played = []
        tracks = self.sp.current_user_recently_played(
            limit=limit, after=after, before=before)

        while tracks:
            for i, item in enumerate(tracks['items']):
                recently_played.append(item)
                track = item['track']
                if i % 10 == 0:
                    self._logger.debug(
                        i, track['artists'][0]['name'], ' - ', track['name'], end="\n")
                else:
                    self._logger.debug(
                        i, track['artists'][0]['name'], ' - ', track['name'], end=" ")

            if tracks['next']:
                tracks = self.sp.next(tracks)
            else:
                tracks = None

        return recently_played

    @lru_cache(maxsize=1)
    def get_saved_tracks(self, limit: int = 20, offset: int = 0, market: str = None):
        saved_tracks = []
        tracks: list[dict] = self.sp.current_user_saved_tracks(
            limit=limit, offset=offset, market=market)

        while tracks:
            for item in tracks['items']:
                saved_tracks.append(item)

            if tracks['next']:
                tracks = self.sp.next(tracks)
            else:
                tracks = None

        return saved_tracks
