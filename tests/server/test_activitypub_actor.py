from unittest.mock import AsyncMock
import pytest

from bovine.utils.test import remove_domain_from_url
from bovine.utils.test.in_memory_test_app import app


async def test_activitypub_actor_unauthorized() -> None:
    client = app.test_client()
    app.config["account_name_or_none_for_token"] = AsyncMock()
    app.config["account_name_or_none_for_token"].return_value = "unknown"

    response = await client.get(
        "/activitypub/unknown",
        headers={"Accept": "application/activity+json"},
    )

    assert response.status_code == 401

    data = await response.get_json()

    assert data == {"status": "http signature not valid"}


async def return_true(*args, **kwargs):
    return True


async def return_false(*args, **kwargs):
    return True


async def test_activitypub_actor_unknown_user() -> None:
    app.config["validate_signature"] = return_true
    client = app.test_client()

    response = await client.get(
        "/activitypub/unknown",
        headers={"Accept": "application/activity+json"},
    )

    assert response.status_code == 404

    data = await response.get_json()

    assert data == {"status": "not found"}


@pytest.mark.asyncio
async def test_activitypub_actor() -> None:
    client = app.test_client()

    response = await client.get(
        "/activitypub/user",
        headers={"Accept": "application/activity+json"},
    )
    data = await response.get_json()

    assert "https://www.w3.org/ns/activitystreams" in data["@context"]
    assert "https://w3id.org/security/v1" in data["@context"]

    assert data["id"] == "https://my_domain/activitypub/user"
    assert data["type"] == "Person"
    assert data["inbox"] == "https://my_domain/activitypub/user/inbox"
    assert data["outbox"] == "https://my_domain/activitypub/user/outbox"


async def test_activitypub_actor_public_key() -> None:
    client = app.test_client()

    response = await client.get(
        "/activitypub/user",
        headers={"Accept": "application/activity+json"},
    )
    data = await response.get_json()

    assert "publicKey" in data

    key_data = data["publicKey"]

    assert key_data["publicKeyPem"].startswith("-----BEGIN PUBLIC KEY-----\n")
    assert key_data["publicKeyPem"].endswith("\n-----END PUBLIC KEY-----\n")


async def test_activitypub_actor_inbox() -> None:
    client = app.test_client()

    response = await client.get(
        "/activitypub/user",
        headers={"Accept": "application/activity+json"},
    )
    data = await response.get_json()

    inbox_url = data["inbox"]

    response = await client.get(
        remove_domain_from_url(inbox_url),
        headers={"Accept": "application/activity+json"},
    )

    assert response.status_code == 405


async def test_activitypub_actor_outbox() -> None:
    client = app.test_client()

    response = await client.get(
        "/activitypub/user",
        headers={"Accept": "application/activity+json"},
    )
    data = await response.get_json()

    outbox_url = data["outbox"]

    response = await client.get(
        remove_domain_from_url(outbox_url),
        headers={"Accept": "application/activity+json"},
    )

    assert response.status_code == 200


async def test_activitypub_bovine_actor() -> None:
    app.config["validate_signature"] = return_false
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
