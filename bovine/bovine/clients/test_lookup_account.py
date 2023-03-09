import aiohttp

from .lookup_account import lookup_account_with_webfinger


async def test_lookup_account():
    async with aiohttp.ClientSession() as session:
        result = await lookup_account_with_webfinger(session, "helge@mymath.rocks")

    assert result.startswith("https://mymath.rocks/")
