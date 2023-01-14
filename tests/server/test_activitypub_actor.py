import pytest

from bovine.test.in_memory_test_app import app
from bovine.test import remove_domain_from_url


@pytest.mark.asyncio
async def test_activitypub_actor_unknown_user() -> None:
    client = app.test_client()

    response = await client.get("/activitypub/unknown")

    assert response.status_code == 404

    data = await response.get_json()

    assert data == {"status": "not found"}


@pytest.mark.asyncio
async def test_activitypub_actor() -> None:
    client = app.test_client()

    response = await client.get("/activitypub/user")
    data = await response.get_json()

    assert "https://www.w3.org/ns/activitystreams" in data["@context"]
    assert "https://w3id.org/security/v1" in data["@context"]

    assert data["id"] == "https://my_domain/activitypub/user"
    assert data["type"] == "Person"
    assert data["inbox"] == "https://my_domain/activitypub/user/inbox"
    assert data["outbox"] == "https://my_domain/activitypub/user/outbox"


@pytest.mark.asyncio
async def test_activitypub_actor_public_key() -> None:
    client = app.test_client()

    response = await client.get("/activitypub/user")
    data = await response.get_json()

    assert "publicKey" in data

    key_data = data["publicKey"]

    assert key_data["publicKeyPem"].startswith("-----BEGIN PUBLIC KEY-----\n")
    assert key_data["publicKeyPem"].endswith("\n-----END PUBLIC KEY-----\n")


@pytest.mark.asyncio
async def test_activitypub_actor_inbox() -> None:
    client = app.test_client()

    response = await client.get("/activitypub/user")
    data = await response.get_json()

    inbox_url = data["inbox"]

    response = await client.get(remove_domain_from_url(inbox_url))

    assert response.status_code == 405


@pytest.mark.asyncio
async def test_activitypub_actor_outbox() -> None:
    client = app.test_client()

    response = await client.get("/activitypub/user")
    data = await response.get_json()

    outbox_url = data["outbox"]

    response = await client.get(remove_domain_from_url(outbox_url))

    assert response.status_code == 200
