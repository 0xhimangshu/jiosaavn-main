from typing import List
from .track import Track


class Playlist:
    """Represents a JioSaavn playlist with its metadata and tracks.
    
    Attributes:
        data: Dictionary containing playlist metadata
        tracks: List of Track objects in the playlist
    """
    
    def __init__(self, data: dict, tracks: List[Track]) -> None:
        """Initialize a new Playlist instance.
        
        Args:
            data: Dictionary containing playlist metadata
            tracks: List of Track objects to include in the playlist
        """
        self.data = data
        self.tracks = tracks

    @property
    def id(self) -> str:
        """Get the unique identifier of the playlist.
        
        Returns:
            The playlist ID as a string
        """
        return self.data["listid"]

    @property 
    def title(self) -> str:
        """Get the title of the playlist.
        
        Returns:
            The playlist title as a string
        """
        return self.data["listname"]

    @property
    def url(self) -> str:
        """Get the permanent URL of the playlist.
        
        Returns:
            The playlist URL as a string
        """
        return self.data["perma_url"]

    @property
    def image(self) -> str:
        """Get the image URL of the playlist.
        
        Returns:
            The playlist image URL as a string
        """
        return self.data["image"]

    @property
    def tracks(self) -> List[Track]:
        """Get the list of tracks in the playlist.
        
        Returns:
            List of Track objects
        """
        return self._tracks

    @tracks.setter 
    def tracks(self, tracks: List[Track]) -> None:
        """Set the list of tracks in the playlist.
        
        Args:
            tracks: List of Track objects to set
        """
        self._tracks = tracks
