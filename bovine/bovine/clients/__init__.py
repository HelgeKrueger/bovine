import json
import logging

import aiohttp
import bovine_core.clients.signed_http

from bovine.types import LocalActor

logger = logging.getLogger(__name__)


async def get_public_key(
    session: aiohttp.ClientSession, local_actor: LocalActor, key_id: str
) -> str | None:
    logger.info(f"getting public key for {key_id}")

    response = await bovine_core.clients.signed_http.signed_get(
        session, local_actor.get_public_key_url(), local_actor.private_key, key_id
    )
    text = await response.text()

    try:
        data = json.loads(text)
    except Exception:
        logger.warning(f"Failed to decode json from {text}")
        return None

    if "publicKey" not in data:
        logger.warning(f"Public key not found in data for {key_id}")
        return None

    key_data = data["publicKey"]

    if key_data["id"] != key_id:
        logger.warning(f"Public key id mismatches for {key_id}")
        return None

    return key_data["publicKeyPem"]


async def get_inbox(
    session: aiohttp.ClientSession, local_actor: LocalActor, account: str
) -> str:
    response = await bovine_core.clients.signed_http.signed_get(
        session, local_actor.get_public_key_url(), local_actor.private_key, account
    )
    text = await response.text()
    data = json.loads(text)

    return data["inbox"]


async def send_activitypub_request(
    session: aiohttp.ClientSession, user: LocalActor, inbox, data
) -> tuple[str, int]:
    body = json.dumps(data)

    response = await bovine_core.clients.signed_http.signed_post(
        session, user.get_public_key_url(), user.private_key, inbox, body
    )
    text = await response.text()
    logger.debug(f"Send activity pub request to {inbox} with response {text}")

    return text, response.status
