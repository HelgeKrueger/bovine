from unittest.mock import AsyncMock, MagicMock

from bovine.types.base_count_and_items import BaseCountAndItems

from bovine.utils.test.in_memory_test_app import (  # noqa F401
    data_store,
    test_client_with_authorization,
)


async def test_activitypub_outbox_with_configured_coroutines(
    test_client_with_authorization,  # noqa F811
) -> None:
    count_and_items = MagicMock(BaseCountAndItems)
    count_and_items.item_count = AsyncMock()
    count_and_items.item_count.return_value = 1
    count_and_items.items = AsyncMock()
    count_and_items.items.return_value = {"items": [{"a": "b"}]}

    data_store.users["user"].set_stream("outbox", count_and_items)

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
    count_and_items = MagicMock(BaseCountAndItems)
    count_and_items.item_count = AsyncMock()
    count_and_items.item_count.return_value = 100
    count_and_items.items = AsyncMock()
    count_and_items.items.return_value = {"items": [{"a": "b"}]}

    data_store.users["user"].set_stream("outbox", count_and_items)

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
