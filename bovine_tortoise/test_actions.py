import aiohttp
from unittest.mock import patch

from bovine.types import LocalUser
from bovine.utils.test import get_user_keys

from .test_database import db_url  # noqa: F401
from .actions import follow
from .models import Following
from . import ManagedDataStore


@patch("bovine.clients.send_activitypub_request")
async def test_follow(
    mock_send_activitypub_request,
    db_url,  # noqa: F811
):
    public_key, private_key = get_user_keys()
    local_user = LocalUser("name", "url", public_key, private_key, "actor_type")
    store = ManagedDataStore(db_url=db_url)

    await store.add_user(local_user)
    async with aiohttp.ClientSession() as session:
        await follow(session, local_user, "helgek@mas.to")

    assert await Following.filter().count() == 1

    mock_send_activitypub_request.assert_awaited_once()
