import asyncio
from urllib.parse import urlparse

import aiohttp
from bovine.clients.nodeinfo import fetch_nodeinfo
from bovine_tortoise.models import Peer, PublicKey
from bovine_tortoise.utils import init
from bovine_tortoise.utils.peer_type import PeerType
from tortoise import Tortoise


async def update_peers():
    public_keys = await PublicKey.all()
    domains = {urlparse(x.url).netloc for x in public_keys}
    for domain in domains:
        await Peer.get_or_create(domain=domain)


async def get_for_peer(session, peer):
    return (peer, await fetch_nodeinfo(session, peer.domain))


async def update_nodeinfo():
    async with aiohttp.ClientSession() as session:
        peers = await Peer().filter(software__not_isnull=False).all()
        for peer in peers:
            try:
                nodeinfo = await fetch_nodeinfo(session, peer.domain)
                peer.software = nodeinfo["software"]["name"]
                peer.version = nodeinfo["software"]["version"]
                await peer.save()
                print(peer.domain)
            except Exception:
                peer.peer_type = PeerType.OFFLINE
                await peer.save()
                print(f"Nodeinfo failed for {peer.domain}")


async def main():
    await init()

    # await update_peers()

    await update_nodeinfo()

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(main())
