import aiohttp

from .lookup_account import lookup_account


async def test_lookup_account():
    async with aiohttp.ClientSession() as session:
        result = await lookup_account(session, "helge@mymath.rocks")

    assert result == "https://mymath.rocks/activitypub/helge"
