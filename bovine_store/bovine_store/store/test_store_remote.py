import pytest

from bovine_store.utils.test import store  # noqa F401

from .store import store_remote_object


async def test_store_remote_object_like_stored(store):  # noqa F811
    first_id = "https://my_domain/first"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Like",
    }

    await store_remote_object("owner", item)

    first = await store.retrieve("owner", first_id)
    assert first == item


@pytest.mark.parametrize(
    "object_type",
    ["Collection", "OrderedCollection", "CollectionPage", "OrderedCollectionPage"],
)
async def test_store_remote_object_collections_are_not_stored(
    store, object_type  # noqa F811
):
    first_id = "https://my_domain/first"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": object_type,
    }

    await store_remote_object("owner", item)

    first = await store.retrieve("owner", first_id)
    assert first is None
