from unittest.mock import MagicMock, patch

import pytest

from spotify_advance.apis.spotify import SpotifyAPI


class TestSpotifyAPIMock:
    """Unit tests for SpotifyAPI using mocks."""

    @pytest.fixture
    def mock_spotify_api(self):
        """Create a mocked SpotifyAPI instance."""
        with patch('spotify_advance.apis.spotify.SpotifyOAuth'), \
                patch('spotify_advance.apis.spotify.Spotify'):
            api = SpotifyAPI(
                client_id="mock_client_id",
                client_secret="mock_client_secret",
                redirect_uri="mock_redirect_uri"
            )
            # Mock the sp client
            api.sp = MagicMock()
            return api

    def test_current_user(self, mock_spotify_api):
        """Test that current_user returns the result from Spotify client."""
        # Mock the current_user response
        mock_user = {"id": "test_user", "display_name": "Test User"}
        mock_spotify_api.sp.current_user.return_value = mock_user

        # Call the method
        result = mock_spotify_api.current_user

        # Verify the result
        assert result == mock_user
        mock_spotify_api.sp.current_user.assert_called_once()

    def test_get_recently_played(self, mock_spotify_api):
        """Test get_recently_played method with mocked data."""
        # Mock the API responses
        mock_track = {
            "track": {
                "id": "track_id_1",
                "name": "Test Track",
                "artists": [{"name": "Test Artist"}]
            },
            "played_at": "2023-01-01T00:00:00Z"
        }

        # First response with one item and a next page
        mock_response_1 = {
            "items": [mock_track],
            "next": "next_page_url"
        }

        # Second response with no next page
        mock_response_2 = {
            "items": [],
            "next": None
        }

        # Setup the mock responses
        mock_spotify_api.sp.current_user_recently_played.return_value = mock_response_1
        mock_spotify_api.sp.next.return_value = mock_response_2

        # Call the method
        result = mock_spotify_api.get_recently_played(limit=10)

        # Verify the result
        assert len(result) == 1
        assert result[0] == mock_track
        mock_spotify_api.sp.current_user_recently_played.assert_called_once_with(
            limit=10, after=None, before=None
        )
        mock_spotify_api.sp.next.assert_called_once_with(mock_response_1)

    def test_get_saved_tracks(self, mock_spotify_api):
        """Test get_saved_tracks method with mocked data."""
        # Mock the API responses
        mock_item = {
            "track": {
                "id": "track_id_1",
                "name": "Test Saved Track",
                "artists": [{"name": "Test Artist"}]
            },
            "added_at": "2023-01-01T00:00:00Z"
        }

        # First response with one item and a next page
        mock_response_1 = {
            "items": [mock_item],
            "next": "next_page_url"
        }

        # Second response with no next page
        mock_response_2 = {
            "items": [],
            "next": None
        }

        # Setup the mock responses
        mock_spotify_api.sp.current_user_saved_tracks.return_value = mock_response_1
        mock_spotify_api.sp.next.return_value = mock_response_2

        # Call the method
        result = mock_spotify_api.get_saved_tracks(limit=10)

        # Verify the result
        assert len(result) == 1
        assert result[0] == mock_item
        mock_spotify_api.sp.current_user_saved_tracks.assert_called_once_with(
            limit=10, offset=0, market=None
        )
        mock_spotify_api.sp.next.assert_called_once_with(mock_response_1)
