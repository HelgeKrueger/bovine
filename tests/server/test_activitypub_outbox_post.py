import json
from unittest.mock import AsyncMock

from bovine.utils.test.in_memory_test_app import app


async def test_activitypub_post_to_outbox() -> None:
    client = app.test_client()
    response = await client.post(
        "/activitypub/user/outbox",
        data=json.dumps({"test": "xxx"}),
        headers={"Accept": "application/activity+json"},
    )

    data = await response.get_json()

    assert response.status_code == 401
    assert data == {"status": "access denied"}


async def test_activitypub_post_with_token() -> None:
    app.config["account_name_or_none_for_token"] = AsyncMock()
    app.config["account_name_or_none_for_token"].return_value = "user"

    client = app.test_client()
    response = await client.post(
        "/activitypub/user/outbox",
        data=json.dumps({"test": "xxx"}),
        headers={
            "Accept": "application/activity+json",
            "Content-Type": "application/activity+json",
            "Authorization": "Bearer test_token",
        },
    )

    data = await response.get_json()

    assert data == {"status": "success"}
