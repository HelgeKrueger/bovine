import asyncio

from tortoise import Tortoise

from bovine_store.models import StoredObject, VisibilityTypes, VisibleTo

from .jsonld import split_into_objects, combine_items
from .permissions import has_access


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

    async def store(self, owner, item, as_public=False, visible_to=[]):
        visibility_type = VisibilityTypes.RESTRICTED
        if as_public:
            visibility_type = VisibilityTypes.PUBLIC

        to_store = await split_into_objects(item)

        tasks = [
            StoredObject.get_or_create(
                id=obj["id"],
                defaults={
                    "content": obj,
                    "owner": owner,
                    "visibility": visibility_type,
                },
            )
            for obj in to_store
        ]

        items = await asyncio.gather(*tasks)

        for item, created in items:
            if created:
                visible_tasks = [
                    VisibleTo.create(
                        main_object=item,
                        object_id=actor,
                    )
                    for actor in visible_to
                ]
                await asyncio.gather(*visible_tasks)
            else:
                print("XXX")

    async def retrieve(self, retriever, object_id, include=[]):
        result = await StoredObject.get_or_none(id=object_id).prefetch_related(
            "visible_to"
        )
        if not await has_access(result, retriever):
            return None

        data = result.content
        if len(include) == 0:
            return data

        items = await asyncio.gather(
            *[StoredObject.get_or_none(id=data[key]) for key in include]
        )
        items = [obj.content for obj in items if obj]

        return combine_items(data, items)
