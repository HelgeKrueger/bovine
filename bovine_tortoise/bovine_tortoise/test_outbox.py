from datetime import datetime

from bovine.types import LocalUser

from .models import Actor, OutboxEntry
from .outbox import outbox_item_count, outbox_items
from .test_database import db_url  # noqa: F401


async def actor_and_local_user():
    actor = await Actor.create(
        account="name",
        url="url",
        actor_type="type",
        private_key="private_key",
        public_key="public_key",
    )
    local_user = LocalUser("name", "url", "public_key", "private_key", "actor_type")

    return actor, local_user


async def test_basic_outbox(db_url):  # noqa: F811
    actor, local_user = await actor_and_local_user()

    await OutboxEntry.create(
        actor=actor, created=datetime.now(), local_path="my_path", content={"a": "b"}
    )

    result = await outbox_item_count(local_user)
    assert result == 1

    items = await outbox_items(local_user)
    assert items == {"items": [{"a": "b"}], "prev": "max_id=1", "next": "min_id=1"}


async def test_full_outbox_behavior(db_url):  # noqa: F811
    actor, local_user = await actor_and_local_user()

    for j in range(10):
        await OutboxEntry.create(
            actor=actor,
            created=datetime.now(),
            local_path="my_path",
            content={"number": j},
        )

    result = await outbox_item_count(local_user)
    assert result == 10

    data = await outbox_items(local_user, limit=2, first=1)
    items = data["items"]
    assert len(items) == 2
    assert items[0] == {"number": 9}
    assert items[1] == {"number": 8}

    new_data = await outbox_items(
        local_user, limit=2, **dict([data["prev"].split("=")])
    )

    assert len(new_data["items"]) == 0

    new_data = await outbox_items(
        local_user, limit=2, **dict([data["next"].split("=")])
    )
    items = new_data["items"]
    assert len(items) == 2
    assert items[0] == {"number": 7}
    assert items[1] == {"number": 6}

    data = await outbox_items(local_user, limit=2, last=1)
    items = data["items"]
    assert len(items) == 2
    assert items[0] == {"number": 1}
    assert items[1] == {"number": 0}

    new_data = await outbox_items(
        local_user, limit=2, **dict([data["next"].split("=")])
    )
    assert len(new_data["items"]) == 0

    new_data = await outbox_items(
        local_user, limit=2, **dict([data["prev"].split("=")])
    )
    items = new_data["items"]
    assert len(items) == 2
    assert items[0] == {"number": 3}
    assert items[1] == {"number": 2}
