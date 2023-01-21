import json
import aiohttp
from datetime import datetime
import logging

from bovine.utils.crypto import content_digest_sha256
from bovine.types import LocalUser

from bovine.utils import build_signature
from .signed_http import signed_get


async def get_public_key(
    local_user: LocalUser, session: aiohttp.ClientSession, key_id: str
) -> str | None:

    response = await signed_get(
        session, local_user.get_public_key_url(), local_user.private_key, key_id
    )
    text = await response.text()
    data = json.loads(text)

    if "publicKey" not in data:
        logging.warning(f"Public key not found in data for {key_id}")
        return None

    key_data = data["publicKey"]

    if key_data["id"] != key_id:
        logging.warning(f"Public key id mismatches for {key_id}")
        return None

    return key_data["publicKeyPem"]


async def get_inbox(actor) -> dict:
    headers = {"accept": "application/activity+json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(actor, headers=headers) as response:
            text = await response.text()
            data = json.loads(text)

            return data["inbox"]


async def send_activitypub_request(inbox, data, user: LocalUser) -> tuple[str, int]:
    headers = {"Accept": "application/activity+json"}

    body = json.dumps(data)

    host = inbox.split("/")[2]
    target = "/" + "/".join(inbox.split("/")[3:])

    digest = content_digest_sha256(body)
    date_header = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    content_type = "application/activity+json"

    signature_header = (
        build_signature(host, "post", target)
        .with_field("date", date_header)
        .with_field("digest", digest)
        .with_field("content-type", content_type)
        .build_signature(user.get_public_key_url(), user.private_key)
    )

    headers["Digest"] = digest
    headers["Date"] = date_header
    headers["Content-Type"] = "application/activity+json"
    headers["Signature"] = signature_header

    async with aiohttp.ClientSession() as session:
        async with session.post(inbox, data=body, headers=headers) as response:
            text = await response.text()

            logging.info(f"Send activity pub request to {inbox}")
            logging.info(text)

            return text, response.status
