import logging
from urllib.parse import urlparse

import aiohttp

from bovine.utils import build_signature
from bovine.utils.crypto import content_digest_sha256
from bovine.utils.date import get_gmt_now

from .consts import BOVINE_CLIENT_NAME
from .event_source import EventSource

logger = logging.getLogger(__name__)


async def signed_get(
    session: aiohttp.ClientSession,
    public_key_url: str,
    private_key: str,
    url: str,
    headers: dict = {},
) -> aiohttp.ClientResponse:
    logger.debug(f"Signed get with {public_key_url} on {url}")

    parsed_url = urlparse(url)
    host = parsed_url.netloc
    target = parsed_url.path

    accept = "application/activity+json"
    content_type = "application/activity+json"
    date_header = get_gmt_now()

    signature_header = (
        build_signature(host, "get", target)
        .with_field("date", date_header)
        .with_field("accept", accept)
        .build_signature(public_key_url, private_key)
    )

    headers["accept"] = accept
    headers["date"] = date_header
    headers["host"] = host
    headers["content-type"] = content_type
    headers["signature"] = signature_header
    headers["user-agent"] = BOVINE_CLIENT_NAME
    return await session.get(url, headers=headers)


def signed_event_source(
    session: aiohttp.ClientSession,
    public_key_url: str,
    private_key: str,
    url: str,
    headers: dict = {},
):
    logger.debug(f"Signed event source with {public_key_url} on {url}")

    parsed_url = urlparse(url)
    host = parsed_url.netloc
    target = parsed_url.path

    accept = "text/event-stream"
    date_header = get_gmt_now()

    signature_header = (
        build_signature(host, "get", target)
        .with_field("date", date_header)
        .with_field("accept", accept)
        .build_signature(public_key_url, private_key)
    )

    headers["accept"] = accept
    headers["date"] = date_header
    headers["host"] = host
    headers["signature"] = signature_header
    headers["user-agent"] = BOVINE_CLIENT_NAME
    return EventSource(session, url, headers=headers)


async def signed_post(
    session: aiohttp.ClientSession,
    public_key_url: str,
    private_key: str,
    url: str,
    body: str,
    headers: dict = {},
    content_type=None,
) -> aiohttp.ClientResponse:
    logger.debug(f"Signed post with {public_key_url} on {url}")

    parsed_url = urlparse(url)
    host = parsed_url.netloc
    target = parsed_url.path

    accept = "application/activity+json"
    # LABEL: ap-s2s-content-type
    if content_type is None:
        content_type = "application/activity+json"
    date_header = get_gmt_now()

    digest = content_digest_sha256(body)

    signature_header = (
        build_signature(host, "post", target)
        .with_field("date", date_header)
        .with_field("digest", digest)
        .with_field("content-type", content_type)
        .build_signature(public_key_url, private_key)
    )

    headers["accept"] = accept
    headers["digest"] = digest
    headers["date"] = date_header
    headers["host"] = host
    headers["content-type"] = content_type
    headers["signature"] = signature_header
    headers["user-agent"] = BOVINE_CLIENT_NAME

    return await session.post(url, data=body, headers=headers)
