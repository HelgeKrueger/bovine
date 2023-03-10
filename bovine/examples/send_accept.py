import asyncio
import json
from argparse import ArgumentParser

import aiohttp

from bovine.activitypub import actor_from_file
from bovine.activitystreams.activities import build_accept


async def send_accept(config_file, target):
    async with aiohttp.ClientSession() as session:
        actor = actor_from_file(config_file, session)

        await actor.load()
        response = await actor.proxy_element(target)
        response = json.loads(await response.text())

        accept = build_accept(actor.actor_id, response).build()

        await actor.send_to_outbox(accept)


parser = ArgumentParser()
parser.add_argument("target")
parser.add_argument("--config", default="h.toml")

args = parser.parse_args()

asyncio.run(send_accept(args.config, args.target))
