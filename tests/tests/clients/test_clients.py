import aiohttp
from bovine import get_bovine_user
from bovine.clients import get_inbox, get_public_key


async def test_get_public_key():
    bovine_user = get_bovine_user("test_domain")
    async with aiohttp.ClientSession() as session:
        key = await get_public_key(
            session, bovine_user, "https://mas.to/users/helgek#main-key"
        )

    assert key.startswith("-----BEGIN PUBLIC KEY-----\n")
    assert key.endswith("\n-----END PUBLIC KEY-----\n")


async def test_get_inbox():
    bovine_user = get_bovine_user("test_domain")
    async with aiohttp.ClientSession() as session:
        inbox = await get_inbox(session, bovine_user, "https://mas.to/users/helgek")

    assert inbox == "https://mas.to/users/helgek/inbox"
