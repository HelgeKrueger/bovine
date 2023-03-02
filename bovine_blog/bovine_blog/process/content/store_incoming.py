import logging

# from bovine.types import ProcessingItem
from bovine_core.activitystreams.utils import actor_for_object, recipients_for_object
from bovine_store.store import store_remote_object
from bovine_store.store.collection import add_to_collection

logger = logging.getLogger(__name__)


async def store_incoming(item, activity_pub, local_actor):
    data = item.get_data()
    owner = actor_for_object(data)
    recipients = recipients_for_object(data)
    recipients.add(local_actor["id"])

    await store_remote_object(owner, data, visible_to=recipients)

    logger.info("Owner %s", owner)
    logger.info("Recipients %s", ";".join(list(recipients)))

    return item


async def add_incoming_to_inbox(item, activity_pub, local_actor):
    data = item.get_data()
    object_id = data.get("id")

    if object_id is None:
        logger.warning("Tried to store object with id to %s", local_actor["inbox"])
        return item

    stored_item = await add_to_collection(local_actor["inbox"], object_id)

    item.meta["database_id"] = stored_item.id

    return item


async def add_incoming_to_outbox(item, activity_pub, local_actor):
    data = item.get_data()
    object_id = data.get("id")

    if object_id is None:
        logger.warning("Tried to store object with id to %s", local_actor["outbox"])
        return item

    stored_item = await add_to_collection(local_actor["outbox"], object_id)

    item.meta["database_id"] = stored_item.id

    return item
