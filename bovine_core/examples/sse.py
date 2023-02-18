import asyncio
import json
from datetime import datetime

import aiohttp
import bleach

from bovine_core.clients.activity_pub import ActivityPubClient


async def sse(client):
    async with aiohttp.ClientSession() as session:
        client = client.set_session(session)
        event_source = client.server_sent_events()

        async for event in event_source:
            data = json.loads(event.data)
            if "object" in data and "content" in data["object"]:
                print(
                    datetime.now().isoformat() + "  " + data["object"]["attributedTo"]
                )
                print(bleach.clean(data["object"]["content"], tags=[], strip=True))
                print()
            else:
                print(json.dumps(data, indent=2))


with open("helge.toml", "rb") as f:
    client = ActivityPubClient.from_toml_file(f)

asyncio.run(sse(client))
