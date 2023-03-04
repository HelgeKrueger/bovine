import logging

from bovine.types import ProcessingItem
from bovine_core.activitystreams.utils import actor_for_object
from bovine_store.store import retrieve_remote_object
from bovine_store.store.collection import add_to_collection

logger = logging.getLogger(__name__)


async def follow_accept(item: ProcessingItem, activity_pub, actor) -> ProcessingItem:
    data = item.get_data()

    if data["type"] != "Accept":
        return item

    obj = data["object"]
    if isinstance(obj, str):
        logger.info("retrieving remote object %s for %s", obj, actor["id"])
        obj = await retrieve_remote_object(actor["id"], obj)

    if obj["type"] != "Follow":
        return item

    if obj["actor"] != actor["id"]:
        logger.warning("Got following for incorrect actor %s", obj["actor"])
        return item

    remote_actor = actor_for_object(data)

    await add_to_collection(actor["following"], remote_actor)

    logger.info("Added %s to following %s", remote_actor, actor["following"])

    return item
