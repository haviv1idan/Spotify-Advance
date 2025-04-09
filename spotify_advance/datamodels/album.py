from spotify_advance.datamodels.artist import Artist


class Album:

    def __init__(self, artists: list[Artist], id: str, uri: str, name: str, popularity: int, images: list[dict], **kwargs):
        self.album_id = id
        self.name = name
        self.uri = uri
        self.artists = artists
        self.popularity = popularity
        self.images = images
