from unittest.mock import AsyncMock

import pytest

from bovine.utils.test.in_memory_test_app import app


@pytest.mark.asyncio
async def test_activitypub_inbox_get_without_header() -> None:
    client = app.test_client()

    response = await client.get("/activitypub/user/inbox")

    assert response.status_code == 302

    headers = {
        "accept": "application/activity+json",
    }

    response = await client.get("/activitypub/user/inbox", headers=headers)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_activitypub_inbox_get_with_header() -> None:
    client = app.test_client()

    app.config["account_name_or_none_for_token"] = AsyncMock()
    app.config["account_name_or_none_for_token"].return_value = "user"

    headers = {
        "Authorization": "Bearer test_token",
        "accept": "application/activity+json",
    }

    response = await client.get("/activitypub/user/inbox", headers=headers)

    assert response.status_code == 200

    app.config["account_name_or_none_for_token"].assert_awaited_once_with("test_token")


@pytest.mark.asyncio
async def test_activitypub_inbox_get_with_incorrect_header() -> None:
    client = app.test_client()

    app.config["account_name_or_none_for_token"] = AsyncMock()
    app.config["account_name_or_none_for_token"].return_value = None

    headers = {
        "Authorization": "Bearer wrong",
        "accept": "application/activity+json",
    }

    response = await client.get("/activitypub/user/inbox", headers=headers)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_activitypub_inbox_get_with_wrong_user() -> None:
    client = app.test_client()

    app.config["account_name_or_none_for_token"] = AsyncMock()
    app.config["account_name_or_none_for_token"].return_value = "wrong"

    headers = {
        "Authorization": "Bearer wrong",
        "accept": "application/activity+json",
    }

    response = await client.get("/activitypub/user/inbox", headers=headers)

    assert response.status_code == 401
