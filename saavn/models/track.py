from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .artist import Artist


class Track:
    def __init__(self, data: dict):
        self.data = data

    @property
    def id(self) -> str:
        return self.data["perma_url"].split("/")[-1]

    @property
    def pid(self) -> str:
        return self.data["id"]

    @property
    def title(self) -> str:
        if self.data.get("title"):
            return self.data["title"].replace("&quot;", '"')
        elif self.data.get("song"):
            return self.data.get("song").replace("&quot;", '"')
        else:
            return None

    @property
    def url(self) -> str:
        if self.data.get("perma_url"):
            return self.data["perma_url"]
        elif self.data.get("url"):
            return self.data.get("url")
        else:
            return None

    @property
    def image(self) -> str:
        return self.data["image"]

    @property
    def duration(self) -> int:
        return self.data["duration"]

    @property
    def encrypted_media_url(self) -> str:
        return self.data["more_info"]["encrypted_media_url"]

    @property
    def has_lyrics(self) -> bool:
        return self.data["more_info"]["has_lyrics"]

    @property
    def media_url(self) -> str:
        return self.data["media_url"].split("?")[0].replace("ac.cf", "aac")

    @property
    def author(self) -> str:
        return Artist(
            data=self.data["more_info"]["artistMap"]["primary_artist"][0], tracks=None
        )

    @property
    def artists(self):
        if self.data["more_info"]["artistMap"].get("artists"):
            artists = [
                Artist(data=artist, tracks=None)
                for artist in self.data["more_info"]["artistMap"]["artists"]
            ]
            return artists
        else:
            return self.author

    @property
    def as_json(self) -> dict:
        return self.data
