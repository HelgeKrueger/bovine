import json

from bovine_store.utils.test import store  # noqa F401

from bovine_process.types.processing_item import ProcessingItem

from .handle_update import handle_update
from .store_incoming import store_incoming


async def test_basic_update(store):  # noqa F801
    remote_actor = "https://remote_domain/actor"
    first_id = "https://my_domain/first"
    second_id = "https://my_domain/second"
    third_id = "https://my_domain/third"
    create = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
        "actor": remote_actor,
        "object": {"type": "Note", "id": second_id, "content": "new"},
    }

    update = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": third_id,
        "type": "Create",
        "actor": remote_actor,
        "object": {"type": "Note", "id": second_id, "content": "updated"},
    }

    processing_item = ProcessingItem(json.dumps(create))

    await store_incoming(processing_item, {}, {"id": "local_actor_url"})

    stored = await store.retrieve("local_actor_url", second_id)
    assert stored["content"] == "new"

    processing_item = ProcessingItem(json.dumps(update))
    await handle_update(processing_item, {}, {"id": "local_actor_url"})

    stored = await store.retrieve("local_actor_url", second_id)
    assert stored["content"] == "updated"
