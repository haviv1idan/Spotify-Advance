import logging
from enum import Enum
from functools import lru_cache
from typing import Final

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from yaml import safe_load

logging.getLogger("spotipy").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logging.basicConfig(filename='flask_utils.log', filemode='w', level=logging.DEBUG)


class TermEnum(Enum):
    SHORT = "short_term"
    MEDIUM = "medium_term"
    LONG = "long_term"


DEFAULT_FUNCTIONS = ("user", "current_user_data", "user_top_artists")


def print_func_cache(functions: list[str] | str = None) -> None:
    if not functions:
        functions = DEFAULT_FUNCTIONS
    elif isinstance(functions, str):
        functions = [functions]

    logger.info(f"{functions=}")
    for func in functions:
        _func = globals().get(func, None)
        if not _func:
            continue

        logger.info(f"cache info of {func}: {_func.cache_info()}")


def clear_func_cache(functions: list[str] | str = None) -> None:
    """clear to given functions their cache. if not, it will run for all functions

    :param list[str] | str functions: functions names to clear their cache, defaults to None
    :return None
    """
    if not functions:
        functions = DEFAULT_FUNCTIONS
    elif isinstance(functions, str):
        functions = [functions]

    logger.info(f"{functions=}")
    for func in functions:
        _func = globals().get(func, None)
        if not _func:
            continue

        logger.info(f"clear cache of function: {func}")
        _func.cache_clear()
        logger.info(f"new cache: {_func.cache_info()}")


def read_client_data() -> dict[str, str]:
    """read client data from conf.yml file

    Returns:
        dict[str, str]: client data
    """
    with open("conf.yml", "r") as f:
        data = safe_load(f)
        return data


@lru_cache()
def user() -> Spotify:
    client_data: dict[str, str] = read_client_data()
    client_id: Final[str] = client_data.get("client_id")
    client_secret: Final[str] = client_data.get("client_secret")
    redirect_uri: Final[str] = client_data.get("redirect_uri")

    scopes = [
        "user-read-email, user-library-read",
        "user-top-read",
        "user-read-recently-played",
    ]
    auth_manager = SpotifyOAuth(
        client_id, client_secret, redirect_uri, scope=",".join(scopes)
    )
    sp = Spotify(auth_manager=auth_manager)

    return sp


@lru_cache()
def current_user_data() -> dict:
    """
    returns current user profile using api /me

    Link to API call:
    https://developer.spotify.com/documentation/web-api/reference/get-current-users-profile

    :return dict: current user data
    """
    return user().me()


@lru_cache()
def user_top_artists(
    term: str = TermEnum.SHORT.value, count: int = 20
) -> list[str]:
    """
    returns the top artists of current user in given term of time and count of artists to display

    Link to API call:
    https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks

    :param TermEnum term: Enum of time terms, default is short_term
    :param int count: number of artists to display, default is 20 as api default limit
    :return list[str]: list of artists
    """
    top_artists: dict = user().current_user_top_artists(limit=count, time_range=term)
    top_artists = top_artists["items"]

    return list(map(lambda artist: artist["name"], top_artists))
