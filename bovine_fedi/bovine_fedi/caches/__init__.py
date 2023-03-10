import json
import logging

import aiohttp
import bovine.clients.signed_http

from bovine_fedi.types import LocalActor

from .public_key import PublicKeyCache

logger = logging.getLogger(__name__)


def build_public_key_fetcher(session: aiohttp.ClientSession, bovine_user: LocalActor):
    def get_public_key_wrapper(key_id):
        return get_public_key(session, bovine_user, key_id)

    cache = PublicKeyCache(get_public_key_wrapper)

    return cache.get_for_url


async def get_public_key(
    session: aiohttp.ClientSession, local_actor: LocalActor, key_id: str
) -> str | None:
    logger.info(f"getting public key for {key_id}")

    response = await bovine.clients.signed_http.signed_get(
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
