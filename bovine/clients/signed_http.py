from datetime import datetime
from urllib.parse import urlparse


from bovine.utils import build_signature


async def signed_get(session, public_key_url, private_key, url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    target = parsed_url.path
    headers = {}

    accept = "application/activity+json"
    content_type = "application/activity+json"
    date_header = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    signature_header = (
        build_signature(host, "get", target)
        .with_field("date", date_header)
        .with_field("accept", accept)
        .build_signature(public_key_url, private_key)
    )

    # logging.warning(signature_header)

    headers["accept"] = accept
    headers["date"] = date_header
    headers["host"] = host
    headers["content-type"] = content_type
    headers["signature"] = signature_header
    headers["user-agent"] = "bovine-client / 0.0.1"
    return await session.get(url, headers=headers)
