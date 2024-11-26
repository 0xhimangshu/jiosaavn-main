from typing import List
from .track import Track


class Artist:
    """Represents an artist on JioSaavn.
    
    Attributes:
        data (dict): Raw artist data from the API
        tracks (List[Track]): List of tracks by this artist
    """

    def __init__(self, data: dict, tracks: List[Track] = None) -> None:
        """Initialize an Artist object.
        
        Args:
            data (dict): Raw artist data from the API
            tracks (List[Track], optional): List of tracks by this artist. Defaults to None.
        """
        self.data = data
        self._tracks = tracks

    @property
    def id(self) -> str:
        """Get the artist ID.
        
        Returns:
            str: Unique identifier for the artist
        """
        return self.data["id"]

    @property
    def name(self) -> str:
        """Get the artist name.
        
        Returns:
            str: Name of the artist
        """
        return self.data["name"]

    @property
    def image(self) -> str:
        """Get the artist image URL.
        
        Returns:
            str: URL to the artist's image, or None if not available
        """
        return self.data.get("image", None)

    @property
    def url(self) -> str:
        """Get the artist's JioSaavn URL.
        
        Returns:
            str: Permanent URL to the artist's page
        """
        return self.data["perma_url"]

    @property
    def tracks(self) -> List[Track]:
        """Get the list of tracks by this artist.
        
        Returns:
            List[Track]: List of Track objects
        """
        return self._tracks

    @tracks.setter
    def tracks(self, tracks: List[Track]) -> None:
        """Set the list of tracks for this artist.
        
        Args:
            tracks (List[Track]): List of Track objects
        """
        self._tracks = tracks
