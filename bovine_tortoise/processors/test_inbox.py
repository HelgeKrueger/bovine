import json
from unittest.mock import patch

from bovine.types import InboxItem, LocalUser
from bovine.utils.test.in_memory_test_app import app
from bovine_tortoise.models import Actor, Follower, Following, InboxEntry
from bovine_tortoise.test_database import db_url  # noqa: F401

from .inbox import accept_follow_request, record_accept_follow, store_in_database


@patch("bovine.clients.send_activitypub_request")
async def test_accept_follow_request(
    mock_send_activitypub_request,
    db_url,  # noqa: F811
) -> None:
    async with app.app_context():
        actor = await Actor.create(
            account="name",
            url="url",
            actor_type="type",
            private_key="private_key",
            public_key="public_key",
        )

        local_user = LocalUser("name", "url", "public_key", "private_key", "actor_type")

        item = InboxItem(json.dumps({"type": "Follow", "actor": "url"}))
        result = await accept_follow_request(item, local_user)

        assert result

        mock_send_activitypub_request.assert_called_once()

        followers = Follower.filter(actor=actor)
        assert await followers.count() == 1

        follower = await followers.get()

        assert follower.account == "url"


async def test_store_in_database(db_url):  # noqa: F811
    actor = await Actor.create(
        account="name",
        url="url",
        actor_type="type",
        private_key="private_key",
        public_key="public_key",
    )
    local_user = LocalUser("name", "url", "public_key", "private_key", "actor_type")

    item = InboxItem(
        json.dumps(
            {
                "type": "Create",
                "actor": "url",
                "object": {"conversation": "uid:bovine:123"},
            }
        ),
    )

    result = await store_in_database(item, local_user)

    assert result == item

    entry = await InboxEntry.filter(actor=actor).get()

    assert entry.content["type"] == "Create"
    assert entry.conversation == "uid:bovine:123"


async def test_store_in_database_no_conversation(db_url):  # noqa: F811
    actor = await Actor.create(
        account="name",
        url="url",
        actor_type="type",
        private_key="private_key",
        public_key="public_key",
    )
    local_user = LocalUser("name", "url", "public_key", "private_key", "actor_type")

    item = InboxItem(
        json.dumps({"type": "Follow", "actor": "url", "object": "proto://url"}),
    )

    result = await store_in_database(item, local_user)

    assert result == item

    entry = await InboxEntry.filter(actor=actor).get()

    assert entry.content["type"] == "Follow"
    assert entry.conversation is None


async def test_accepted_follow_request(db_url) -> None:  # noqa: F811
    actor = await Actor.create(
        account="name",
        url="url",
        actor_type="type",
        private_key="private_key",
        public_key="public_key",
    )
    local_user = LocalUser("name", "url", "public_key", "private_key", "actor_type")

    body = json.dumps(
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": "https://following#accept",
            "type": "Accept",
            "actor": "https://following",
            "object": {
                "id": "https://actor/follows",
                "type": "Follow",
                "actor": "https://actor",
                "object": "https://following",
            },
        }
    )

    item = InboxItem(body)

    result = await record_accept_follow(item, local_user)

    assert result == item

    entries = await Following.filter(actor=actor).all()

    assert len(entries) == 1
