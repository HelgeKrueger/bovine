from datetime import datetime

from bovine_tortoise.models import Actor, OutboxEntry
from bovine_tortoise.utils import db_url  # noqa: F401

from .tortoise import TortoiseStore


async def test_index_contents(db_url):  # noqa F811
    store = TortoiseStore()

    result = await store.index_contents()

    assert result == []


async def test_with_data(db_url):  # noqa F811
    first, second = [
        await Actor.create(
            account=name,
            url="url",
            actor_type="type",
            private_key="private_key",
            public_key="public_key",
        )
        for name in ["first", "second"]
    ]
    for actor in [first, second]:
        await OutboxEntry().create(
            actor=actor,
            local_path=actor.account,
            created=datetime.now(),
            content={"a": "b"},
        )

    store = TortoiseStore()

    result = await store.index_contents()

    assert len(result) == 2

    result = await store.user_contents("first")

    assert len(result) == 1
