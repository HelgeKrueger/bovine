import aiohttp

from .nodeinfo import fetch_nodeinfo


async def test_fetch_nodeinfo():
    async with aiohttp.ClientSession() as session:
        result = await fetch_nodeinfo(session, "mymath.rocks")

        assert result["software"]["name"] == "bovine"
        assert "version" in result["software"]
