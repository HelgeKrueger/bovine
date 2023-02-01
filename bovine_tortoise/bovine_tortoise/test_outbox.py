from datetime import datetime

from bovine.types import LocalUser

from .models import Actor, OutboxEntry
from .outbox import outbox_item_count, outbox_items
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
