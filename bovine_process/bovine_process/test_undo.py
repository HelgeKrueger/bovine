import json

from bovine_store.utils.test import store  # noqa F401

from .content.store_incoming import store_incoming
from .types.processing_item import ProcessingItem
from .undo import undo


async def test_undo_bad_format(store):  # noqa F801
    first_id = "https://my_domain/first"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Undo",
    }

    processing_item = ProcessingItem(json.dumps(item))

    result = await undo(processing_item, {}, {})

    assert result is None


async def test_undo(store):  # noqa F801a
    actor = "https://remote_actor"
    first_id = "https://my_domain/first"
    second_id = "https://my_domain/second"

    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Like",
        "actor": actor,
        "id": second_id,
    }

    processing_item = ProcessingItem(json.dumps(item))
    result = await store_incoming(processing_item, {}, {"id": "local_actor_url"})

    undo_item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "actor": actor,
        "type": "Undo",
        "object": item,
    }

    processing_item = ProcessingItem(json.dumps(undo_item))
    result = await undo(processing_item, {}, {"id": "local_actor_url"})

    assert result is None

    first = await store.retrieve("local_actor_url", first_id)
    second = await store.retrieve("local_actor_url", second_id)

    assert first is None
    assert second is None
