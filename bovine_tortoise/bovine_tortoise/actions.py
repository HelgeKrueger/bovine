import json
import logging
from datetime import datetime
from urllib.parse import urlparse

import aiohttp
import bovine.clients
from bovine.clients.lookup_account import lookup_account_with_webfinger
from bovine.types import InboxItem, LocalUser
from bovine_core.activitystreams.activities import build_follow
from bovine_core.clients.signed_http import signed_get

from .models import Actor, Following

logger = logging.getLogger("bovine_torroise")


async def follow(session: aiohttp.ClientSession, local_user: LocalUser, account: str):
    actor = await Actor.get_or_none(account=local_user.name)

    if actor is None:
        logger.error(f"Actor not found !!!! {local_user.name}")
        return

    account_url = await lookup_account_with_webfinger(session, account)

    if account_url is None:
        logging.error(f"Failed to lookup account {account}")
        return

    logger.info(f"Found account url {account_url}")

    response = await signed_get(
        session, local_user.get_public_key_url(), local_user.private_key, account_url
    )

    text = await response.text()
    data = json.loads(text)
    inbox = data["inbox"]

    await Following.create(actor=actor, account=account_url, followed_on=datetime.now())

    logging.debug("created following")

    domain = urlparse(local_user.url).netloc
    activity = build_follow(domain, local_user.url, account_url).build()

    await bovine.clients.send_activitypub_request(session, local_user, inbox, activity)


async def fetch_post(
    session: aiohttp.ClientSession, local_user: LocalUser, post_url: str
):
    response = await signed_get(
        session, local_user.get_public_key_url(), local_user.private_key, post_url
    )
    text = await response.text()

    inbox_item = InboxItem(text)
    await local_user.process_inbox_item(inbox_item, session)
