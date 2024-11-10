from typing import Any


class Route:
    BASE_URL = "https://www.jiosaavn.com/api.php"
    ENDPOINTS = {
        "search": "?__call=search.getResults&_format=json&_marker=0&api_version=4&ctx=web6dot0&n=20&q={query}&p={page}",
        "autocomplete": "?__call=autocomplete.get&_format=json&_marker=0&cc=in&includeMetaTags=1&query={query}",
        "lyrics": "?__call=lyrics.getLyrics&ctx=web6dot0&api_version=4&_format=json&_marker=0%3F_marker%3D0&lyrics_id={lyrics_id}",
        "token": "?__call=song.generateAuthToken&api_version=4&_format=json&ctx=web6dot0&_marker=0%3F_marker%3D0&url={url}&bitrate={bitrate}",
        "details": "?__call=webapi.get&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0%3F_marker%3D0&type={type}&token={token}",
        "recomend": "?__call=reco.getreco&api_version=4&_format=json&_marker=0&ctx=web6dot0&language=english&pid={pid}",
    }

    def __init__(self, endpoint: str, **params: Any):
        self.url = self.build_url(endpoint, **params)

    def build_url(self, endpoint: str, **params: Any) -> str:
        path = self.ENDPOINTS.get(endpoint)
        if not path:
            raise ValueError(f"Invalid endpoint: {endpoint}")
        return f"{self.BASE_URL}{path.format_map(params)}"
