import json
import logging

import aiohttp

from bovine.types import LocalUser

import bovine_core.clients.signed_http


async def get_public_key(
    session: aiohttp.ClientSession, local_user: LocalUser, key_id: str
) -> str | None:

    logging.info(f"getting public key for {key_id}")

    response = await bovine_core.clients.signed_http.signed_get(
        session, local_user.get_public_key_url(), local_user.private_key, key_id
    )
    text = await response.text()

    try:
        data = json.loads(text)
    except Exception:
        logging.warning(f"Failed to decode json from {text}")
        return None

    if "publicKey" not in data:
        logging.warning(f"Public key not found in data for {key_id}")
        return None

    key_data = data["publicKey"]

    if key_data["id"] != key_id:
        logging.warning(f"Public key id mismatches for {key_id}")
        return None

    return key_data["publicKeyPem"]


async def get_inbox(
    session: aiohttp.ClientSession, local_user: LocalUser, account: str
) -> str:
    response = await bovine_core.clients.signed_http.signed_get(
        session, local_user.get_public_key_url(), local_user.private_key, account
    )
    text = await response.text()
    data = json.loads(text)

    return data["inbox"]


async def send_activitypub_request(
    session: aiohttp.ClientSession, user: LocalUser, inbox, data
) -> tuple[str, int]:
    body = json.dumps(data)

    response = await bovine_core.clients.signed_http.signed_post(
        session, user.get_public_key_url(), user.private_key, inbox, body
    )
    logging.info(f"Send activity pub request to {inbox}")
    text = await response.text()
    logging.debug(text)

    return text, response.status
