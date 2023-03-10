import logging
import traceback

from bovine.activitystreams.utils import actor_for_object
from bovine_store.jsonld import combine_items
from bovine_store.store import retrieve_remote_object, store_remote_object

from bovine_process.types.processing_item import ProcessingItem

logger = logging.getLogger(__name__)


async def incoming_actor(item: ProcessingItem, activity_pub, actor) -> ProcessingItem:
    data = item.get_data()
    owner = actor_for_object(data)

    if owner is None or owner == "__NO__ACTOR__":
        logger.warning("Retrieved object without actor %s", item.body)
        return item

    if data["type"] == "Delete":
        return item

    try:
        remote_actor = await retrieve_remote_object(actor["id"], owner)
        if remote_actor:
            data = combine_items(data, [remote_actor])
            item = item.set_data(data)
            return item

        remote_actor = await activity_pub.get(owner)
        await store_remote_object(owner, remote_actor, visible_to=[actor["id"]])

        data = combine_items(data, [remote_actor])

        item = item.set_data(data)
    except Exception as ex:
        logger.warning("Failed to retrieve remote actor %s due to %s", owner, ex)
        for log_line in traceback.format_exc().splitlines():
            logger.warning(log_line)

    return item
