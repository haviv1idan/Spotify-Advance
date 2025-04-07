from pytest import fixture

from spotify_advance.apis import client_data
from spotify_advance.apis.spotify import SpotifyAPI


@fixture(name="spotify_api", scope="session", autouse=True)
def spotify_api_fixture() -> SpotifyAPI:
    return SpotifyAPI(**client_data)


@fixture(name="user_id", scope="session", autouse=True)
def user_id_fixture(spotify_api: SpotifyAPI) -> str:
    return spotify_api.current_user['id']
