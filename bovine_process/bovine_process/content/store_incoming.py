import logging

from bovine_core.activitystreams.utils import (
    actor_for_object,
    is_public,
    recipients_for_object,
    remove_public,
)
from bovine_store.store import store_remote_object
from bovine_store.store.collection import add_to_collection

logger = logging.getLogger(__name__)


async def store_incoming(item, activity_pub, local_actor):
    data = item.get_data()
    owner = actor_for_object(data)
    recipients = remove_public(recipients_for_object(data))
    recipients.add(local_actor["id"])

    await store_remote_object(owner, data, visible_to=recipients)

    logger.info("Owner %s Recipients %s", owner, " | ".join(list(recipients)))
    return item


async def store_outgoing(item, activity_pub, local_actor):
    data = item.get_data()
    owner = actor_for_object(data)

    if is_public(data):
        await store_remote_object(owner, data, as_public=True)
        logger.info("Owner %s, public", owner)

    else:
        recipients = remove_public(recipients_for_object(data))
        recipients.add(local_actor["id"])

        await store_remote_object(owner, data, visible_to=recipients)
        logger.info("Owner %s Recipients %s", owner, " | ".join(list(recipients)))

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
