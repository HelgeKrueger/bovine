from bovine.utils.parsers import parse_signature_header
from bovine.utils.crypto import content_digest_sha256, verify_signature
from bovine.clients import get_public_key
from bovine.stores import LocalUser
from . import InboxItem


async def verify_inbox_request(
    local_user: LocalUser, item: InboxItem
) -> InboxItem | None:
    for header in ["Signature", "Digest", "Host", "Date", "Content-Type"]:
        if header not in item.headers:
            return

    signature_header = item.headers["Signature"]
    digest = item.headers["Digest"]
    host = item.headers["Host"]

    date_header = item.headers["Date"]
    content_type = item.headers["Content-Type"]

    headers = parse_signature_header(signature_header)

    content = item.body

    if digest != content_digest_sha256(content):
        return

    public_key = await get_public_key(headers.key_id)

    message = "\n".join(
        [
            "(request-target): post /activitypub/test/inbox",
            f"host: {host}",
            f"date: {date_header}",
            f"digest: {digest}",
            f"content-type: {content_type}",
        ]
    )
    if not verify_signature(public_key, message, headers.signature):
        return

    return item
