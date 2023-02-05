import asyncio
import json
import tomllib

import aiohttp
import feedparser
from bovine_core.activitystreams.activities import build_create, build_delete
from bovine_core.activitystreams.objects import build_note
from bovine_core.clients.activity_pub import ActivityPubClient

from dateutil.parser import parse


def entry_to_note(account_url, entry):
    entry_id = entry["id"].split("/")[-1]
    entry_url = f"{account_url}/{entry_id}"
    entry_content = entry["summary"]
    entry_published = parse(entry["published"])

    builder = (
        build_note(account_url, entry_url, entry_content)
        .as_public()
        .with_published(entry_published)
    )

    return builder.build()


async def update_account(session, client, config):
    feed = feedparser.parse(config["feed_url"])

    entries = [entry_to_note(config["account_url"], entry) for entry in feed["entries"]]

    response = await client.get_ordered_collection(config["outbox_url"])
    ids_in_outbox = [item["object"]["id"] for item in response["items"]]
    entry_ids = [entry["id"] for entry in entries]

    activities = [
        build_create(entry).build()
        for entry in entries
        if entry["id"] not in ids_in_outbox
    ] + [
        build_delete(config["account_url"], outbox_id).build()
        for outbox_id in ids_in_outbox
        if outbox_id not in entry_ids
    ]

    async with asyncio.TaskGroup() as tg:
        for activity in activities:
            tg.create_task(
                client.post(
                    config["outbox_url"],
                    json.dumps(activity),
                )
            )


async def process(config):
    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as tg:
            for account_name, account_config in config.items():
                client = ActivityPubClient(
                    session,
                    account_config["public_key_url"],
                    account_config["private_key"],
                )
                tg.create_task(update_account(session, client, account_config))


with open("resisa.toml", "rb") as f:
    config = tomllib.load(f)
asyncio.run(process(config))
