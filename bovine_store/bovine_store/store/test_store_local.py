from bovine_store.utils.test import store  # noqa F401

from .local import store_local_object


async def test_store_local_object(store):  # noqa F811
    first_id = "https://my_domain/first"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Like",
    }

    result = await store_local_object("owner", item)

    first = await store.retrieve("owner", first_id)
    assert first is None

    new_id = result[0]["id"]

    second = await store.retrieve("owner", new_id)
    assert second["type"] == "Like"
