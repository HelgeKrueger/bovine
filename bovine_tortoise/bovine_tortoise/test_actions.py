from unittest.mock import patch

import aiohttp
from bovine.types import LocalUser
from bovine.utils.test import get_user_keys

from . import ManagedDataStore
from .actions import fetch_post, follow
from .models import Following, InboxEntry
from .processors.inbox import store_in_database
from .utils.test import db_url  # noqa: F401


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


# @patch("bovine.clients.send_activitypub_request")
async def test_fetch_post(
    # mock_send_activitypub_request,
    db_url,  # noqa: F811
):
    public_key, private_key = get_user_keys()
    local_user = LocalUser(
        "name", "url", public_key, private_key, "actor_type"
    ).set_inbox_process(store_in_database)
    store = ManagedDataStore(db_url=db_url)

    await store.add_user(local_user)
    async with aiohttp.ClientSession() as session:
        await fetch_post(
            session, local_user, "https://social.exozy.me/@a/109718407634106530"
        )

    assert await InboxEntry.filter().count() == 1
