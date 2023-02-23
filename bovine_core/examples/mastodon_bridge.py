import asyncio

import aiohttp

from bovine_core.clients.activity_pub import ActivityPubClient


async def sse(client):
    async with aiohttp.ClientSession() as session:
        client = client.set_session(session)
        event_source = client.server_sent_events()

        async for event in event_source:
            await client.post("http://mastodon.local/users/admin/inbox", event.data)


with open("helge.toml", "rb") as f:
    client = ActivityPubClient.from_toml_file(f)

asyncio.run(sse(client))
