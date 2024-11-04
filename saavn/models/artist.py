from typing import List
from .track import Track
from .album import Album
from .playlist import Playlist

class Artist:
    def __init__(self, data: dict, tracks: List[Track]):
        self.data = data
        self._tracks = tracks

    @property
    def id(self) -> str:
        return self.data['id']  
    
    @property
    def name(self) -> str:
        return self.data['name']
    
    @property
    def image(self) -> str:
        return self.data['image']
    
    @property
    def url(self) -> str:
        return self.data['perma_url']
    
    @property
    def tracks(self) -> List[Track]:
        return self._tracks
    
    @tracks.setter
    def tracks(self, tracks: List[Track]):
        self._tracks = tracks