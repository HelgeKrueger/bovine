import logging

from bovine.activitystreams.objects import tombstone
from bovine.activitystreams.utils import actor_for_object
from bovine_store.store import (
    retrieve_remote_object,
    store_remote_object,
    update_remote_object,
)

from bovine_process.types.processing_item import ProcessingItem

logger = logging.getLogger(__name__)


async def incoming_delete(
    item: ProcessingItem, activity_pub, local_actor
) -> ProcessingItem:
    data = item.get_data()

    owner = actor_for_object(data)

    await store_remote_object(owner, data, visible_to=[local_actor["id"]])

    object_to_delete = data.get("object")

    if isinstance(object_to_delete, dict):
        object_to_delete = object_to_delete.get("id")

    if object_to_delete is None:
        logger.warning("Delete without object %s", item.body)
        return

    to_update_from_db = await retrieve_remote_object(owner, object_to_delete)

    if to_update_from_db:
        await update_remote_object(owner, tombstone(object_to_delete))

    return item
    # return None
