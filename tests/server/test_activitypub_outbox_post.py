import json
from bovine.utils.test.in_memory_test_app import app


async def test_activitypub_post_to_outbox() -> None:
    client = app.test_client()
    response = await client.post(
        "/activitypub/user/outbox",
        data="XXX",
        headers={"Accept": "application/activity+json"},
    )

    data = await response.get_json()

    assert data == {"status": "request not signed"}


async def test_activitypub_post_with_token() -> None:
    client = app.test_client()
    response = await client.post(
        "/activitypub/user/outbox",
        data=json.dumps({"test": "xxx"}),
        headers={
            "Accept": "application/activity+json",
            "Authorization": "Bearer test_token",
        },
    )

    data = await response.get_json()

    assert data == {"status": "success"}
