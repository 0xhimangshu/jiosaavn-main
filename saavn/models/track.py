from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from saavn.models.artist import Artist


class Track:
    """Represents a music track from JioSaavn."""

    def __init__(self, data: dict) -> None:
        """Initialize a Track object.

        Args:
            data: Raw track data from JioSaavn API
        """
        self.data = data

    @property
    def id(self) -> str:
        """Get the track's permanent ID.

        Returns:
            The track's permanent ID extracted from its URL
        """
        return self.data["perma_url"].split("/")[-1]

    @property
    def pid(self) -> str:
        """Get the track's platform ID.

        Returns:
            The track's platform-specific ID
        """
        return self.data["id"]

    @property
    def title(self) -> Optional[str]:
        """Get the track's title.

        Returns:
            The track title with proper quote formatting, or None if not found
        """
        if self.data.get("title"):
            return self.data["title"].replace("&quot;", '"')
        elif self.data.get("song"):
            return self.data["song"].replace("&quot;", '"')
        return None

    @property
    def url(self) -> Optional[str]:
        """Get the track's URL.

        Returns:
            The track's permanent or regular URL, or None if not found
        """
        if self.data.get("perma_url"):
            return self.data["perma_url"]
        elif self.data.get("url"):
            return self.data["url"]
        return None

    @property
    def image(self) -> str:
        """Get the track's cover image URL.

        Returns:
            URL of the track's cover image
        """
        return self.data["image"]

    @property
    def duration(self) -> Optional[int]:
        """Get the track's duration in seconds.

        Returns:
            Duration in seconds, or None if not found
        """
        if self.data.get("duration"):
            return self.data["duration"]
        elif self.data.get("more_info"):
            return self.data["more_info"]["duration"]
        return None

    @property
    def encrypted_media_url(self) -> str:
        """Get the track's encrypted media URL.

        Returns:
            The encrypted URL for the track's media
        """
        return self.data["more_info"]["encrypted_media_url"]

    @property
    def has_lyrics(self) -> bool:
        """Check if the track has lyrics available.

        Returns:
            True if lyrics are available, False otherwise
        """
        return self.data["more_info"]["has_lyrics"]

    @property
    def media_url(self) -> str:
        """Get the track's media URL.

        Returns:
            The processed media URL for the track
        """
        return self.data["media_url"].split("?")[0].replace("ac.cf", "aac")

    @property
    def author(self) -> Artist:
        """Get the primary artist of the track.

        Returns:
            Artist object representing the primary artist
        """
        from saavn.models.artist import Artist
        return Artist(
            data=self.data["more_info"]["artistMap"]["primary_artists"][0], tracks=None
        )

    @property
    def artists(self) -> List[Artist]:
        """Get all artists associated with the track.

        Returns:
            List of Artist objects, or the primary artist if no other artists found
        """
        from saavn.models.artist import Artist
        if self.data["more_info"]["artistMap"].get("artists"):
            artists = [
                Artist(data=artist, tracks=None)
                for artist in self.data["more_info"]["artistMap"]["artists"]
            ]
            return artists
        return [self.author]

    @property
    def as_json(self) -> dict:
        """Get the raw track data.

        Returns:
            Dictionary containing the raw track data
        """
        return self.data
