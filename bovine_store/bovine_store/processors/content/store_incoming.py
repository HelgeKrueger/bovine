import logging

from bovine.types import LocalActor, ProcessingItem

from bovine_store.store import store_remote_object
from bovine_store.store.collection import add_to_collection

from bovine_store.utils.activitystreams import actor_for_object, recipients_for_object

logger = logging.getLogger(__name__)


async def store_incoming(
    item: ProcessingItem, local_actor: LocalActor
) -> ProcessingItem:
    data = item.get_data()

    owner = actor_for_object(data)
    recipients = recipients_for_object(data)
    recipients.add(local_actor.url)

    await store_remote_object(owner, data, visible_to=recipients)
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
