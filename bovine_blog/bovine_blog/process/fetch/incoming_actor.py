import json
import logging
import traceback

from bovine.types import LocalActor, ProcessingItem
from bovine_core.activitystreams.utils import actor_for_object
from bovine_store.jsonld import combine_items
from bovine_store.store import retrieve_remote_object, store_remote_object

logger = logging.getLogger(__name__)


async def incoming_actor(
    item: ProcessingItem, local_actor: LocalActor
) -> ProcessingItem:
    data = item.get_data()
    owner = actor_for_object(data)

    if owner is None or owner == "__NO__ACTOR__":
        logger.warning("Retrieved object without actor %s", item.body)
        return item

    try:
        actor = await retrieve_remote_object(local_actor.url, owner)
        if actor:
            data = combine_items(data, [actor])
            item = item.set_data(data)
            return item

        response = await local_actor.client().get(owner)
        actor = json.loads(await response.text())
        await store_remote_object(owner, actor)

        data = combine_items(data, [actor])

        item = item.set_data(data)
    except Exception as ex:
        logger.warning("Failed to retrieve remote actor %s due to %s", owner, ex)
        for log_line in traceback.format_exc().splitlines():
            logger.warning(log_line)

    return item
