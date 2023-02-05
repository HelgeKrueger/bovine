from .local_actor import LocalActor


async def test_items_and_item_count():
    local_actor = LocalActor("name", "url", "public_key", "private_key", "actor_type")

    assert await local_actor.item_count_for("outbox")() == 0
    assert await local_actor.item_count_for("inbox")() == 0

    assert await local_actor.items_for("outbox")() == {"items": []}
    assert await local_actor.items_for("inbox")() == {"items": []}
