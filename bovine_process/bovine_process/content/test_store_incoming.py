import json

from bovine_store.utils.test import store  # noqa F401

from bovine_process.types.processing_item import ProcessingItem

from .store_incoming import store_incoming


async def test_store_incoming(store):  # noqa F801
    first_id = "https://my_domain/first"
    second_id = "https://my_domain/second"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
        "object": {
            "type": "Note",
            "id": second_id,
        },
    }

    processing_item = ProcessingItem(json.dumps(item))

    result = await store_incoming(processing_item, {}, {"id": "local_actor_url"})

    assert result == processing_item

    first = await store.retrieve("local_actor_url", first_id)
    second = await store.retrieve("local_actor_url", second_id)

    assert first["id"] == first_id
    assert first["object"] == second_id
    assert second["id"] == second_id
