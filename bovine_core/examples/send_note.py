import asyncio
import json
from argparse import ArgumentParser

import aiohttp

from bovine_core.activitystreams.activities import build_create
from bovine_core.activitystreams.objects import build_note
from bovine_core.clients.activity_pub import ActivityPubClient


async def send_note(client, text):
    async with aiohttp.ClientSession() as session:
        client = client.set_session(session)

        note = build_note(client.account_url, "", text).as_public().build()
        create = build_create(note).build()

        await client.post(client.account_url + "/outbox", json.dumps(create))


parser = ArgumentParser()
parser.add_argument("text")

args = parser.parse_args()

with open("helge.toml", "rb") as f:
    client = ActivityPubClient.from_toml_file(f)

asyncio.run(send_note(client, args.text))
