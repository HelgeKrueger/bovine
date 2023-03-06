import asyncio
import logging

from tortoise import Tortoise

from bovine_store.jsonld import split_into_objects
from bovine_store.models import StoredJsonObject

from .retrieve_object import retrieve_remote_object

from .local import store_local_object
from .store import store_remote_object

logger = logging.getLogger(__name__)


async def update_remote_object(owner, item):
    # FIXME Currently update does not handle visibility changes

    to_store = await split_into_objects(item)

    tasks = [
        StoredJsonObject.update_or_create(
            id=obj["id"],
            defaults={
                "content": obj,
            },
        )
        for obj in to_store
    ]

    items = await asyncio.gather(*tasks)

    return items


async def remove_remote_object(remover, object_id):
    result = await StoredJsonObject.get_or_none(id=object_id)

    if result and result.owner == remover:
        await result.delete()


class ObjectStore:
    def __init__(self, db_url="sqlite://store.db", id_generator=None):
        self.db_url = db_url
        self.id_generator = id_generator

    async def init_connection(self):
        await Tortoise.init(
            db_url=self.db_url, modules={"models": ["bovine_store.models"]}
        )
        await Tortoise.generate_schemas()

    async def close_connection(self):
        await Tortoise.close_connections()

    async def retrieve(self, retriever, object_id, include=[]):
        return await retrieve_remote_object(retriever, object_id, include=include)

    async def store(self, owner, item, as_public=False, visible_to=[]):
        return await store_remote_object(
            owner, item, as_public=as_public, visible_to=visible_to
        )

    async def store_local(self, owner, item, as_public=False, visible_to=[]):
        if self.id_generator:
            return await store_local_object(
                owner,
                item,
                as_public=as_public,
                visible_to=visible_to,
                id_generator=self.id_generator,
            )
        return await store_local_object(
            owner, item, as_public=as_public, visible_to=visible_to
        )
