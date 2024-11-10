import asyncio
import json
import logging
import random
from functools import wraps
from typing import List, Union
from urllib.parse import quote

from .client import HttpClient
from .models import Album, Artist, Playlist, Track
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

    def _extract_id(self, url_or_id: str) -> str:
        if "https" or "http" in url_or_id or "/" in url_or_id:
            return url_or_id.split("/")[-1]
        return url_or_id

    def extract_id(func):
        @wraps(func)
        def wrapper(self, url_or_id: str, *args, **kwargs):
            id_or_token = self._extract_id(url_or_id)
            return func(self, id_or_token, *args, **kwargs)

        return wrapper

    async def get_media_url(self, enc_url: str):
        async with HttpClient(headers=self.headers) as client:
            route = Route("token", url=quote(enc_url), bitrate="320")
            response = await client.post(route)
            return response["auth_url"]

    async def get_buffer(self, track: Track):
        async with HttpClient() as client:
            response = await client.get_buffer(track.media_url)
            if not response:
                raise ValueError("Failed to fetch buffer")
            return response

    async def _search_tracks(
        self, query: str, as_dict: bool = False, pages: int = 5, count: int = 5
    ) -> List[Track]:
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
            tasks = [
                client.get(Route("search", query=query, page=i))
                for i in range(1, pages + 1)
            ]
            responses = await asyncio.gather(*tasks)

            tracks = []
            media_url_tasks = []

            if as_dict:
                for response in responses:
                    if response.get("results") == []:
                        raise ValueError("No results found")
                    tracks.append(response)
                return tracks

            for response in responses:

                if response.get("results") == []:
                    break
                for song in response.get("results", []):
                    media_url_tasks.append(
                        self.get_media_url(song["more_info"]["encrypted_media_url"])
                    )
                    tracks.append(Track(data=song))

            media_urls = await asyncio.gather(*media_url_tasks)
            for track, media_url in zip(tracks, media_urls):
                track.data["media_url"] = media_url

            return tracks[:count]

    async def search(self, query: str, as_dict: bool = False, **kwargs):
        """
        Searches for tracks, albums, artists and playlists

        Parameters
        ----------
        query : str
            - The search query (title/artist/album/playlist)

        as_dict : bool
            - Whether to return the results as a dictionary

        kwargs
        ------
        #if link is not provided
        page : int
            - The page number to fetch
        count : int
            - The number of results to fetch

        Returns
        -------
        ...
        """
        if query.startswith("https://www.jiosaavn.com/"):
            if "album" in query:
                if as_dict:
                    return await self.get_album(query, as_dict=True)
                return await self.get_album(query)
            elif "playlist" in query:
                if as_dict:
                    return await self.get_playlist(query, as_dict=True)
                return await self.get_playlist(query)
            elif "artist" in query:
                if as_dict:
                    return await self.get_artist(query, as_dict=True)
                return await self.get_artist(query)
            elif "song" in query:
                if as_dict:
                    return await self.get_track(query, as_dict=True)
                return await self.get_track(query)
        else:
            pages = kwargs.get("page", 1)
            count = kwargs.get("count", 5)
            return await self._search_tracks(
                query, as_dict=as_dict, pages=pages, count=count
            )

    @extract_id
    async def get_track(self, track: str, as_dict: bool = False):
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
            route = Route("details", type="song", token=track)
            response = await client.get(route)
            media_url = await self.get_media_url(
                response["songs"][0]["more_info"]["encrypted_media_url"]
            )
            response["songs"][0]["media_url"] = media_url
            return response if as_dict else Track(data=response["songs"][0])

    @extract_id
    async def get_album(self, album: str, as_dict: bool = False):
        """
        Retrieves album details and associated tracks concurrently.

        Parameters
        ----------
        album : str
            - The ID or URL of the album to retrieve. (example: 125656, 134976)

        Returns
        -------
        Album
            - Album with track details, fetched concurrently.
        """
        route = Route("details", type="album", token=album)
        async with HttpClient(headers=self.headers) as client:
            response = await client.get(route)
            if as_dict:
                return response
            else:
                tracks = []
                if response.get("list"):
                    for song in response.get("list"):
                        media_url = await self.get_media_url(
                            song["more_info"]["encrypted_media_url"]
                        )
                        song["media_url"] = media_url
                        tracks.append(Track(data=song))

                return Album(data=response, tracks=tracks)

    @extract_id
    async def get_artist(self, artist: str, as_dict: bool = False):
        """
        Retrieves artist details and associated tracks concurrently.

        Parameters
        ----------
        artist : str
            - The ID or URL of the artist to retrieve. (example: 125656, 134976)

        Returns
        -------
        Artist
            - Artist details with top tracks.
        """
        route = Route("details", type="artist", token=artist)
        async with HttpClient(headers=self.headers) as client:
            response = await client.get(route)

            if as_dict:
                return response
            else:
                tracks = []
                if response.get(
                    "topSongs"
                ):  # currently only top songs , in the future we can add all songs (check json response for more info)
                    for song in response.get("topSongs"):
                        media_url = await self.get_media_url(
                            song["more_info"]["encrypted_media_url"]
                        )
                        song["media_url"] = media_url
                        tracks.append(Track(data=song))

                return Artist(data=response, tracks=tracks)

    @extract_id
    async def get_playlist(self, playlist: str, as_dict: bool = False):
        """
        Retrieves playlist details and associated tracks concurrently.

        Parameters
        ----------
        playlist : str
            - The ID or URL of the playlist to retrieve. (example: 125656, https://www.jiosaavn.com/s/playlist/d106d3c2d80b4702585f0e1a41098fd4/test/PCXplErt,39xWb5,FqsjKg__)

        Returns
        -------
        Playlist
            - Playlist with track details, fetched concurrently.
        """

        route = Route("details", type="playlist", token=playlist)
        async with HttpClient(headers=self.headers) as client:
            response = await client.get(route)
            if as_dict:
                return response
            else:
                tracks = []
                if response.get("list"):
                    for song in response.get("list"):
                        media_url = await self.get_media_url(
                            song["more_info"]["encrypted_media_url"]
                        )
                        song["media_url"] = media_url
                        tracks.append(Track(data=song))

                return Playlist(data=response, tracks=tracks)

    async def get_recommendations(self, pid: str | Track) -> List[Track]:
        # check a track response as dict for pid
        async with HttpClient(headers=self.headers) as client:
            if isinstance(pid, Track):
                pid = pid.pid

            route = Route("recomend", pid=pid)
            response = await client.get(route)
            tracks: List[Track] = []
            if type(response) == list:
                for song in response:
                    media_url = await self.get_media_url(
                        song["more_info"]["encrypted_media_url"]
                    )
                    song["media_url"] = media_url
                    tracks.append(Track(data=song))
                return tracks
