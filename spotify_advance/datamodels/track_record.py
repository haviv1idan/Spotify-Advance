from datetime import datetime


class TrackRecord:

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
