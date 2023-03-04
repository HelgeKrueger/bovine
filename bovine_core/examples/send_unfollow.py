import asyncio
from argparse import ArgumentParser

import aiohttp

from bovine_core.activitypub import actor_from_file
from bovine_core.activitystreams.activities import build_follow, build_undo

print("This does not seem to work")
exit(1)


async def send_unfollow(config_file, target):
    async with aiohttp.ClientSession() as session:
        actor = actor_from_file(config_file, session)

        await actor.load()

        follow = build_follow("", actor.information["id"], target).build()
        unfollow = build_undo(follow).build()
        # print(json.dumps(unfollow, indent=2))

        await actor.send_to_outbox(unfollow)


parser = ArgumentParser()
parser.add_argument("target")
parser.add_argument("--config", default="h.toml")

args = parser.parse_args()

asyncio.run(send_unfollow(args.config, args.target))
