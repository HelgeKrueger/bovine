import asyncio

from .collection import (
    remove_from_collection,
    add_to_collection,
    collection_count,
    collection_items,
)

from . import store_remote_object
from .test_store import store  # noqa F401


first_id = "https://my_domain/first"
second_id = "https://my_domain/second"
item = {
    "@context": "https://www.w3.org/ns/activitystreams",
    "id": second_id,
    "type": "Like",
}


async def test_add_remove_item(store):  # noqa F811
    assert not await remove_from_collection(first_id, second_id)

    await add_to_collection(first_id, second_id)
    await store_remote_object("owner", item, as_public=True)

    assert await collection_count("retriever", first_id) == 1

    assert await remove_from_collection(first_id, second_id)

    assert await collection_count("retriever", first_id) == 0


async def test_not_public_item_not_retrieved(store):  # noqa F811
    await add_to_collection(first_id, second_id)
    await store_remote_object("owner", item, as_public=False)
    assert await collection_count("retriever", first_id) == 0


async def test_owner_can_retrieve(store):  # noqa F811
    await add_to_collection(first_id, second_id)
    await store_remote_object("owner", item, as_public=False)
    assert await collection_count("owner", first_id) == 1


async def test_public_item_retrieved(store):  # noqa F811
    await add_to_collection(first_id, second_id)
    await store_remote_object("owner", item, as_public=True)
    assert await collection_count("retriever", first_id) == 1


async def test_item_is_visible_retrieved(store):  # noqa F811
    await add_to_collection(first_id, second_id)
    await store_remote_object("owner", item, as_public=False, visible_to=["retriever"])
    assert await collection_count("retriever", first_id) == 1


async def test_follower_can_see_item(store):  # noqa F811
    await add_to_collection(first_id, second_id)
    await add_to_collection("follower", "retriever")
    await asyncio.sleep(0.01)
    await store_remote_object("owner", item, as_public=False, visible_to=["follower"])
    assert await collection_count("retriever", first_id) == 1


async def test_follower_after_cannot_see_item(store):  # noqa F811
    await add_to_collection(first_id, second_id)
    await store_remote_object("owner", item, as_public=False, visible_to=["follower"])
    await asyncio.sleep(0.01)
    await add_to_collection("follower", "retriever")
    assert await collection_count("retriever", first_id) == 0


def numbered_item(number):
    return {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": f"https://my_domain/item/number/{number}",
        "type": "Note",
        "content": f"item number {number}",
    }


async def test_items_from_collection(store):  # noqa F811
    for j in range(37):
        item = numbered_item(j)
        await add_to_collection(first_id, item["id"])
        await store_remote_object("owner", item, as_public=True)

    assert await collection_count("retriever", first_id) == 37

    items = await collection_items("retriever", first_id, last=1)

    assert "items" in items
    assert len(items["items"]) == 10
    assert items["items"][0] == "https://my_domain/item/number/9"
    assert items["items"][9] == "https://my_domain/item/number/0"

    items = await collection_items("retriever", first_id, first=1)

    assert "items" in items
    assert len(items["items"]) == 10
    assert items["items"][0] == "https://my_domain/item/number/36"
    assert items["items"][9] == "https://my_domain/item/number/27"

    items = await collection_items("retriever", first_id, min_id=17)

    assert "items" in items
    assert len(items["items"]) == 10
    assert items["items"][0] == "https://my_domain/item/number/15"
    assert items["items"][9] == "https://my_domain/item/number/6"

    items = await collection_items("retriever", first_id, max_id=17)

    assert "items" in items
    assert len(items["items"]) == 10
    assert items["items"][0] == "https://my_domain/item/number/26"
    assert items["items"][9] == "https://my_domain/item/number/17"
