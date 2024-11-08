from typing import Final

import spotipy
import yaml
from spotipy.oauth2 import SpotifyOAuth


def read_client_data() -> dict[str, str]:
    with open("conf.yml", "r") as f:
        data = yaml.safe_load(f)
        return data


client_data: dict[str, str] = read_client_data()
CLIENT_ID: Final[str] = client_data.get("client_id")
CLIENT_SECRET: Final[str] = client_data.get("client_secret")
REDIRECT_URI: Final[str] = client_data.get("redirect_uri")

# Authenticate with Spotify using OAuth
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-library-read",
    )
)

# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])
