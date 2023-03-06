from bovine_store.utils.test import store  # noqa F401

from . import store_remote_object


# FIXME Collections should not be stored

# FIXME Local / Remote is notspecified i.e. the ObjectType property
# FIXME The ObjectType is necessary to effectively clean up remote
# FIXME objects after say a few days


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

    first = await store.retrieve("owner", first_id)
    second = await store.retrieve("owner", second_id)

    assert first["id"] == first_id
    assert first["object"] == second_id
    assert second["id"] == second_id


async def test_store_retrieval_with_object(store):  # noqa F811
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

    first = await store.retrieve("owner", first_id, include=["object"])

    assert first["id"] == first_id
    assert isinstance(first["object"], dict)
    assert first["object"]["id"] == second_id


async def test_store_basic_access(store):  # noqa F811
    first_id = "https://my_domain/first"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
    }

    await store_remote_object("owner", item)

    owner = await store.retrieve("owner", first_id)
    other = await store.retrieve("other", first_id)

    assert owner is not None
    assert other is None


async def test_store_public_access(store):  # noqa F811
    first_id = "https://my_domain/first"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
    }

    await store_remote_object("owner", item, as_public=True)

    other = await store.retrieve("other", first_id)

    assert other is not None
    assert other["id"] == first_id


async def test_store_visible_to_other(store):  # noqa F811
    first_id = "https://my_domain/first"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
    }

    await store_remote_object("owner", item, visible_to=["other"])

    other = await store.retrieve("other", first_id)

    assert other is not None
    assert other["id"] == first_id


async def test_store_update(store):  # noqa F811
    first_id = "https://my_domain/first"
    second_id = "https://my_domain/second"
    third_id = "https://my_domain/third"

    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
        "object": {"type": "Note", "id": second_id, "content": "new"},
    }

    second_item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": third_id,
        "type": "Create",
        "object": {"type": "Note", "id": second_id, "content": "updated"},
    }

    await store_remote_object("owner", item)
    await store_remote_object("owner", second_item)

    data = await store.retrieve("owner", second_id)

    assert data["content"] == "updated"
