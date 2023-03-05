import asyncio
import json
from argparse import ArgumentParser

import aiohttp

from bovine_core.clients.activity_pub import ActivityPubClient


async def send_delete(client, target):
    async with aiohttp.ClientSession() as session:
        client = client.set_session(session)
        result = await client.get(f"https://{target}/actor")
        data = json.loads(await result.text())

        shared_inbox = data["endpoints"]["sharedInbox"]

        print(shared_inbox)

        account = "https://mymath.rocks/activitypub/test"

        delete = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": f"{account}#delete",
            "type": "Delete",
            "actor": account,
            "to": ["https://www.w3.org/ns/activitystreams#Public"],
            "object": account,
        }

        print(await client.post(shared_inbox, json.dumps(delete)))


parser = ArgumentParser()
parser.add_argument("target")
args = parser.parse_args()

with open("test.toml", "rb") as f:
    client = ActivityPubClient.from_toml_file(f)

asyncio.run(send_delete(client, args.target))
