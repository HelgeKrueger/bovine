from datetime import datetime
from unittest.mock import patch

import aiohttp
from bovine.types import LocalActor

from bovine_tortoise.models import Actor, Follower, OutboxEntry
from bovine_tortoise.utils.test import db_url  # noqa: F401

from .outbox import create_outbox_entry, delete_outbox_entry, send_activity


async def test_create_outbox_entry(db_url: str) -> None:  # noqa: F811
    actor = await Actor.create(
        account="name",
        url="url",
        actor_type="type",
        private_key="private_key",
        public_key="public_key",
    )

    local_user = LocalActor("name", "url", "public_key", "private_key", "actor_type")

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
    assert element.local_path == "/something/name/uuid"


async def test_delete_outbox_entry(db_url: str) -> None:  # noqa: F811
    actor = await Actor.create(
        account="name",
        url="url",
        actor_type="type",
        private_key="private_key",
        public_key="public_key",
    )

    activity_to_delete = {
        "id": "https://domain/something/name/uuid/delete",
        "to": ["somebody/followers"],
        "object": {
            "id": "https://domain/something/name/uuid",
        },
    }

    await OutboxEntry.create(
        actor=actor,
        created=datetime.now(),
        content=activity_to_delete,
        local_path="/something/name/uuid/activity",
    )

    local_user = LocalActor("name", "url", "public_key", "private_key", "actor_type")

    async with aiohttp.ClientSession() as session:
        result = await delete_outbox_entry(
            activity_to_delete,
            local_user,
            session,
        )

    assert result == activity_to_delete

    outbox_elements = OutboxEntry.filter(actor=actor)
    assert await outbox_elements.count() == 0


@patch("bovine.clients.send_activitypub_request")
async def test_send_activity(
    mock_send_activitypub_request, db_url: str  # noqa: F811
) -> None:
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

    local_user = LocalActor("name", "url", "public_key", "private_key", "actor_type")

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
    mock_send_activitypub_request, mock_get_inbox, db_url: str  # noqa: F811
) -> None:
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

    local_user = LocalActor("name", "url", "public_key", "private_key", "actor_type")

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
