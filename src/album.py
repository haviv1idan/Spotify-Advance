from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Optional

from .artist import Artist


@dataclass
class Album:
    """
    Represents a Spotify album with essential information.

    Attributes:
        id: Spotify ID for the album
        name: Name of the album
        artists: List of artists who created the album
        release_date: Release date of the album
        total_tracks: Total number of tracks in the album
        type: Type of album (album, single, compilation)
        external_urls: Dictionary of external URLs for this album
        href: Spotify Web API endpoint for this album
        uri: Spotify URI for this album
        images: List of album cover images
        genres: List of genres associated with this album
        label: Record label that released the album
        popularity: Album's popularity score (0-100)
    """
    id: str
    name: str
    artists: List[Artist]
    release_date: date
    total_tracks: int
    type: str
    external_urls: Dict[str, str]
    href: str
    uri: str
    images: Optional[List[Dict[str, str]]] = None
    genres: Optional[List[str]] = None
    label: Optional[str] = None
    popularity: Optional[int] = None

    @property
    def spotify_url(self) -> str:
        """Get the Spotify URL for this album."""
        return self.external_urls.get('spotify', '')

    @property
    def main_image_url(self) -> Optional[str]:
        """Get the URL of the album's main cover image."""
        if self.images and len(self.images) > 0:
            return self.images[0].get('url')
        return None

    @property
    def artist_names(self) -> List[str]:
        """Get a list of artist names for this album."""
        return [artist.name for artist in self.artists]

    def __str__(self) -> str:
        """Return a string representation of the album."""
        artists = ', '.join(self.artist_names)
        return f"{self.name} by {artists} ({self.release_date.year})"

    def __repr__(self) -> str:
        """Return a detailed string representation of the album."""
        return f"Album(name='{self.name}', artists={self.artist_names}, release_date={self.release_date}, total_tracks={self.total_tracks})"

    @classmethod
    def from_spotify_dict(cls, data: Dict) -> 'Album':
        """
        Create an Album instance from Spotify API response data.

        Args:
            data: Dictionary containing album data from Spotify API

        Returns:
            Album instance populated with the provided data
        """
        artists = [Artist(**artist_data) for artist_data in data.get('artists', [])]

        # Parse release date
        release_date_str = data.get('release_date', '')
        try:
            year, month, day = map(int, release_date_str.split('-'))
            release_date = date(year, month, day)
        except ValueError:
            # Handle partial dates (some albums only have year)
            release_date = date(int(release_date_str), 1, 1)

        return cls(
            id=data.get('id'),
            name=data.get('name'),
            artists=artists,
            release_date=release_date,
            total_tracks=data.get('total_tracks'),
            type=data.get('type'),
            external_urls=data.get('external_urls', {}),
            href=data.get('href'),
            uri=data.get('uri'),
            images=data.get('images'),
            genres=data.get('genres'),
            label=data.get('label'),
            popularity=data.get('popularity')
        )
