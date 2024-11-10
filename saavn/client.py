import asyncio
import json
import logging
from typing import Dict, Optional

import aiohttp

from .routes import Route

logging.getLogger("aiohttp").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)


class HttpClient:
    def __init__(self, headers: Optional[Dict[str, str]] = None):
        self.headers = headers

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get(self, route: Route) -> Dict:
        async with self.session.get(route.url) as response:
            if response.status != 200:
                raise aiohttp.ClientError(f"Failed to fetch data: {response.status}")
            try:
                return json.loads(await response.text())
            except json.JSONDecodeError:
                raise ValueError("Failed to parse JSON response")

    async def post(self, route: Route) -> Dict:
        async with self.session.post(route.url) as response:
            if response.status != 200:
                raise aiohttp.ClientError(f"Failed to fetch data: {response.status}")
            try:
                return json.loads(await response.text())
            except json.JSONDecodeError:
                raise ValueError("Failed to parse JSON response")

    async def get_buffer(self, url: str) -> bytes:
        async with self.session.get(url) as response:
            if response.status != 200:
                raise aiohttp.ClientError(f"Failed to fetch data: {response.status}")
            return await response.read()
