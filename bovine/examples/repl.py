import aiohttp
from bovine.activitypub import actor_from_file


async def get_actor():
    return actor_from_file("h.toml", aiohttp.ClientSession())
