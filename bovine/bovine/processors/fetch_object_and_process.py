import logging

import aiohttp
import bovine_core.clients.signed_http

from bovine.types import ProcessingItem, LocalActor

logger = logging.getLogger("proc-fetch")


async def fetch_object_and_process(
    item: ProcessingItem, local_actor: LocalActor, session: aiohttp.ClientSession
) -> ProcessingItem | None:
    url = item.get_data().get("object", None)

    if not url:
        logger.warning("object not present on item")
        return item

    response = await bovine_core.clients.signed_http.signed_get(
        session, local_actor.get_public_key_url(), local_actor.private_key, url
    )

    fetched_item = ProcessingItem(await response.text())
    await local_actor.process_inbox_item(fetched_item, session)

    return item
