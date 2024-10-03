from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from yaml import safe_load
from functools import lru_cache
from typing import Final

@lru_cache()
def read_client_data() -> dict[str, str]:
    """read client data from conf.yml file

    Returns:
        dict[str, str]: client data
    """
    with open('conf.yml', 'r') as f:
        data = safe_load(f)
        return data
    
@lru_cache(maxsize=1)
def user():
    client_data: dict[str, str] = read_client_data()
    client_id: Final[str] = client_data.get('client_id')
    client_secret: Final[str] = client_data.get('client_secret')
    redirect_uri: Final[str] = client_data.get('redirect_uri')

    scopes = ['user-library-read', 'user-top-read', 'user-read-recently-played']
    sp = Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri=redirect_uri,
                                       scope=','.join(scopes)))
    
    return sp