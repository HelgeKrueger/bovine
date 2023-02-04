from bovine.utils.test.in_memory_test_app import (  # noqa F401
    data_store,
    test_client_with_authorization,
)


async def test_activitypub_outbox_with_configured_coroutines(
    test_client_with_authorization,  # noqa F811
) -> None:
    async def item_count(local_user):
        return 1

    async def items(local_user, **kwargs):
        return {"items": [{"a": "b"}]}

    data_store.users["user"].set_outbox(item_count, items)

    response = await test_client_with_authorization.get(
        "/activitypub/user/outbox",
        headers={"Accept": "application/activity+json"},
    )

    assert response.status_code == 200

    data = await response.get_json()

    assert data["totalItems"] == 1

    assert data["orderedItems"] == [{"a": "b"}]


async def test_activitypub_outbox_with_many_items(
    test_client_with_authorization,  # noqa F811
) -> None:
    async def item_count(local_user):
        return 100

    async def items(local_user, *args, **kwargs):
        return {"args": args, "kwargs": kwargs, "items": ["a"]}

    data_store.users["user"].set_outbox(item_count, items)

    response = await test_client_with_authorization.get(
        "/activitypub/user/outbox",
        headers={"Accept": "application/activity+json"},
    )

    assert response.status_code == 200

    data = await response.get_json()
    assert data["type"] == "OrderedCollection"
    assert data["totalItems"] == 100
    assert data["first"]
    assert data["last"]

    first_page_url = data["first"]

    response = await test_client_with_authorization.get(
        first_page_url,
        headers={"Accept": "application/activity+json"},
    )

    assert response.status_code == 200

    data = await response.get_json()
    assert data["id"] == first_page_url
    assert data["partOf"].endswith("/activitypub/user/outbox")
    assert data["type"] == "OrderedCollectionPage"
