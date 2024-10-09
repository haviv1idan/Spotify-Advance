import logging
from typing import Final

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from yaml import safe_load

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename="logs/top_artists.log", filemode="w")


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
        scope="user-top-read",
    )
)


for sp_range in ["short_term", "medium_term", "long_term"]:
    logger.info(f"Range: {sp_range}")

    results = sp.current_user_top_artists(time_range=sp_range, limit=10)

    for i, item in enumerate(results["items"]):
        logger.info(f"{i}, {item['name']}")

    logger.info("\n")
