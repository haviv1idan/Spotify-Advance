# generate a playlists for each time range.

import logging
from typing import Final

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from yaml import safe_load

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename="my_top_tracks.log", filemode="w")


def read_client_data() -> dict[str, str]:
    with open("conf.yml", "r") as f:
        data = safe_load(f)
        return data


client_data: dict[str, str] = read_client_data()
CLIENT_ID: Final[str] = client_data.get("client_id")
CLIENT_SECRET: Final[str] = client_data.get("client_secret")
REDIRECT_URI: Final[str] = client_data.get("redirect_uri")

sp = Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-top-read,playlist-modify-private,user-library-read",
    )
)

# get the user's username
username = sp.me()["id"]
logger.info(f"{username=}")

ranges_items = {"short_term": [], "medium_term": [], "long_term": []}

for sp_range in ranges_items.keys():
    logger.info(f"Range: {sp_range}")

    results = sp.current_user_top_tracks(time_range=sp_range, limit=50)

    for i, item in enumerate(results["items"]):
        logger.info(f"{i}. {item['name']} - {item['artists'][0]['name']}")
        ranges_items[sp_range].append(item["id"])

    logger.info("-" * 20)

    # Create a playlist with the representative tracks
    playlist = sp.user_playlist_create(
        user=username, name=f"Personalized {sp_range} Playlist", public=False
    )
    sp.playlist_add_items(playlist_id=playlist["id"], items=ranges_items[sp_range])

    # Print the URL of the created playlist
    print(
        f"Playlist created successfully. You can access it at: {playlist['external_urls']['spotify']}"
    )
