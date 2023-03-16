import json
import logging

from .add_to_queue import add_to_queue
from .content.handle_update import handle_update
from .content.incoming_delete import incoming_delete
from .content.store_incoming import (
    add_incoming_to_inbox,
    add_incoming_to_outbox,
    store_incoming,
    store_outgoing,
)
from .fetch.incoming_actor import incoming_actor
from .follow.accept_follow import accept_follow
from .follow.follow_accept import follow_accept
from .send_item import send_outbox_item
from .types.processing_item import ProcessingItem
from .undo import undo
from .utils.processor_list import ProcessorList

logger = logging.getLogger(__name__)

default_content_processors = {
    "Create": store_incoming,
    "Update": handle_update,
    "Delete": incoming_delete,
    "Undo": undo,
}


default_inbox_process = (
    ProcessorList()
    .add_for_types(**default_content_processors, Accept=follow_accept)
    .add(store_incoming)
    .add(add_incoming_to_inbox)
    .add(incoming_actor)
    .add(add_to_queue)
    .apply
)


default_outbox_process = (
    ProcessorList()
    .add(store_outgoing)
    .add(add_incoming_to_outbox)
    .add_for_types(**default_content_processors)
    .apply
)


default_async_outbox_process = (
    ProcessorList().add_for_types(Accept=accept_follow).add(add_to_queue).apply
)


async def process_inbox(request, activity_pub, actor):
    logger.info("Processing inbox request")
    data = await request.get_json()

    item = ProcessingItem(json.dumps(data))

    await default_inbox_process(item, activity_pub, actor)

    logger.debug(json.dumps(data))


async def process_outbox_item(item, activity_pub, actor):
    await default_async_outbox_process(item, activity_pub, actor)
    await send_outbox_item(item, activity_pub, actor)
