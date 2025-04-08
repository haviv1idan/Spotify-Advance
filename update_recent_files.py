from spotify_advance.apis import client_data
from spotify_advance.apis.spotify import SpotifyAPI
from spotify_advance.utils import get_one_week_before


def main():
    spotify_api = SpotifyAPI(**client_data)
    one_week_before = get_one_week_before()
    recently_played = spotify_api.get_recently_played(
        limit=50, after=one_week_before)
    print(recently_played)


main()
