from bovine.utils.test.in_memory_test_app import app, data_store


async def test_activitypub_outbox_with_configured_coroutines() -> None:
    client = app.test_client()

    async def item_count(local_user):
        return 1

    async def items(local_user, start, limit):
        return [{"start": start, "limit": limit}]

    data_store.users["user"].set_outbox(item_count, items)

    response = await client.get(
        "/activitypub/user/outbox",
        headers={"Accept": "application/activity+json"},
    )

    assert response.status_code == 200

    data = await response.get_json()

    assert data["totalItems"] == 1
    assert data["orderedItems"] == [{"start": 0, "limit": 10}]
