import json
import logging
import random
from typing import Any, List
from urllib.parse import quote
import asyncio

from .client import HttpClient
from .models import Album, SearchResult, Track
from .routes import Route

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
]

class Saavn:
    def __init__(self):
        self.headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Referer": "https://www.jiosaavn.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }
        
    def extract_id(self, url: str):
        return url.split("/")[-1]
    
    async def get_media_url(self, enc_url: str):
        async with HttpClient(headers=self.headers) as client:
            route = Route("token", url=quote(enc_url), bitrate="320")
            response = await client.post(route.url)
            return response["auth_url"]

    async def search_tracks(self, query: str, pages: int = 5, count: int = 5) -> List[Track]:
        """
        Searches for tracks, up to a specified number of pages
        
        Parameters
        ----------
        query : str
            - The search query (title/artist/album)
        max_pages : int, optional
            - Maximum number of pages to fetch

        Returns
        -------
        List[Track]
            - List of tracks
        """
        async with HttpClient(headers=self.headers) as client:
            # Fetch search results concurrently across pages, limited by max_pages
            tasks = [client.get(Route("search", query=query, page=i).url) for i in range(1, pages + 1)]
            responses = await asyncio.gather(*tasks)

            tracks = []
            media_url_tasks = []
            for response in responses:
                if response.get("results") == []:
                    break
                for song in response.get("results", []):
                    # Schedule concurrent media URL fetches, with a limit
                    media_url_tasks.append(
                        self.get_media_url(song["more_info"]["encrypted_media_url"])
                    )
                    tracks.append(Track(data=song))

            # Fetch media URLs concurrently with controlled concurrency
            media_urls = await asyncio.gather(*media_url_tasks)
            for track, media_url in zip(tracks, media_urls):
                track.data["media_url"] = media_url

            return tracks[:count]

    async def get_track(self, track_id: str, as_dict: bool = False):
        """
        Retrieves track details and media URL.
        
        Parameters
        ----------
        track_id : str
            - The ID of the track to retrieve.

        Returns
        -------
        Track
            - Track with media URL.
        """
        async with HttpClient(headers=self.headers) as client:
            route = Route("details", token=track_id)
            response = await client.get(route.url)
            media_url = await self.get_media_url(response["songs"][0]["more_info"]["encrypted_media_url"])

            response["songs"][0]["media_url"] = media_url
            return response if as_dict else Track(data=response["songs"][0])
        
        
    async def get_album(self, album_id: str, as_dict: bool = False):
        """
        Retrieves album details and associated tracks concurrently.
        
        Parameters
        ----------
        album_id : str
            - The ID of the album to retrieve. (example: 125656, 134976)

        Returns
        -------
        Album
            - Album with track details, fetched concurrently.
        """
        route = Route("albums", albumid=album_id)
        async with HttpClient(headers=self.headers) as client:
            response = await client.get(route.url)
            if as_dict:
                return response
            else:
                # Fetch all tracks concurrently
                tasks = [
                    self.get_track(self.extract_id(song["perma_url"]), as_dict=False)
                    for song in response["songs"]
                ]
                tracks = await asyncio.gather(*tasks)
                return Album(data=response, tracks=tracks)

    async def get_playlist(self, playlist_id: str, as_dict: bool = False) -> dict:
        ...