
import aiohttp
import json
from typing import Dict, Optional
import logging
import asyncio
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

    async def get(self, url: str) -> Dict:
        async with self.session.get(url) as response:
            if response.status != 200:
                raise aiohttp.ClientError(f"Failed to fetch data: {response.status}")
            try:
                return json.loads(await response.text())
            except json.JSONDecodeError:
                raise ValueError("Failed to parse JSON response")

    async def post(self, url: str) -> Dict:
        async with self.session.post(url) as response:
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
