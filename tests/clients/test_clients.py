import aiohttp

# import pytest
from bovine import get_bovine_user
from bovine.clients import get_public_key, get_inbox


# @pytest.mark.skip
async def test_get_public_key():
    bovine_user = get_bovine_user("test_domain")
    async with aiohttp.ClientSession() as session:
        key = await get_public_key(
            bovine_user, session, "https://mas.to/users/helgek#main-key"
        )

    assert key.startswith("-----BEGIN PUBLIC KEY-----\n")
    assert key.endswith("\n-----END PUBLIC KEY-----\n")


# @pytest.mark.skip
async def test_get_inbox():
    inbox = await get_inbox("https://mas.to/users/helgek")

    assert inbox == "https://mas.to/users/helgek/inbox"
