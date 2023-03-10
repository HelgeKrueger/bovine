import aiohttp
import IPython
from bovine_core.clients.activity_pub import ActivityPubClient


async def set_session(client):
    return client.set_session(await aiohttp.ClientSession())


with open("helge.toml", "rb") as f:
    client = ActivityPubClient.from_toml_file(f)


IPython.embed()
