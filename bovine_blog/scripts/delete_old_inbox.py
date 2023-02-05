import asyncio
from datetime import datetime, timedelta, timezone

from bovine_tortoise.models import InboxEntry
from bovine_tortoise.utils import init
from tortoise import Tortoise


async def delete_old(max_age_days=2):
    await init()
    max_age = datetime.now(tz=timezone.utc) - timedelta(days=max_age_days)

    to_delete = InboxEntry.filter(created__lt=max_age)

    print(f"To delete {await to_delete.count()}")

    await to_delete.delete()

    await Tortoise.close_connections()


asyncio.run(delete_old())
