import asyncio
import logging
import traceback

from bovine.activitystreams.utils import recipients_for_object, remove_public
from bovine_store.store.collection import collection_all
from quart import current_app

logger = logging.getLogger(__name__)


async def get_inbox_for_recipient(activity_pub, recipient):
    try:
        store = current_app.config["bovine_store"]
        actor = await store.retrieve(activity_pub.actor_id, recipient)
        if not actor:
            actor = await activity_pub.get(recipient)
        return actor["inbox"]
    except Exception as ex:
        logger.warning("Failed to fetch inbox for %s with %s", recipient, ex)
        return


async def send_outbox_item(item, activity_pub, actor):
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

    logger.info("Inboxes %s", " - ".join(inboxes))

    for inbox in inboxes:
        try:
            response = await activity_pub.post(inbox, data)
            logger.info(await response.text())
        except Exception as ex:
            logger.warning("Sending to %s failed with %s", inbox, ex)
            for log_line in traceback.format_exc().splitlines():
                logger.warning(log_line)
