from bovine_store.utils.test import store  # noqa F401

from . import store_remote_object
from .retrieve_object import retrieve_remote_object


async def test_store_retrieval(store):  # noqa F811
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

    await store_remote_object("owner", item)

    first = await retrieve_remote_object("owner", first_id, include=["object"])

    assert first == item

    second = await retrieve_remote_object("owner", second_id, include=["object"])

    assert set(second.keys()) == {"@context", "type", "id"}
