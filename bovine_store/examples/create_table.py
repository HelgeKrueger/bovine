import asyncio

from tortoise import Tortoise


async def create_table():
    db_file = "db.sqlite3"
    db_url = f"sqlite://{db_file}"

    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["bovine_store.models"]},
    )
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


asyncio.run(create_table())
