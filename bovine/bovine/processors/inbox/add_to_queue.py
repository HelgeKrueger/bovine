from quart import current_app
import json

from bovine.types import ProcessingItem, LocalActor
from bovine.types.server_side_event import ServerSentEvent

import logging

logger = logging.getLogger(__name__)


async def add_to_queue(
    item: ProcessingItem, local_actor: LocalActor, session
) -> ProcessingItem | None:
    data = item.get_data()

    data_s = json.dumps(data)
    event = ServerSentEvent(data=data_s, event="outbox")

    if "database_id" in item.meta:
        event.id = item.meta["database_id"]

    # FIXME: Is there a better way to access the queue_manager ?
    # If I do this, I could also access the session in a similar way
    # This would simplify the processor interface

    queues = current_app.config["queue_manager"].get_queues_for_actor(local_actor.name)

    logging.debug(f"Adding items to {len(queues)} queues")

    for queue in queues:
        await queue.put(event)

    return item
