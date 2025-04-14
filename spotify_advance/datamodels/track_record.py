from datetime import datetime


class TrackRecord:

    def __init__(self, _id: object, name: str, track_id: str, popularity: int, uri: str, album: dict, artists: list[dict]):
        self._id = str(_id)
        self.name = name
        self.track_id = track_id
        self.popularity = popularity
        self.uri = uri
        self.album = album
        self.artists = artists

    def __str__(self):
        return f"{self.name} - {self.track_id} - {self.popularity} - {self.uri} - {self.album} - {self.artists}"

    def __repr__(self):
        return f"{self.name} - {self.track_id} - {self.popularity} - {self.uri} - {self.album} - {self.artists}"

    def __eq__(self, other):
        return self.name == other.name and self.track_id == other.track_id and self.popularity == other.popularity and self.uri == other.uri and self.album == other.album and self.artists == other.artists

    def __hash__(self):
        return hash((self.name, self.track_id, self.popularity, self.uri, self.album, self.artists))


class RecentlyPlayedTrackRecord:

    def __init__(self, _id: object, user_id: str, track_id: str, played_at: datetime):
        self._id = str(_id)
        self.user_id = user_id
        self.track_id = track_id
        self.played_at = played_at

    def __str__(self):
        return f"{self.user_id} - {self.track_id} - {self.played_at}"

    def __repr__(self):
        return f"{self.user_id} - {self.track_id} - {self.played_at}"

    def __eq__(self, other):
        return self.user_id == other.user_id and self.track_id == other.track_id and self.played_at == other.played_at

    def __hash__(self):
        return hash((self.user_id, self.track_id, self.played_at))
