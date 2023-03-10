import asyncio
import json
from argparse import ArgumentParser

import aiohttp

from bovine.clients.activity_pub import ActivityPubClient


async def send_delete(client, target):
    async with aiohttp.ClientSession() as session:
        client = client.set_session(session)
        result = await client.get(f"https://{target}/actor")
        data = json.loads(await result.text())

        shared_inbox = data["endpoints"]["sharedInbox"]

        account = "https://mymath.rocks/activitypub/test"

        delete = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": f"{account}#delete",
            "type": "Delete",
            "actor": account,
            "to": ["https://www.w3.org/ns/activitystreams#Public"],
            "object": account,
        }

        response = await client.post(shared_inbox, json.dumps(delete))
        print(shared_inbox, response.status)


parser = ArgumentParser()
parser.add_argument("--config", default="munchingcow.toml")
args = parser.parse_args()

with open(args.config, "rb") as f:
    client = ActivityPubClient.from_toml_file(f)

with open("server_list") as f:
    for line in f:
        try:
            asyncio.run(send_delete(client, line.strip()))
        except Exception as e:
            print(e)
            pass
