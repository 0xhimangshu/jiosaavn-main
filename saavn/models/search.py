from typing import List, Optional

from .track import Track


class SearchResult:
    def __init__(
        self,
        tracks: Optional[List[Track]] = None,
        albums: Optional[List[Track]] = None,
        artists: Optional[List[Track]] = None,
        playlists: Optional[List[Track]] = None
    ):
        self.tracks = tracks
        self.albums = albums
        self.artists = artists
        self.playlists = playlists

