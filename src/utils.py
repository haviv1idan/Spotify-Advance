import logging
from enum import Enum
from functools import lru_cache
from json import dump, load
from os.path import exists
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
    term: str = TermEnum.SHORT.value, count: int = 10
) -> list[str]:
    """
    returns the top artists of current user in given term of time and count of artists to display

    Link to API call:
    https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks

    :param TermEnum term: Enum of time terms, default is short_term
    :param int count: number of artists to display, default is 10 as api default limit
    :return list[str]: list of artists
    """
    return user().current_user_top_artists(limit=count, time_range=term)["items"]


@lru_cache()
def user_top_tracks(
    term: str = TermEnum.SHORT.value, count: int = 10
) -> list[str]:
    """
    returns the top tracks of current user in given term of time and count of tracks to display

    Link to API call:
    https://developer.spotify.com/documentation/web-api/reference/get-users-top-tracks-and-tracks

    :param TermEnum term: Enum of time terms, default is short_term
    :param int count: number of tracks to display, default is 10 as api default limit
    :return list[str]: list of tracks
    """
    return user().current_user_top_tracks(limit=count, time_range=term)["items"]


def init_saved_tracks() -> dict[str, dict]:
    """
    Get all current user saved tracks and store them in file

    :return dict[str, dict]: dict of track id and track information
    """

    saved_tracks_dict = {}
    tracks = user().current_user_saved_tracks()

    while tracks:
        for track in tracks['items']:
            saved_tracks_dict[track['track']['id']] = track

        tracks = user().next(tracks) if tracks['next'] else None

    with open('saved_tracks.json', 'w') as f:
        dump(saved_tracks_dict, f)

    return saved_tracks_dict


def user_saved_tracks() -> list[dict]:
    """
    returns the saved tracks of current user

    Link to API call:
    https://developer.spotify.com/documentation/web-api/reference/get-users-saved-tracks

    :return list[dict]: user saved tracks (liked songs)
    """

    # if saved_track.json file isn't exists, will get all user saved tracks
    if not exists('saved_tracks.json'):
        saved_tracks = init_saved_tracks()
        return list(saved_tracks.values())

    # read all saved tracks
    with open('saved_tracks.json', 'r') as f:
        saved_tracks: dict = load(f)

    # get last added saved tracks
    tracks = user().current_user_saved_tracks()

    # iterate on last added track and add to saved track the new track.
    while tracks:

        for track in tracks['items']:
            # if we reach a track we've exist in saved track, stop and return the updated saved tracks
            if track['track']['id'] in saved_tracks:
                return list(saved_tracks.values())

            # in case of track isn't in our saved track, will create a new track and add him to saved tracks.
            saved_tracks[track['track']['id']] = track
            with open('saved_tracks.json', 'w') as f:
                dump(saved_tracks, f)

        # continue to next tracks block or we reach the end.
        tracks = user().next(tracks) if tracks['next'] else None


def user_recommendations(artists: list[str], songs: list[str] = None,
                         genres: list[str] = None, count: int = 20) -> list[dict[str, str]]:
    """
    Get current user recommendations songs based on given artists and songs.

    :param list[str] artists: base artists
    :param list[str] songs: base songs
    :param list[str] genres: base genres
    :param int count: count of songs to return
    :return list[dict[str, str]]: list of recommended songs
    """
    return user().recommendations(seed_artists=artists, seed_genres=genres, seed_tracks=songs, limit=count)['tracks']
