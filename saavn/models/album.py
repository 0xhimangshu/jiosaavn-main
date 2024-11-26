from typing import List

from .track import Track


class Album:
    """Represents a JioSaavn album with its metadata and tracks."""

    def __init__(self, data: dict, tracks: List[Track]) -> None:
        """Initialize an Album instance.
        
        Args:
            data: Dictionary containing album metadata from JioSaavn API
            tracks: List of Track objects belonging to this album
        """
        self.data = data
        self._tracks = tracks

    @property
    def id(self) -> str:
        """Get the unique album ID."""
        return self.data["albumid"]

    @property 
    def title(self) -> str:
        """Get the album title."""
        return self.data["title"]

    @property
    def url(self) -> str:
        """Get the JioSaavn permalink URL for this album."""
        return self.data["perma_url"]

    @property
    def image(self) -> str:
        """Get the album artwork URL."""
        return self.data["image"]

    @property
    def tracks(self) -> List[Track]:
        """Get the list of tracks in this album."""
        return self._tracks

    @tracks.setter
    def tracks(self, tracks: List[Track]) -> None:
        """Set the list of tracks for this album.
        
        Args:
            tracks: List of Track objects to set
        """
        self._tracks = tracks
