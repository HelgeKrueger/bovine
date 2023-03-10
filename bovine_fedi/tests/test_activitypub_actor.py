from bovine_fedi.utils.test.in_memory_test_app import app


async def test_activitypub_bovine_actor() -> None:
    client = app.test_client()

    response = await client.get(
        "/activitypub/bovine",
        headers={"Accept": "application/activity+json"},
    )

    assert response.status_code == 200

    data = await response.get_json()

    assert data["id"] == "https://my_domain/activitypub/bovine"
    assert "publicKey" in data

    key_data = data["publicKey"]

    assert key_data["publicKeyPem"].startswith("-----BEGIN PUBLIC KEY-----\n")
    assert key_data["publicKeyPem"].endswith("\n-----END PUBLIC KEY-----\n")


async def test_activitypub_inbox_post_is_not_implemented() -> None:
    client = app.test_client()

    response = await client.post("/activitypub/user/inbox")

    assert response.status_code == 501
