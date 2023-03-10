import asyncio
from datetime import datetime, timedelta

from bovine_blog import TORTOISE_ORM
from bovine_store.models import CollectionItem, StoredJsonObject
from tortoise import Tortoise


async def cleanup_db():
    await Tortoise.init(
        db_url=TORTOISE_ORM["connections"]["default"],
        modules={"models": TORTOISE_ORM["apps"]["models"]["models"]},
    )
    today = datetime.now()
    delete_from_datetime = today - timedelta(days=3)

    result = (
        await StoredJsonObject.filter(created__lt=delete_from_datetime)
        .limit(1000)
        .all()
        .prefetch_related("visible_to")
    )

    for x in result:
        if not x.id.startswith("https://mymath.rocks"):
            for y in x.visible_to:
                await y.delete()
            items = await CollectionItem.filter(object_id=x.id).all()
            print(x.id, len(items))
            for i in items:
                await i.delete()

            await x.delete()

    await Tortoise.close_connections()


asyncio.run(cleanup_db())
