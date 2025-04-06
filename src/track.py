from dataclasses import dataclass
from typing import Dict, List, Optional

from .album import Album
from .artist import Artist


@dataclass
class Track:
    """
    Represents a Spotify track with essential information.

    Attributes:
        id: Spotify ID for the track
        name: Name of the track
        artists: List of artists who performed the track
        album: Album containing this track
        duration_ms: Duration of the track in milliseconds
        popularity: Track's popularity score (0-100)
        preview_url: URL to a 30-second preview of the track
        track_number: Position of the track in its album
        external_urls: Dictionary of external URLs for this track
        href: Spotify Web API endpoint for this track
        uri: Spotify URI for this track
        explicit: Whether the track has explicit content
        is_local: Whether the track is from local files
        disc_number: Position of the disc in the album
    """
    id: str
    name: str
    artists: List[Artist]
    album: Album
    duration_ms: int
    popularity: int
    track_number: int
    external_urls: Dict[str, str]
    href: str
    uri: str
    explicit: bool
    is_local: bool
    disc_number: int
    preview_url: Optional[str] = None

    @property
    def spotify_url(self) -> str:
        """Get the Spotify URL for this track."""
        return self.external_urls.get('spotify', '')

    @property
    def duration_seconds(self) -> float:
        """Get the track duration in seconds."""
        return self.duration_ms / 1000.0

    @property
    def duration_minutes(self) -> float:
        """Get the track duration in minutes."""
        return self.duration_seconds / 60.0

    @property
    def duration_formatted(self) -> str:
        """Get the track duration formatted as MM:SS."""
        total_seconds = int(self.duration_seconds)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"

    @property
    def artist_names(self) -> List[str]:
        """Get a list of artist names for this track."""
        return [artist.name for artist in self.artists]

    def __str__(self) -> str:
        """Return a string representation of the track."""
        artists = ', '.join(self.artist_names)
        return f"{self.name} by {artists} ({self.duration_formatted})"

    def __repr__(self) -> str:
        """Return a detailed string representation of the track."""
        return f"Track(name='{self.name}', artists={self.artist_names}, duration={self.duration_formatted}, popularity={self.popularity})"

    @classmethod
    def from_spotify_dict(cls, data: Dict, include_album: bool = True) -> 'Track':
        """
        Create a Track instance from Spotify API response data.

        Args:
            data: Dictionary containing track data from Spotify API
            include_album: Whether to include full album data (default: True)

        Returns:
            Track instance populated with the provided data
        """
        artists = [Artist(**artist_data) for artist_data in data.get('artists', [])]

        album_data = data.get('album') if include_album else None
        album = Album.from_spotify_dict(album_data) if album_data else None

        return cls(
            id=data.get('id'),
            name=data.get('name'),
            artists=artists,
            album=album,
            duration_ms=data.get('duration_ms'),
            popularity=data.get('popularity', 0),
            track_number=data.get('track_number'),
            external_urls=data.get('external_urls', {}),
            href=data.get('href'),
            uri=data.get('uri'),
            explicit=data.get('explicit', False),
            is_local=data.get('is_local', False),
            disc_number=data.get('disc_number', 1),
            preview_url=data.get('preview_url')
        )
