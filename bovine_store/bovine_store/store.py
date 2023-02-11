import asyncio

from tortoise import Tortoise

from bovine_store.models import StoredObject

from .jsonld import split_into_objects, combine_items


class Store:
    def __init__(self, db_url="sqlite://store.db"):
        self.db_url = db_url

    async def init_connection(self):
        await Tortoise.init(
            db_url=self.db_url, modules={"models": ["bovine_store.models"]}
        )
        # Generate the schema
        await Tortoise.generate_schemas()

    async def close_connection(self):
        await Tortoise.close_connections()

    async def store(self, owner, item):
        to_store = await split_into_objects(item)

        tasks = [
            StoredObject.create(id=obj["id"], content=obj, owner=owner)
            for obj in to_store
        ]

        await asyncio.gather(*tasks)

    async def retrieve(self, retriever, object_id, include=[]):
        result = await StoredObject.get_or_none(id=object_id)
        if result.owner != retriever:
            return None

        data = result.content
        if len(include) == 0:
            return data

        items = await asyncio.gather(
            *[StoredObject.get_or_none(id=data[key]) for key in include]
        )
        items = [obj.content for obj in items if obj]

        return combine_items(data, items)
