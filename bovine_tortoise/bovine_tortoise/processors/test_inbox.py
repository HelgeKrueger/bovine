import json

from bovine.types import LocalActor, ProcessingItem

from bovine_tortoise.models import Actor, InboxEntry
from bovine_tortoise.utils.test import db_url  # noqa: F401

from .inbox import remove_from_database, store_in_database


async def test_store_in_database(db_url):  # noqa: F811
    actor = await Actor.create(
        account="name",
        url="url",
        actor_type="type",
        private_key="private_key",
        public_key="public_key",
    )
    local_user = LocalActor("name", "url", "public_key", "private_key", "actor_type")

    item = ProcessingItem(
        json.dumps(
            {
                "type": "Create",
                "actor": "url",
                "object": {"conversation": "uid:bovine:123"},
            }
        ),
    )

    result = await store_in_database(item, local_user, None)

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
    local_user = LocalActor("name", "url", "public_key", "private_key", "actor_type")

    item = ProcessingItem(
        json.dumps({"type": "Follow", "actor": "url", "object": "proto://url"}),
    )

    result = await store_in_database(item, local_user, None)

    assert result == item

    entry = await InboxEntry.filter(actor=actor).get()

    assert entry.content["type"] == "Follow"
    assert entry.conversation is None


async def test_store_and_remove_from_database(db_url):  # noqa: F811
    actor = await Actor.create(
        account="name",
        url="url",
        actor_type="type",
        private_key="private_key",
        public_key="public_key",
    )
    local_user = LocalActor("name", "url", "public_key", "private_key", "actor_type")

    item = ProcessingItem(
        json.dumps(
            {"type": "Follow", "actor": "url", "object": "proto://url", "id": "my_id"}
        ),
    )

    assert await InboxEntry.filter(actor=actor).count() == 0

    await store_in_database(item, local_user, None)
    assert await InboxEntry.filter(actor=actor).count() == 1

    await remove_from_database(item, local_user, None)
    assert await InboxEntry.filter(actor=actor).count() == 0

    await remove_from_database(item, local_user, None)
    assert await InboxEntry.filter(actor=actor).count() == 0
