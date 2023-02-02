import logging

import aiohttp
import bovine_core.clients.signed_http

from bovine.types import InboxItem, LocalUser

logger = logging.getLogger("proc-fetch")


async def fetch_object_and_process(
    item: InboxItem, local_user: LocalUser, session: aiohttp.ClientSession
) -> InboxItem | None:
    url = item.get_data().get("object", None)

    if not url:
        logger.warning("object not present on item")
        return item

    response = await bovine_core.clients.signed_http.signed_get(
        session, local_user.get_public_key_url(), local_user.private_key, url
    )

    fetched_item = InboxItem(await response.text())
    await local_user.process_inbox_item(fetched_item, session)

    return item
