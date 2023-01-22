from datetime import datetime
from unittest.mock import patch

import aiohttp

from bovine.types import LocalUser

from .models import Actor, Follower, OutboxEntry
from .outbox import outbox_item_count, outbox_items, send_activity
from .test_database import db_url  # noqa: F401


async def test_basic_outbox(db_url):  # noqa: F811
    actor = await Actor.create(
        account="name",
        url="url",
        actor_type="type",
        private_key="private_key",
        public_key="public_key",
    )
    await OutboxEntry.create(
        actor=actor, created=datetime.now(), local_path="my_path", content={"a": "b"}
    )

    local_user = LocalUser("name", "url", "public_key", "private_key", "actor_type")

    result = await outbox_item_count(local_user)

    assert result == 1

    items = await outbox_items(local_user, 0, 10)

    assert items == [{"a": "b"}]


@patch("bovine.clients.send_activitypub_request")
async def test_send_activity(mock_send_activitypub_request, db_url):  # noqa: F811
    actor = await Actor.create(
        account="name",
        url="url",
        actor_type="type",
        private_key="private_key",
        public_key="public_key",
    )

    await Follower.create(
        actor=actor,
        account="follower_1",
        inbox="inbox_1",
        followed_on=datetime.utcnow(),
    )

    local_user = LocalUser("name", "url", "public_key", "private_key", "actor_type")

    activity_to_send = {
        "id": "https://domain/something/name/uuid",
        "to": ["somebody/followers"],
    }

    async with aiohttp.ClientSession() as session:
        await send_activity(
            session,
            local_user,
            activity_to_send,
            "local_path",
        )

    assert mock_send_activitypub_request.await_count == 1

    outbox_elements = OutboxEntry.filter(actor=actor)
    assert await outbox_elements.count() == 1
    element = await outbox_elements.get()

    assert element.content == activity_to_send
    assert element.local_path == "local_path"


@patch("bovine.clients.get_inbox", return_value="other_inbox")
@patch("bovine.clients.send_activitypub_request")
async def test_send_activity_with_additional_user(
    mock_send_activitypub_request, mock_get_inbox, db_url  # noqa: F811
):
    actor = await Actor.create(
        account="name",
        url="url",
        actor_type="type",
        private_key="private_key",
        public_key="public_key",
    )

    await Follower.create(
        actor=actor,
        account="follower_1",
        inbox="inbox_1",
        followed_on=datetime.utcnow(),
    )

    local_user = LocalUser("name", "url", "public_key", "private_key", "actor_type")

    activity_to_send = {
        "id": "https://domain/something/name/uuid",
        "to": ["somebody/followers", "some_user"],
    }

    async with aiohttp.ClientSession() as session:
        await send_activity(
            session,
            local_user,
            activity_to_send,
            "local_path",
        )
    await mock_get_inbox.awaited_once()
    assert mock_send_activitypub_request.await_count == 2

    outbox_elements = OutboxEntry.filter(actor=actor)
    assert await outbox_elements.count() == 1
    element = await outbox_elements.get()

    assert element.content == activity_to_send
    assert element.local_path == "local_path"
