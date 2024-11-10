from typing import List

from .track import Track


class Album:
    def __init__(self, data: dict, tracks: List[Track]):
        self.data = data
        self._tracks = tracks

    @property
    def id(self) -> str:
        return self.data["albumid"]

    @property
    def title(self) -> str:
        return self.data["title"]

    @property
    def url(self) -> str:
        return self.data["perma_url"]

    @property
    def image(self) -> str:
        return self.data["image"]

    @property
    def tracks(self) -> List[Track]:
        return self._tracks

    @tracks.setter
    def tracks(self, tracks: List[Track]):
        self._tracks = tracks
