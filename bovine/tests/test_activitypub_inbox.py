from bovine.utils.test.in_memory_test_app import app


async def test_activitypub_inbox_post_is_not_implemented() -> None:
    client = app.test_client()

    response = await client.post("/activitypub/user/inbox")

    assert response.status_code == 501
