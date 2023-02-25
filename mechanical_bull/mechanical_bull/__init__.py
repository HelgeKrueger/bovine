import asyncio
import json
from datetime import datetime

import aiohttp

from bovine_core.activitypub import actor_from_file
from .actions.handle_follow_request import handle_follow_request


async def mechanical_bull(config_file):
    async with aiohttp.ClientSession() as session:
        actor = actor_from_file(config_file, session)
        event_source = await actor.event_source()

        async for event in event_source:
            data = json.loads(event.data)
            await handle_follow_request(actor, data)
