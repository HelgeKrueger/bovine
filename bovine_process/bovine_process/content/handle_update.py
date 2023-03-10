import logging

from bovine_core.activitystreams.utils import actor_for_object
from bovine_store.store import (
    retrieve_remote_object,
    store_remote_object,
    update_remote_object,
)
from bovine_process.types.processing_item import ProcessingItem

logger = logging.getLogger(__name__)


async def handle_update(item: ProcessingItem, activity_pub, actor) -> ProcessingItem:
    data = item.get_data()

    owner = actor_for_object(data)

    await store_remote_object(owner, data, visible_to=[actor["id"]])

    object_to_update = data.get("object")
    if object_to_update is None or object_to_update.get("id") is None:
        logger.warning("Update without object %s", item.body)
        return

    to_update_from_db = await retrieve_remote_object(owner, object_to_update["id"])

    if to_update_from_db:
        await update_remote_object(owner, object_to_update)

    return item
