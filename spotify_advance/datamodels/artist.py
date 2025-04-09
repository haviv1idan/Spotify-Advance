class Artist:

    def __init__(self, id: str, name: str, uri: str, **kwargs) -> None:
        self.artist_id = id
        self.name = name
        self.uri = uri
