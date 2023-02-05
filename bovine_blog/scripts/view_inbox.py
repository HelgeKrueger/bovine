import asyncio
from argparse import ArgumentParser

from bovine_tortoise import ManagedDataStore
from bovine_tortoise.models import Actor, InboxEntry
from rich import print as pprint


async def store_user(username):
    store = ManagedDataStore()
    await store.connect()
    actor = await Actor.get_or_none(account=username)
    entries = await InboxEntry.filter(actor=actor).all()
    for entry in entries:
        pprint(entry.content)
        await entry.delete()
    await store.disconnect()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("username")
    args = parser.parse_args()

    asyncio.run(store_user(args.username))
