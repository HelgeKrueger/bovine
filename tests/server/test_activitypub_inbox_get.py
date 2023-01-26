import pytest

from bovine.utils.test.in_memory_test_app import app


@pytest.mark.asyncio
async def test_activitypub_inbox_get_without_header() -> None:
    client = app.test_client()

    response = await client.get("/activitypub/user/inbox_tmp")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_activitypub_inbox_get_with_header() -> None:
    client = app.test_client()

    headers = {"Authorization": "Bearer test_token"}

    response = await client.get("/activitypub/user/inbox_tmp", headers=headers)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_activitypub_inbox_get_with_incorrect_header() -> None:
    client = app.test_client()

    headers = {"Authorization": "Bearer wrong"}

    response = await client.get("/activitypub/user/inbox_tmp", headers=headers)

    assert response.status_code == 401
