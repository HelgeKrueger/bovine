import logging

import bovine_core.clients.signed_http

from quart import current_app

from bovine.types import ProcessingItem, LocalActor

logger = logging.getLogger(__name__)


async def fetch_object_and_process(
    item: ProcessingItem, local_actor: LocalActor
) -> ProcessingItem | None:
    url = item.get_data().get("object", None)

    if not url:
        logger.warning("object not present on item")
        return item

    session = current_app.config["session"]

    response = await bovine_core.clients.signed_http.signed_get(
        session, local_actor.get_public_key_url(), local_actor.private_key, url
    )

    fetched_item = ProcessingItem(await response.text())
    await local_actor.process_inbox_item(fetched_item)

    return item
