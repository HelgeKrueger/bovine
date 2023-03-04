import asyncio
import json
import logging
from argparse import ArgumentParser
from datetime import datetime

import aiohttp
import bleach

from bovine_core.activitypub.actor import ActivityPubActor

logging.basicConfig(level=logging.DEBUG)


async def sse(config_file):
    async with aiohttp.ClientSession() as session:
        actor = ActivityPubActor.from_file(config_file, session)
        event_source = await actor.event_source()
        async for event in event_source:
            if event is None:
                return
            # print(event)
            if event and event.data:
                data = json.loads(event.data)

                if "object" in data and "content" in data["object"]:
                    print(
                        datetime.now().isoformat()
                        + "  "
                        + data["object"]["attributedTo"]
                    )
                    print(bleach.clean(data["object"]["content"], tags=[], strip=True))
                    print()
                else:
                    print(json.dumps(data, indent=2))


parser = ArgumentParser()
parser.add_argument("--config", default="h.toml")

args = parser.parse_args()

asyncio.run(sse(args.config))
