import asyncio
import random
from argparse import ArgumentParser

import aiohttp

from bovine_core.activitypub import actor_from_file
from bovine_core.activitystreams.activities import build_like


async def send_like(config_file, target):
    async with aiohttp.ClientSession() as session:
        actor = actor_from_file(config_file, session)
        response = await actor.get(target)
        author = response["attributedTo"]

        #
        # Most implementations just support a single like, so we are
        # sending a random cow flavored emoji instead of all of them
        #
        # If this makes you sad, you should lobby UI implementations
        # to display multiple emotes from the same person.
        #

        emote_to_send = random.choice("🐮🐄🦬🐂🌱🥩🥛🧀🍼")

        like = (
            build_like(actor.actor_id, target)
            .with_content(emote_to_send)
            .add_to(author)
            .build()
        )

        await actor.send_to_outbox(like)


parser = ArgumentParser()
parser.add_argument("target")

args = parser.parse_args()

asyncio.run(send_like("helge.toml", args.target))
