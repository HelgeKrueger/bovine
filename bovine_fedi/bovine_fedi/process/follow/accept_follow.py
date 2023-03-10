import logging

from bovine.types import ProcessingItem
from bovine_core.activitystreams.utils import actor_for_object
from bovine_store.store import retrieve_remote_object
from bovine_store.store.collection import add_to_collection

logger = logging.getLogger(__name__)


async def accept_follow(item: ProcessingItem, activity_pub, actor) -> ProcessingItem:
    data = item.get_data()

    if data["type"] != "Accept":
        return item

    obj = data["object"]
    if isinstance(obj, str):
        obj = await retrieve_remote_object(actor["id"], obj)

    if obj["type"] != "Follow":
        return item

    remote_actor = actor_for_object(obj)

    await add_to_collection(actor["followers"], remote_actor)

    logger.info("Added %s to followers %s", remote_actor, actor["followers"])

    return item
