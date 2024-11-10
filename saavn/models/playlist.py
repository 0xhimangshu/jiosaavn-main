from typing import List
from .track import Track


class Playlist:
    def __init__(self, data, tracks: List[Track]):
        self.data = data
        self.tracks = tracks

    @property
    def id(self):
        return self.data["listid"]

    @property
    def title(self):
        return self.data["listname"]

    @property
    def url(self):
        return self.data["perma_url"]

    @property
    def image(self):
        return self.data["image"]

    @property
    def tracks(self) -> List[Track]:
        return self._tracks

    @tracks.setter
    def tracks(self, tracks: List[Track]):
        self._tracks = tracks
