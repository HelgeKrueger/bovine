from datetime import datetime
from unittest.mock import patch

import aiohttp

from bovine.types import LocalUser
from bovine_tortoise.models import Actor, Follower, OutboxEntry
from bovine_tortoise.test_database import db_url  # noqa: F401

from .outbox import send_activity, create_outbox_entry


async def test_send_create_outbox_entry(db_url):  # noqa: F811
    actor = await Actor.create(
        account="name",
        url="url",
        actor_type="type",
        private_key="private_key",
        public_key="public_key",
    )

    local_user = LocalUser("name", "url", "public_key", "private_key", "actor_type")

    activity_to_send = {
        "id": "https://domain/something/name/uuid",
        "to": ["somebody/followers"],
    }

    async with aiohttp.ClientSession() as session:
        result = await create_outbox_entry(
            activity_to_send,
            local_user,
            session,
        )

    assert result == activity_to_send

    outbox_elements = OutboxEntry.filter(actor=actor)
    assert await outbox_elements.count() == 1
    element = await outbox_elements.get()

    assert element.content == activity_to_send
    assert element.local_path == "name/uuid"


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
