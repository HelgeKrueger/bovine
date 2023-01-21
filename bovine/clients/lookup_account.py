import aiohttp
import json
import logging

from bovine.utils.parsers import parse_account_name


async def lookup_account(
    session: aiohttp.ClientSession, account_name: str
) -> str | None:
    username, domain = parse_account_name(account_name)

    webfinger_url = f"https://{domain}/.well-known/webfinger"

    params = {"resource": f"acct:{username}@{domain}"}

    async with session.get(webfinger_url, params=params, timeout=10) as response:
        if response.status != 200:
            logging.warn(f"{account_name} not found using webfinger")
            return None
        text = await response.text()
        data = json.loads(text)

        if "links" not in data:
            return None

        links = data["links"]
        for entry in links:
            if "rel" in entry and entry["rel"] == "self":
                return entry["href"]

    return None
