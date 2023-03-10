import json
import logging

from bovine.types import ServerSentEvent
from quart import current_app

from .types.processing_item import ProcessingItem

logger = logging.getLogger(__name__)


async def add_to_queue(
    item: ProcessingItem, activity_pub, actor
) -> ProcessingItem | None:
    data = item.get_data()

    data_s = json.dumps(data)
    event = ServerSentEvent(data=data_s, event="inbox")

    if "database_id" in item.meta:
        event.id = item.meta["database_id"]

    # FIXME: Is there a better way to access the queue_manager ?
    # If I do this, I could also access the session in a similar way
    # This would simplify the processor interface

    event_source = actor["endpoints"]["eventSource"]

    queues = current_app.config["queue_manager"].get_queues_for_actor(event_source)

    logging.debug(f"Adding items to {len(queues)} queues")

    for queue in queues:
        await queue.put(event)

    return item
