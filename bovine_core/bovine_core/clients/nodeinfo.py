import json
import logging
import traceback

import aiohttp

from .consts import BOVINE_CLIENT_NAME

logger = logging.getLogger(__name__)


async def fetch_nodeinfo(session: aiohttp.ClientSession, domain: str) -> dict | None:
    try:
        wellknown_nodeinfo_url = f"https://{domain}/.well-known/nodeinfo"

        async with session.get(
            wellknown_nodeinfo_url,
            headers={"user-agent": BOVINE_CLIENT_NAME},
            timeout=60,
        ) as response:
            text = await response.text()
            data = json.loads(text)

        for link in data["links"]:
            if link["rel"] == "http://nodeinfo.diaspora.software/ns/schema/2.0":
                return await fetch_nodeinfo20(session, link["href"])

        return None

    except Exception as e:
        logger.error(str(e))
        for log_line in traceback.format_exc().splitlines():
            logger.error(log_line)
        return None


async def fetch_nodeinfo20(session: aiohttp.ClientSession, url: str) -> dict | None:
    try:
        async with session.get(
            url, headers={"user-agent": BOVINE_CLIENT_NAME}
        ) as response:
            text = await response.text()
            return json.loads(text)

    except Exception as e:
        logger.error(str(e))
        for log_line in traceback.format_exc().splitlines():
            logger.error(log_line)
        return None
