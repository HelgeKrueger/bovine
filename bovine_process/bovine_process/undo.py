import logging

from bovine_core.activitystreams.utils import actor_for_object
from bovine_store.store import remove_remote_object
from .types.processing_item import ProcessingItem

logger = logging.getLogger(__name__)


async def undo(item: ProcessingItem, activity_pub, actor) -> ProcessingItem:
    data = item.get_data()
    owner = actor_for_object(data)

    object_to_undo = data.get("object")
    if isinstance(object_to_undo, dict):
        object_to_undo = object_to_undo.get("id")

    if object_to_undo is None:
        logger.warning("Undo without object %s", item.body)
        return

    logger.info("Removing object with id %s for %s", object_to_undo, owner)

    await remove_remote_object(owner, object_to_undo)

    return
