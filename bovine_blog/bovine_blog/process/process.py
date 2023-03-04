import asyncio
import json
import logging

from bovine.processors.processor_list import ProcessorList
from bovine.types import ProcessingItem
from bovine_core.activitystreams.utils import recipients_for_object, remove_public
from bovine_store.store.collection import collection_all
from quart import current_app

from . import default_content_processors
from .add_to_queue import add_to_queue
from .content.store_incoming import (
    add_incoming_to_inbox,
    add_incoming_to_outbox,
    store_incoming,
)
from .fetch.incoming_actor import incoming_actor
from .follow.accept_follow import accept_follow

logger = logging.getLogger(__name__)


default_inbox_process = (
    ProcessorList()
    .add_for_types(
        **default_content_processors,
    )
    .add(store_incoming)
    .add(add_incoming_to_inbox)
    .add(incoming_actor)
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


default_async_outbox_process = ProcessorList().add_for_types(Accept=accept_follow).apply


async def process_inbox(request, activity_pub, actor):
    logger.info("Processing inbox request")
    data = await request.get_json()

    item = ProcessingItem(json.dumps(data))

    await default_inbox_process(item, activity_pub, actor)

    logger.debug(json.dumps(data))


async def get_inbox_for_recipient(activity_pub, recipient):
    try:
        actor = await activity_pub.get(recipient)
        return actor["inbox"]
    except Exception as ex:
        logger.warning("Failed to fetch inbox for %s with %s", recipient, ex)
        return


async def send_outbox_item(item, activity_pub, actor):
    await default_async_outbox_process(item, activity_pub, actor)

    logger.info("Sending outbox item")

    data = item.get_data()

    recipients = recipients_for_object(data)
    recipients = remove_public(recipients)

    host = current_app.config["host"]

    endpoints = [x for x in recipients if x.startswith(host + "/endpoints")]

    if len(endpoints) > 0:
        endpoint_recipients = set(
            sum(
                (
                    await asyncio.gather(
                        *[
                            collection_all(actor["id"], endpoint)
                            for endpoint in endpoints
                        ]
                    )
                ),
                [],
            )
        )
        recipients = {x for x in recipients if x not in endpoints}.union(
            endpoint_recipients
        )
    inboxes = [
        await get_inbox_for_recipient(activity_pub, x)
        for x in recipients
        if x != actor["id"] and x not in endpoints
    ]
    inboxes = [x for x in inboxes if x and x != actor["inbox"]]

    logger.info("Inboxes %s", "-".join(inboxes))

    for inbox in inboxes:
        response = await activity_pub.post(inbox, data)
        logger.info(await response.text())
