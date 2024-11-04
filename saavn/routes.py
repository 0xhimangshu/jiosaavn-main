from typing import Any

class Route:
    BASE_URL = "https://www.jiosaavn.com/api.php"
    ENDPOINTS = {
        "search": "?__call=search.getResults&_format=json&_marker=0&api_version=4&ctx=web6dot0&n=20&q={query}&p={page}",
        "autocomplete": "?__call=autocomplete.get&_format=json&_marker=0&cc=in&includeMetaTags=1&query={query}",
        "singles": "?__call=song.getDetails&cc=in&_marker=0%3F_marker%3D0&_format=json&pids={pids}",
        "albums": "?__call=content.getAlbumDetails&_format=json&cc=in&_marker=0%3F_marker%3D0&albumid={albumid}",
        "playlists": "?__call=playlist.getDetails&_format=json&cc=in&_marker=0%3F_marker%3D0&listid={listid}",
        "lyrics": "?__call=lyrics.getLyrics&ctx=web6dot0&api_version=4&_format=json&_marker=0%3F_marker%3D0&lyrics_id={lyrics_id}",
        "token": "?__call=song.generateAuthToken&api_version=4&_format=json&ctx=web6dot0&_marker=0%3F_marker%3D0&url={url}&bitrate={bitrate}",
        "details": "?__call=webapi.get&type=song&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0%3F_marker%3D0&token={token}",
    }
    def __init__(self, endpoint: str, **params: Any):
        self.url = self.build_url(endpoint, **params)

    def build_url(self, endpoint: str, **params: Any) -> str:
        path = self.ENDPOINTS.get(endpoint)
        if not path:
            raise ValueError(f"Invalid endpoint: {endpoint}")
        return f"{self.BASE_URL}{path.format_map(params)}"