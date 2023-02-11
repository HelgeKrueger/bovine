import os

import pytest

from .store import Store


@pytest.fixture
async def store():
    db_file = "test_db.db"
    db_url = f"sqlite://{db_file}"
    store = Store(db_url)

    await store.init_connection()

    yield store
    await store.close_connection()
    os.unlink(db_file)


async def test_store_retrieval(store):
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

    await store.store("owner", item)

    first = await store.retrieve("owner", first_id)
    second = await store.retrieve("owner", second_id)

    assert first["id"] == first_id
    assert first["object"] == second_id
    assert second["id"] == second_id


async def test_store_retrieval_with_object(store):
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

    await store.store("owner", item)

    first = await store.retrieve("owner", first_id, include=["object"])

    assert first["id"] == first_id
    assert isinstance(first["object"], dict)
    assert first["object"]["id"] == second_id


async def test_store_basic_access(store):
    first_id = "https://my_domain/first"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
    }

    await store.store("owner", item)

    owner = await store.retrieve("owner", first_id)
    other = await store.retrieve("other", first_id)

    assert owner is not None
    assert other is None
