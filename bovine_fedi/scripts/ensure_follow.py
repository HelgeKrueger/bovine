import asyncio

from bovine import BovineActor
from bovine_store.models import CollectionItem
from tortoise import Tortoise


async def fetch_followers():
    async with BovineActor("helge.toml") as actor:
        await Tortoise.init(
            db_url="sqlite://db.sqlite3",
            modules={
                "models": [
                    "bovine_fedi.models",
                    "bovine_store.models",
                    "bovine_user.models",
                    "aerich.models",
                ]
            },
        )
        for key in ["followers", "following"]:
            followers = actor.information[key]

            print(followers)

            items = await CollectionItem.filter(part_of=followers).all()

            for x in items:
                print(await actor.proxy_element(x.object_id))

        await Tortoise.close_connections()


asyncio.run(fetch_followers())
