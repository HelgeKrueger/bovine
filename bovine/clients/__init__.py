import json
import aiohttp
from datetime import datetime

from bovine.utils.crypto import content_digest_sha256, sign_message
from bovine.stores import LocalUser


async def get_public_key(key_id):
    headers = {"accept": "application/activity+json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(key_id, headers=headers) as response:
            text = await response.text()
            data = json.loads(text)

            if "publicKey" not in data:
                return

            key_data = data["publicKey"]

            if key_data["id"] != key_id:
                return

            return key_data["publicKeyPem"]


async def get_inbox(actor):
    headers = {"accept": "application/activity+json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(actor, headers=headers) as response:
            text = await response.text()
            data = json.loads(text)

            return data["inbox"]


async def send_activitypub_request(inbox, data, user: LocalUser):
    headers = {"Accept": "application/activity+json"}

    body = json.dumps(data)

    host = inbox.split("/")[2]
    target = "/" + "/".join(inbox.split("/")[3:])

    digest = content_digest_sha256(body)
    date_header = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    content_type = "application/activity+json"

    message = "\n".join(
        [
            f"(request-target): post {target}",
            f"host: {host}",
            f"date: {date_header}",
            f"digest: {digest}",
            f"content-type: {content_type}",
        ]
    )

    signature_string = sign_message(user.private_key, message)

    signature = f'keyId="{user.get_public_key_url()}",algorithm="rsa-sha256",headers="(request-target) host date digest content-type",signature="{signature_string}"'

    headers["Digest"] = digest
    headers["Date"] = date_header
    headers["Content-Type"] = "application/activity+json"
    headers["Signature"] = signature

    async with aiohttp.ClientSession() as session:
        async with session.post(inbox, data=body, headers=headers) as response:
            text = await response.text()
            return text, response.status
