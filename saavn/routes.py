from typing import Any, Dict


class Route:
    """Class for handling JioSaavn API route construction."""

    # Base API endpoint
    BASE_URL: str = "https://www.jiosaavn.com/api.php"

    # API endpoint paths with parameter placeholders
    ENDPOINTS: Dict[str, str] = {
        "search": "?__call=search.getResults&_format=json&_marker=0&api_version=4&ctx=web6dot0&n=20&q={query}&p={page}",
        "autocomplete": "?__call=autocomplete.get&_format=json&_marker=0&cc=in&includeMetaTags=1&query={query}",
        "lyrics": "?__call=lyrics.getLyrics&ctx=web6dot0&api_version=4&_format=json&_marker=0%3F_marker%3D0&lyrics_id={lyrics_id}",
        "token": "?__call=song.generateAuthToken&api_version=4&_format=json&ctx=web6dot0&_marker=0%3F_marker%3D0&url={url}&bitrate={bitrate}",
        "details": "?__call=webapi.get&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0%3F_marker%3D0&type={type}&token={token}",
        "recomend": "?__call=reco.getreco&api_version=4&_format=json&_marker=0&ctx=web6dot0&language=english&pid={pid}",
    }

    __slots__ = ('url',)

    def __init__(self, endpoint: str, **params: Any) -> None:
        """Initialize Route with endpoint and parameters.
        
        Args:
            endpoint: The API endpoint key
            **params: URL parameters to format into the endpoint path
        """
        self.url = self.build_url(endpoint, **params)

    def build_url(self, endpoint: str, **params: Any) -> str:
        """Build the complete URL for the given endpoint and parameters.
        
        Args:
            endpoint: The API endpoint key
            **params: URL parameters to format into the endpoint path
            
        Returns:
            The complete formatted URL
            
        Raises:
            ValueError: If the endpoint is not found in ENDPOINTS
        """
        if not (path := self.ENDPOINTS.get(endpoint)):
            raise ValueError(f"Invalid endpoint: {endpoint}")
        return f"{self.BASE_URL}{path.format_map(params)}"
