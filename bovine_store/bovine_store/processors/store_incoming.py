import logging

from bovine.types import LocalActor, ProcessingItem

from bovine_store.store import store_remote_object
from bovine_store.store.collection import add_to_collection

logger = logging.getLogger(__name__)


async def store_incoming(
    item: ProcessingItem, local_actor: LocalActor
) -> ProcessingItem:
    data = item.get_data()

    # FIXME: Who owns an object?

    await store_remote_object(local_actor.url, data, visible_to=[local_actor.url])
    return item


async def add_incoming_to_inbox(
    item: ProcessingItem, local_actor: LocalActor
) -> ProcessingItem:
    data = item.get_data()
    object_id = data.get("id")

    if object_id is None:
        logger.warning("Tried to store object with id to %", local_actor.get_inbox())
        return item

    stored_item = await add_to_collection(local_actor.get_inbox(), object_id)

    item.meta["database_id"] = stored_item.id

    return item
