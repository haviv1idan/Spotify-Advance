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
        scope="user-read-recently-played",
    )
)


@lru_cache(maxsize=1)
def get_recently_played(limit: int = 50, before: str = None, after: str = None):
    recently_played = []
    tracks = sp.current_user_recently_played(limit=limit, after=after, before=before)
    while tracks:
        for i, item in enumerate(tracks["items"]):
            recently_played.append(item)
            track = item["track"]
            if i % 10 == 0:
                print(i, track["artists"][0]["name"], " - ", track["name"], end="\n")
            else:
                print(i, track["artists"][0]["name"], " - ", track["name"], end=" ")

        if tracks["next"]:
            tracks = sp.next(tracks)
        else:
            tracks = None

    return recently_played


after_unix_time = "1727038800"
recently_played = get_recently_played(after=after_unix_time)
for idx, track in enumerate(recently_played):
    name = track["track"]["name"]
    artist = track["track"]["artists"][0]["name"]
    print(f"{idx}. {artist} - {name}", end="\n")
