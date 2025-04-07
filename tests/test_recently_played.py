import pytest
from requests import delete, get, post

from spotify_advance.apis.spotify import SpotifyAPI


@pytest.mark.test_recently_played
class TestRecentlyPlayed:

    def setup_method(self):
        self.url = "http://localhost:8000/recently_played"

    def test_store_recently_played(self, spotify_api: SpotifyAPI, user_id: str):
        recently_played = spotify_api.get_recently_played(
            limit=1).get('items', [])
        assert len(recently_played) == 1, "Expected 1 recently played track"

        track_id = recently_played[0]['track']['id']
        played_at = recently_played[0]['played_at']

        response = post(self.url, json={
                        'user_id': user_id, 'track_id': track_id, 'played_at': played_at})
        assert response.status_code == 200, "Expected status code 200"

    def test_get_recently_played(self, user_id: str):
        response = get(self.url + f"/{user_id}")
        assert response.status_code == 200, "Expected status code 200"

    def test_delete_user_recently_played(self, user_id: str):
        response = delete(self.url + f"/{user_id}")
        assert response.status_code == 200, "Expected status code 200"
