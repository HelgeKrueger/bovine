import asyncio
from argparse import ArgumentParser

import aiohttp

from bovine_core.activitypub import actor_from_file
from bovine_core.activitystreams.activities import build_create


async def send_note(config_file, text):
    async with aiohttp.ClientSession() as session:
        actor = actor_from_file(config_file, session)

        note = actor.note(text).as_public().build()
        create = build_create(note).build()

        await actor.send_to_outbox(create)


parser = ArgumentParser()
parser.add_argument("text")
parser.add_argument("--config_file", default="helge.toml")

args = parser.parse_args()

asyncio.run(send_note(args.config_file, args.text))
