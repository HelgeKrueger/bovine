import asyncio

from tortoise import Tortoise

from bovine_store.models import StoredObject, VisibilityTypes, VisibleTo, CollectionItem

from .jsonld import split_into_objects, combine_items
from .permissions import has_access


class ObjectStore:
    def __init__(self, db_url="sqlite://store.db"):
        self.db_url = db_url

    async def init_connection(self):
        await Tortoise.init(
            db_url=self.db_url, modules={"models": ["bovine_store.models"]}
        )
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

        id_to_store = {obj["id"]: obj for obj in to_store}

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
                if item.owner == owner:
                    item.content = id_to_store[item.id]
                    await item.save()

                    # FIXME visibility not changed; check timestamps?

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

    async def add_to_collection(self, collection_id, object_id):
        await CollectionItem.create(part_of=collection_id, object_id=object_id)

    async def remove_from_collection(self, collection_id, object_id):
        item = await CollectionItem.get_or_none(
            part_of=collection_id, object_id=object_id
        )

        if item is None:
            return False

        await item.delete()

        return True

    async def collection_count(self, collection_id):
        return await CollectionItem.filter(part_of=collection_id).count()
