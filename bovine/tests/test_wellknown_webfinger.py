from bovine.utils.test.in_memory_test_app import app


async def test_no_argument_leads_to_bad_request() -> None:
    client = app.test_client()

    response = await client.get("/.well-known/webfinger")

    assert response.status_code == 400


async def test_unknown_account() -> None:
    client = app.test_client()

    response = await client.get("/.well-known/webfinger?resource=acct:unknown")

    assert response.status_code == 404

    data = await response.get_json()

    assert data["status"] == "not found"


async def test_success() -> None:
    client = app.test_client()

    response = await client.get("/.well-known/webfinger?resource=acct:user")

    assert response.status_code == 200
    # Label: webfinger-content-type
    assert response.headers["content-type"] == "application/jrd+json"

    data = await response.get_json()

    assert data["subject"] == "acct:user@my_domain"
    assert "links" in data


async def test_success_with_domain() -> None:
    client = app.test_client()

    response = await client.get("/.well-known/webfinger?resource=acct:user@my_domain")

    assert response.status_code == 200

    data = await response.get_json()

    assert data["subject"] == "acct:user@my_domain"
    assert "links" in data


async def test_success_with_other_domain() -> None:
    client = app.test_client()

    response = await client.get("/.well-known/webfinger?resource=acct:user@other")

    assert response.status_code == 404
