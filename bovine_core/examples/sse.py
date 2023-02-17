import asyncio
import json
from datetime import datetime

import aiohttp
import bleach
import tomli

from bovine_core.clients.event_source import EventSource


async def sse(url, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    async with aiohttp.ClientSession() as session:
        event_source = EventSource(session, url, headers=headers)

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
    config = tomli.load(f)["helge"]

asyncio.run(sse(config["server_sent_events_url"], config["access_token"]))
