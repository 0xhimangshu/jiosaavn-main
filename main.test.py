import asyncio
import json

from saavn import Saavn
from typing import List


async def main(search:str):
    saavn = Saavn()
    resp = await saavn.get_track(search)
    with open(f"test.mp3", "wb") as f:
        f.write(await saavn.get_buffer(resp))
 
def test():
    search = input("Search: ")
    asyncio.run(main(search=search))

if __name__ == "__main__":
    test()
    # unnecessary