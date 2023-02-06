import asyncio
import json

import aiohttp
from rich import print


async def get_activity():
    url = "https://mymath.rocks/activitypub/helge/4963d54c-8320-444b-9559-db5e9a5b7068"

    async with aiohttp.ClientSession() as session:
        response = await session.get(
            url,
            headers={
                "accept": "application/activity+json",
            },
        )  # authorization missing

        print(response.status)

        text_content = await response.text()

        data = json.loads(text_content)
        assert data["id"] == url

        print(data)


asyncio.run(get_activity())
