from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Artist:
    """
    Represents a Spotify artist with essential information.

    Attributes:
        external_urls: Dictionary of external URLs for this artist
        href: Spotify Web API endpoint for this artist
        id: Spotify ID for this artist
        name: Name of the artist
        type: Type of Spotify object ('artist')
        uri: Spotify URI for this artist
        genres: List of genres associated with this artist
        popularity: Artist's popularity score (0-100)
        followers: Number of followers
        images: List of artist's profile images
    """
    external_urls: Dict[str, str]
    href: str
    id: str
    name: str
    type: str
    uri: str
    genres: Optional[list[str]] = None
    popularity: Optional[int] = None
    followers: Optional[int] = None
    images: Optional[list[Dict[str, str]]] = None

    @property
    def spotify_url(self) -> str:
        """Get the Spotify URL for this artist."""
        return self.external_urls.get('spotify', '')

    @property
    def main_image_url(self) -> Optional[str]:
        """Get the URL of the artist's main profile image."""
        if self.images and len(self.images) > 0:
            return self.images[0].get('url')
        return None

    def __str__(self) -> str:
        """Return a string representation of the artist."""
        return f"{self.name} (ID: {self.id})"

    def __repr__(self) -> str:
        """Return a detailed string representation of the artist."""
        return f"Artist(name='{self.name}', id='{self.id}', popularity={self.popularity})"

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> str:
        return self._id
