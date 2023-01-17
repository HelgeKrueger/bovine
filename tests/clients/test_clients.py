import pytest

from bovine.clients import get_public_key, get_inbox


@pytest.mark.skip
@pytest.mark.asyncio
async def test_get_public_key():
    key = await get_public_key("https://mas.to/users/helgek#main-key")

    assert key.startswith("-----BEGIN PUBLIC KEY-----\n")
    assert key.endswith("\n-----END PUBLIC KEY-----\n")


@pytest.mark.skip
@pytest.mark.asyncio
async def test_get_inbox():
    inbox = await get_inbox("https://mas.to/users/helgek")

    assert inbox == "https://mas.to/users/helgek/inbox"
