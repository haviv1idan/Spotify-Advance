from typing import Final
from yaml import safe_load
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from functools import lru_cache


def read_client_data() -> dict[str, str]:
    with open("conf.yml", "r") as f:
        data = safe_load(f)
        return data


client_data: dict[str, str] = read_client_data()
CLIENT_ID: Final[str] = client_data.get("client_id")
CLIENT_SECRET: Final[str] = client_data.get("client_secret")
REDIRECT_URI: Final[str] = client_data.get("redirect_uri")

# Authenticate with Spotify using OAuth
sp = Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-library-read",
    )
)


@lru_cache(maxsize=1)
def get_saved_tracks():
    saved_tracks = []
    tracks = sp.current_user_saved_tracks()
    while tracks:
        for i, item in enumerate(tracks["items"]):
            saved_tracks.append(item)

        if tracks["next"]:
            tracks = sp.next(tracks)
        else:
            tracks = None
    return saved_tracks


saved_tracks = get_saved_tracks()
for idx, track in enumerate(saved_tracks):
    name = track["track"]["name"]
    artist = track["track"]["artists"][0]["name"]
    print(f"{idx}. {artist} - {name}", end="\n")
