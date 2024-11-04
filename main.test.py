import asyncio
import json

from saavn import Saavn


async def main(search:str):
    saavn = Saavn()
    resp = await saavn.search_tracks(search, pages=1, count=1)
    for song in resp:
        print(song.title, song.media_url)
    # print(len(resp))


def test():
    search = input("Search: ")
    asyncio.run(main(search=search))

if __name__ == "__main__":
    test()