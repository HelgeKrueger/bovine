import aiohttp

from .nodeinfo import fetch_nodeinfo


async def test_fetch_nodeinfo():
    session = aiohttp.ClientSession()

    result = await fetch_nodeinfo(session, "mymath.rocks")

    assert result["software"] == {"name": "bovine", "version": "0.0.1"}
