from spotify_advance.datamodels.album import Album
from spotify_advance.datamodels.artist import Artist


class Track:

    def __init__(self, **kwargs):
        self.album = Album(**kwargs['album'])
        self.artists = [Artist(**artist) for artist in kwargs['artists']]
        self.track_id = kwargs['id']
        self.name = kwargs['name']
        self.popularity = kwargs['popularity']
        self.uri = kwargs['uri']
