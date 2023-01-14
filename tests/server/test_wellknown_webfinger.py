import pytest

from bovine.test.in_memory_test_app import app


@pytest.mark.asyncio
async def test_no_argument_leads_to_bad_request() -> None:
    client = app.test_client()

    response = await client.get("/.well-known/webfinger")

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_unknown_account() -> None:
    client = app.test_client()

    response = await client.get("/.well-known/webfinger?resource=acct:unknown")

    assert response.status_code == 404

    data = await response.get_json()

    assert data["status"] == "not found"


@pytest.mark.asyncio
async def test_success() -> None:
    client = app.test_client()

    response = await client.get("/.well-known/webfinger?resource=acct:user")

    assert response.status_code == 200

    data = await response.get_json()

    assert data["subject"] == "acct:user@my_domain"
    assert "links" in data


@pytest.mark.asyncio
async def test_success_with_domain() -> None:
    client = app.test_client()

    response = await client.get("/.well-known/webfinger?resource=acct:user@my_domain")

    assert response.status_code == 200

    data = await response.get_json()

    assert data["subject"] == "acct:user@my_domain"
    assert "links" in data
