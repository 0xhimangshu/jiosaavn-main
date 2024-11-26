import logging
from functools import wraps
from typing import Dict, List, Optional, Union
from urllib.parse import quote

from .client import HttpClient
from .models import Album, Artist, Playlist, Track
from .routes import Route

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Common user agents for requests
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0", 
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
]

class Saavn:
    def __init__(self):
        """Initialize Saavn client with default headers."""
        self.headers = {
            "User-Agent": USER_AGENTS[0],  # Use first agent by default
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive", 
            "Referer": "https://www.jiosaavn.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }

    def _extract_id(self, url_or_id: str) -> str:
        """Extract ID from URL or return ID if already extracted."""
        return url_or_id.split("/")[-1] if "/" in url_or_id else url_or_id

    def extract_id(func):
        """Decorator to extract ID from URL before calling function."""
        @wraps(func)
        def wrapper(self, url_or_id: str, *args, **kwargs):
            id_or_token = self._extract_id(url_or_id)
            return func(self, id_or_token, *args, **kwargs)
        return wrapper

    def get_media_url(self, enc_url: str) -> str:
        """Get media URL from encrypted URL."""
        with HttpClient(headers=self.headers) as client:
            route = Route("token", url=quote(enc_url), bitrate="320")
            response = client.post(route)
            return response["auth_url"]

    def get_buffer(self, track: Track) -> bytes:
        """Get audio buffer for track."""
        with HttpClient() as client:
            response = client.get_buffer(track.media_url)
            if not response:
                raise ValueError("Failed to fetch buffer")
            return response

    def _search_tracks(
        self, 
        query: str, 
        as_dict: bool = False, 
        pages: int = 5, 
        count: int = 5
    ) -> Union[List[Track], List[Dict]]:
        """Search for tracks with pagination support."""
        with HttpClient(headers=self.headers) as client:
            tasks = [
                client.get(Route("search", query=query, page=i))
                for i in range(1, pages + 1)
            ]
            responses = [task for task in tasks]

            if as_dict:
                tracks = []
                for response in responses:
                    if not response.get("results"):
                        raise ValueError("No results found")
                    tracks.append(response)
                return tracks

            tracks = []
            media_url_tasks = []

            for response in responses:
                if not response.get("results"):
                    break
                    
                for song in response.get("results", []):
                    media_url_tasks.append(
                        self.get_media_url(song["more_info"]["encrypted_media_url"])
                    )
                    tracks.append(Track(data=song))

            media_urls = [task for task in media_url_tasks]
            for track, media_url in zip(tracks, media_urls):
                track.data["media_url"] = media_url

            return tracks[:count]

    def search(
        self, 
        query: str, 
        as_dict: bool = False, 
        **kwargs
    ) -> Union[List[Track], Album, Artist, Playlist, Dict]:
        """
        Search for tracks, albums, artists and playlists.
        
        Args:
            query: Search query or URL
            as_dict: Return raw dictionary response
            **kwargs: Additional parameters (page, count)
            
        Returns:
            Matching tracks, album, artist or playlist
        """
        if query.startswith("https://www.jiosaavn.com/"):
            if "album" in query:
                return self.get_album(query, as_dict=as_dict)
            elif "playlist" in query:
                return self.get_playlist(query, as_dict=as_dict)
            elif "artist" in query:
                return self.get_artist(query, as_dict=as_dict)
            elif "song" in query:
                return self.get_track(query, as_dict=as_dict)
        else:
            pages = kwargs.get("page", 1)
            count = kwargs.get("count", 5)
            return self._search_tracks(
                query, as_dict=as_dict, pages=pages, count=count
            )

    @extract_id
    def get_track(self, track: str, as_dict: bool = False) -> Union[Track, Dict]:
        """Get track details by ID or URL."""
        with HttpClient(headers=self.headers) as client:
            route = Route("details", type="song", token=track)
            response = client.get(route)
            media_url = self.get_media_url(
                response["songs"][0]["more_info"]["encrypted_media_url"]
            )
            response["songs"][0]["media_url"] = media_url
            return response if as_dict else Track(data=response["songs"][0])

    @extract_id
    def get_album(self, album: str, as_dict: bool = False) -> Union[Album, Dict]:
        """Get album details by ID or URL."""
        route = Route("details", type="album", token=album)
        with HttpClient(headers=self.headers) as client:
            response = client.get(route)
            if as_dict:
                return response

            tracks = []
            if response.get("list"):
                for song in response.get("list"):
                    media_url = self.get_media_url(
                        song["more_info"]["encrypted_media_url"]
                    )
                    song["media_url"] = media_url
                    tracks.append(Track(data=song))

            return Album(data=response, tracks=tracks)

    @extract_id
    def get_artist(self, artist: str, as_dict: bool = False) -> Union[Artist, Dict]:
        """Get artist details by ID or URL."""
        route = Route("details", type="artist", token=artist)
        with HttpClient(headers=self.headers) as client:
            response = client.get(route)

            if as_dict:
                return response

            tracks = []
            if response.get("topSongs"):
                for song in response.get("topSongs"):
                    media_url = self.get_media_url(
                        song["more_info"]["encrypted_media_url"]
                    )
                    song["media_url"] = media_url
                    tracks.append(Track(data=song))

            return Artist(data=response, tracks=tracks)

    @extract_id
    def get_playlist(self, playlist: str, as_dict: bool = False) -> Union[Playlist, Dict]:
        """Get playlist details by ID or URL."""
        route = Route("details", type="playlist", token=playlist)
        with HttpClient(headers=self.headers) as client:
            response = client.get(route)
            if as_dict:
                return response

            tracks = []
            if response.get("list"):
                for song in response.get("list"):
                    media_url = self.get_media_url(
                        song["more_info"]["encrypted_media_url"]
                    )
                    song["media_url"] = media_url
                    tracks.append(Track(data=song))

            return Playlist(data=response, tracks=tracks)

    def get_recommendations(self, pid: Union[str, Track]) -> List[Track]:
        """Get track recommendations based on track ID or Track object."""
        with HttpClient(headers=self.headers) as client:
            if isinstance(pid, Track):
                pid = pid.pid

            route = Route("recomend", pid=pid)
            response = client.get(route)
            tracks: List[Track] = []
            
            if isinstance(response, list):
                for song in response:
                    media_url = self.get_media_url(
                        song["more_info"]["encrypted_media_url"]
                    )
                    song["media_url"] = media_url
                    tracks.append(Track(data=song))
                return tracks
