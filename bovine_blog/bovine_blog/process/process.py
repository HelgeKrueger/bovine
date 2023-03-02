import json
import logging

from bovine.processors.processor_list import ProcessorList
from bovine.types import ProcessingItem

from . import default_content_processors
from .add_to_queue import add_to_queue
from .content.store_incoming import (
    add_incoming_to_inbox,
    add_incoming_to_outbox,
    store_incoming,
)

logger = logging.getLogger(__name__)


default_inbox_process = (
    ProcessorList()
    .add_for_types(
        **default_content_processors,
        # Accept=record_accept_follow,
        # Announce=fetch_object_and_process,
        # Update=update_in_database,
        # Delete=incoming_delete,
        # Delete=ProcessorList(on_object=True).add(remove_from_database).apply,
        # Follow=accept_follow_request,
        # Undo=ProcessorList(on_object=True)
        # .add_for_types(Like=remove_from_inbox, Announce=remove_from_inbox)
        # .apply,
    )
    # .add(store_in_database)
    .add(store_incoming)
    .add(add_incoming_to_inbox)
    # .add(incoming_actor)
    .add(add_to_queue)
    .apply
)


default_outbox_process = (
    ProcessorList()
    .add_for_types(**default_content_processors)
    .add(store_incoming)
    .add(add_incoming_to_outbox)
    .apply
)


async def process_inbox(request, activity_pub, actor):
    logger.info("Processing inbox request")
    data = await request.get_json()

    item = ProcessingItem(json.dumps(data))

    await default_inbox_process(item, activity_pub, actor)

    logger.debug(json.dumps(data))


async def process_outbox(request, activity_pub, actor):
    logger.info("Processing outbox request")
    data = await request.get_json()

    item = ProcessingItem(json.dumps(data))

    await default_outbox_process(item, activity_pub, actor)

    logger.debug(json.dumps(data))
