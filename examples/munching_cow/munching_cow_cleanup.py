import asyncio
import json
import aiohttp

from dateutil.parser import parse
from datetime import datetime, timedelta, timezone

from bovine_core.clients.signed_http import signed_get, signed_post
from bovine_core.activitystreams.activities import build_delete


account_url = "https://mymath.rocks/activitypub/munchingcow"
public_key_url = f"{account_url}#main-key"
outbox_url = f"{account_url}/outbox"


async def cleanup_outbox(public_key_url, private_key, outbox_url):
    cut_off = datetime.now(tz=timezone.utc) - timedelta(hours=12)
    async with aiohttp.ClientSession() as session:
        response = await signed_get(session, public_key_url, private_key, outbox_url)
        data = json.loads(await response.text())

        for item in data["orderedItems"]:
            if parse(item["published"]) < cut_off:
                object_id = item["object"]["id"]

                delete = build_delete(account_url, object_id).build()

                response = await signed_post(
                    session, public_key_url, private_key, outbox_url, json.dumps(delete)
                )


with open("../../.files/cow_private.pem", "r") as f:
    private_key = f.read()

asyncio.run(cleanup_outbox(public_key_url, private_key, outbox_url))
