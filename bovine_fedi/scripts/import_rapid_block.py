import asyncio
import json

import aiohttp
from bovine_tortoise.models import Peer
from bovine_tortoise.utils import init
from bovine_tortoise.utils.peer_type import PeerType
from tortoise import Tortoise


async def fetch_blocklist(session):
    response = await session.get("https://rapidblock.org/blocklist.json", timeout=60)
    data = await response.text()

    parsed = json.loads(data)

    result = [
        domain for domain, value in parsed["blocks"].items() if value["isBlocked"]
    ]

    return result


async def update_peers(blocklist):
    await init()

    for domain in blocklist:
        peer, _ = await Peer.get_or_create(domain=domain)
        peer.peer_type = PeerType.BLOCKED
        await peer.save()

    await Tortoise.close_connections()


async def main():
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        blocklist = await fetch_blocklist(session)
        await update_peers(blocklist)


if __name__ == "__main__":
    asyncio.run(main())
